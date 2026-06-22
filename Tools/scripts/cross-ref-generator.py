#!/usr/bin/env python3
"""
Cross-Reference Generator for Peace Lab Database (v2 — TF-IDF rewrite)

Rewrite rationale (see Tools/reports/project-evaluation-20260622.md):
  - v1 used 25 coarse topic clusters + alphabetic triplets → absurd links
    (e.g. Ballet_Overview → Necrophilia_Treatment_System).
  - v1's inject step *skipped* files that already had cross_refs (line 174),
    so bad links were never overwritten.
  - v2 uses TF-IDF + cosine similarity on title/headings/body, which
    *mechanically* down-weights ubiquitous words (anxiety/aging have low IDF).
  - v2 OVERWRITES the cross_refs block instead of skipping.

Algorithm:
  - Document vector source: title + H1 + all H2 headings + first 500 chars of
    body (semantically densest region, excluding frontmatter).
  - Tokenization: Chinese char-bigrams (no jieba dependency) + English words.
    Bilingual stopword table is built in.
  - TF-IDF weighting: IDF naturally suppresses generic terms.
  - Matching: cross-pillar only, cosine similarity ≥ SIM_THRESHOLD, top-N.
  - Guardrails:
      1. Drop candidate if no overlap in either doc's top-10 weighted terms.
      2. relation = the top-3 SHARED high-weight real topic terms.
      3. Never link two files whose only shared term is a global stopword.

CLI:
  --dry-run   compute & print samples, modify nothing
  --apply     overwrite cross_refs in all matched files (default: dry-run)
  --verbose   print every file's matched refs
  --sample N  print N detailed sample matchups in dry-run (default 10)

Usage:
  python3 Tools/scripts/cross-ref-generator.py --dry-run --sample 12
  python3 Tools/scripts/cross-ref-generator.py --apply
"""

import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

ROOT = Path(__file__).resolve().parent.parent.parent  # repo root

# Directories that never contain knowledge content. Unified with the other
# Tools/scripts so CI sees a consistent exclude set.
EXCLUDE_DIRS = {
    '.git', '.venv', 'venv', '.env', 'site', 'node_modules',
    'logs', 'reports', 'Tools', 'Project', 'Web', 'Visualization',
    '_meta', '.claude', '.codebuddy', '.qoder', '.trae',
    '__pycache__', '.cache',
}

# Cosine similarity gate. Empirically: meaningful cross-pillar links sit well
# above 0.10; noise clusters below 0.06. 0.15 is conservative after switching
# to dictionary-based CJK extraction (which yields fewer, cleaner terms).
# Minimum number of shared high-weight terms for a link to be accepted.
# A single shared term (even a high-IDF one like 意义/智慧/恐惧) can spuriously
# link unrelated docs (e.g. Confucianism review ↔ Mozart concerto on "智慧").
# Requiring ≥2 shared domain terms demands genuine topical overlap.
MIN_SHARED_TERMS = 2

# Cosine gate. Empirically validated on this corpus (see eval report):
#   0.15 → 58% of files linked — too permissive; templated clinical skeletons
#          (*_Overview.md / *_Clinical_Management.md) cluster on boilerplate
#          and produce links like necrophilia ↔ lower-back-pain.
#   0.25 → 38% linked — sweet spot. Every surviving link has a clean,
#          topic-specific relation label (黄帝内经↔neijing, 拖延↔认知重构,
#          Sogyal Rinpoche↔藏传死亡). Boilerplate-only clusters fall below.
SIM_THRESHOLD = 0.25
MAX_REFS = 4            # max cross-refs to write per file
TOP_TERM_OVERLAP = 10   # top-N weighted terms checked for guardrail #1
RELATION_TERMS = 3      # how many shared terms form the `relation` string

# Pillars that are mirrors of other pillars (06-Clinical-Topics is a curated
# re-projection of 02/03/05 content — md5-identical files confirmed in the
# eval report; e.g. Personal_Development_Atomic_Habits.md is byte-identical
# across 05 and 06). Cross-linking them to their source pillar produces
# cos≈1.0 self-references that add no value, so these pairs are never
# matched against each other. 06 mirrors content from all of 02/03/05.
MIRROR_GROUPS = [
    {'06-Clinical-Topics', '02-Mind-Psychology'},
    {'06-Clinical-Topics', '03-Bio-Science'},
    {'06-Clinical-Topics', '05-Praxis-Growth'},
    {'06-Clinical-Topics', '01-Wisdom-Traditions'},
    {'06-Clinical-Topics', '04-Humanities-Arts'},
]

# English function-word stopwords.
EN_STOP = {
    'the', 'a', 'an', 'and', 'or', 'but', 'of', 'to', 'in', 'on', 'for',
    'with', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'this', 'that', 'these', 'those', 'it', 'its', 'from', 'by', 'at',
    'which', 'who', 'whom', 'whose', 'what', 'when', 'where', 'why', 'how',
    'not', 'no', 'nor', 'so', 'than', 'too', 'very', 'can', 'could',
    'should', 'would', 'may', 'might', 'must', 'shall', 'will', 'do',
    'does', 'did', 'has', 'have', 'had', 'having', 'if', 'then', 'else',
    'about', 'into', 'over', 'under', 'again', 'also', 'such', 'only',
    'own', 'same', 'other', 'some', 'any', 'all', 'both', 'each', 'few',
    'more', 'most', 'between', 'through', 'during', 'before', 'after',
    'above', 'below', 'up', 'down', 'out', 'off', 'your', 'their',
    'there', 'here', 'them', 'they', 'we', 'you', 'he', 'she', 'him',
    'her', 'his', 'us', 'our', 'me', 'my', 'one', 'two', 'three',
    'md', 'index', 'overview', 'guide', 'introduction', 'topic',
    'content', 'section', 'chapter', 'part', 'class', 'type',
}

# Chinese dictionary for forward maximum matching (FMM).
# Curated from this knowledge base's actual domain vocabulary (mind-body
# healing, Buddhism/Daoism, clinical psychology, meditation, bio-science).
# Using a real lexicon avoids the bigram-boundary noise (e.g. 治疗→疗干/物治)
# that made v1's relation fields read as gibberish. Unmatched CJK runs are
# discarded — we prefer fewer, clean terms over many noisy ones.
CN_DICT = """
禅宗 佛教 佛法 佛学 菩萨 菩提 般若 智慧 空性 缘起 中观 唯识 如来 藏传
止观 内观 观想 冥想 正念 静坐 坐禅 参禅 话头 默照 念佛 念诵 陀罗尼 真言
坛城 曼陀罗 结界 加持 传承 上师 喇嘛 堪布 阿闍黎 戒律 菩萨戒 别解脱
道家 道教 道德经 庄子 老子 内丹 炼气 气功 太极 八段丹 五行 阴阳 无为
瑜伽 瑜伽经 体式 调息 帕坦伽利 昆达里尼 哈他瑜伽 胜王瑜伽
心理学 心理治疗 精神分析 认知行为 行为主义 人本主义 积极心理学 进化心理学
发展心理学 社会心理学 人格心理学 临床心理学 神经心理学 变态心理学
抑郁 焦虑 恐惧 强迫 创伤 压力 倦怠 自杀 哀伤 悲伤 愤怒 羞耻 内疚 嫉妒
自恋 依恋 人格 边缘型 自恋型 反社会 解离 闪回 应激 适应
创伤后应激 障碍 失眠 嗜睡 梦魇 昼夜节律
治疗 干预 疗法 评估 诊断 症状 共病 复发 缓解 预后 循证 随机对照 元分析
认知重构 暴露 反应预防 系统脱敏 眼动脱敏 再加工 慈心冥想 正念减压
正念认知 接纳承诺 辩证行为 人际关系 团体治疗 家庭治疗 叙事治疗
焦点解决 意义疗法 格式塔
冥想引导 呼吸 觉察 身体扫描 身体感受 情绪调节 自我安抚 容纳窗口
接地 充电 锚定 转介 危机干预 安全计划
神经科学 神经元 突触 神经可塑性 默认模式 前额叶 杏仁核 海马
皮质醇 肾上腺 交感神经 副交感 迷走神经 肠脑轴 微生物组 炎症 免疫
睡眠 深睡眠 快速眼动 褪黑素 生物钟 断食 间歇性断食 营养 维生素
运动 有氧 力量 高强度间歇 血压 心率 变异性
呼吸法 桶式呼吸 腹式呼吸 4-7-8呼吸 箱式呼吸 威姆霍夫
成瘾 物质成瘾 行为成瘾 戒断 渴求 复发预防
亲密关系 婚姻 亲子 依恋类型 沟通 冲突 谈判 非暴力沟通 共情 倾听
自尊 自信 自我价值 自我关怀 自悲 韧性 心力 内核
拖延 习惯 心流 专注 效率 执行力 目标 意义 价值观
死亡 临终 哀伤辅导 丧亲 存在主义 意义建构
艺术疗愈 音乐疗愈 绘画 舞蹈 戏剧 表达性艺术
芭蕾 古典乐 书法 茶道 花道
睡眠卫生 失眠认知行为 睡眠限制 刺激控制
胎息 周天 经络 腧穴 针灸 推拿 黄帝内经 伤寒论 本草
""".split()

# Single CJK chars that, when they constitute an *unmatched* run, are dropped.
CN_STOPCHAR = set('的了是在我有和就不人都一个上也很到说要去你会着没有看好自己这那他她它们与及或而但所以因为如果虽然然后还又再把被让吗呢吧啊呀哦嗯么哪每各另其之之以以及并并且或者但是然而则即就是为为了地得过将可以使得对于关于通过尽管无论只要只有除非')


# --------------------------------------------------------------------------- #
# File discovery & text extraction
# --------------------------------------------------------------------------- #

def should_skip(path: Path) -> bool:
    for part in path.relative_to(ROOT).parts:
        if part in EXCLUDE_DIRS or part.startswith('.'):
            return True
    return False


def split_frontmatter(content: str):
    """Return (frontmatter_str, body_str). frontmatter_str excludes the --- fences."""
    if not content.lstrip().startswith('---'):
        return '', content
    end = content.find('\n---', 3)
    if end == -1:
        return '', content
    # +3 to skip past the closing --- line start; account for newline
    fm = content[3:end].lstrip('\n')
    # find where the closing fence line ends
    nl = content.find('\n', end + 1)
    body = content[nl + 1:] if nl != -1 else ''
    return fm, body


def extract_semantic_text(filepath: Path) -> str:
    """Pull out the semantically densest text: title + H1 + all H2 + body head."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception:
        return ''
    _, body = split_frontmatter(content)
    # Keep headings (they're topic-dense) but strip markup + blockquotes early on
    # because blockquotes are often editorial notes, not topical content.
    lines = body.split('\n')
    headings = []
    body_chars = []
    char_budget = 500
    for ln in lines:
        stripped = ln.strip()
        if stripped.startswith('#'):
            # heading text without the leading #'s
            headings.append(re.sub(r'^#+\s*', '', stripped))
        if char_budget > 0:
            body_chars.append(stripped)
            char_budget -= len(stripped)
    return ' \n '.join(headings) + ' \n ' + ' '.join(body_chars)


# --------------------------------------------------------------------------- #
# Tokenization
# --------------------------------------------------------------------------- #

_CN_CHAR_RE = re.compile(r'[\u4e00-\u9fff]')
_EN_WORD_RE = re.compile(r'[a-zA-Z][a-zA-Z\-]{1,30}')

# Build a max-length-indexed matcher for forward maximum matching.
_CN_DICT = set(w for w in CN_DICT if w)
_CN_MAXLEN = max((len(w) for w in _CN_DICT), default=1)


def _extract_cjk_words(text: str) -> Counter:
    """Forward Maximum Matching over CJK runs using CN_DICT.

    Unmatched CJK runs are discarded. This trades recall for precision: the
    old char-bigram approach produced nonsense boundary fragments
    (治疗→疗干/物治/群治) that dominated cosine similarity and linked
    unrelated 'treatment' docs. FMM with a domain lexicon yields clean
    domain terms.
    """
    counts = Counter()
    out = []
    for ch in text:
        if _CN_CHAR_RE.match(ch):
            out.append(ch)
        else:
            out.append('\x00')  # non-CJK sentinel breaks runs
    s = ''.join(out)
    # split into maximal CJK runs
    for run in re.split(r'\x00+', s):
        if not run:
            continue
        i = 0
        n = len(run)
        while i < n:
            matched = False
            for L in range(min(_CN_MAXLEN, n - i), 1, -1):
                cand = run[i:i + L]
                if cand in _CN_DICT:
                    counts[cand] += 1
                    i += L
                    matched = True
                    break
            if not matched:
                i += 1  # skip unmatched char (drop it, don't emit)
    return counts


def tokenize(text: str) -> Counter:
    """Tokenize bilingual text → Counter of terms.

    Chinese: forward maximum matching against CN_DICT (clean domain terms).
    English: lowercased words ≥2 letters, minus stopwords.
    """
    counts = Counter()
    for w in _EN_WORD_RE.findall(text):
        wl = w.lower()
        if wl in EN_STOP or len(wl) < 2:
            continue
        counts[wl] += 1
    counts.update(_extract_cjk_words(text))
    return counts


# --------------------------------------------------------------------------- #
# TF-IDF + cosine
# --------------------------------------------------------------------------- #

def build_corpus():
    """Discover files, tokenize, compute document frequency & TF-IDF vectors."""
    docs = []  # list of dict(path, rel, pillar, counts)
    df = Counter()  # document frequency per term

    for md in sorted(ROOT.rglob('*.md')):
        if should_skip(md):
            continue
        try:
            content = md.read_text(encoding='utf-8')
        except Exception:
            continue
        if not content.lstrip().startswith('---'):
            continue  # no frontmatter → not a content doc, skip
        text = extract_semantic_text(md)
        counts = tokenize(text)
        if not counts:
            continue
        parts = md.relative_to(ROOT).parts
        docs.append({
            'path': md,
            'rel': str(md.relative_to(ROOT)),
            'pillar': parts[0] if parts else '',
            'counts': counts,
        })
        for term in counts:
            df[term] += 1

    N = len(docs)
    # Domain-stopword gate. Two layers:
    #  (a) MANUAL_CLINICAL_STOP — clinical-skeleton boilerplate that DF-gating
    #      misses because each word sits at 15-24% DF (below the 25% gate) yet
    #      every *_Overview.md / *_Clinical_Management.md shares the exact same
    #      skeleton ("评估/诊断/治疗/循证/干预/症状/预后/共病/适应/康复…"),
    #      causing unrelated topics (necrophilia ↔ lower-back-pain) to cluster.
    #      These are zeroed explicitly.
    #  (b) DF gate — any term in > MAX_DF_RATIO of docs (心理学/治疗/焦虑 at
    #      31-56%) is auto-zeroed.
    MANUAL_CLINICAL_STOP = {
        '评估', '诊断', '治疗', '干预', '循证', '症状', '预后', '共病',
        '适应', '康复', '缓解', '复发', '病因', '病理', '机制', '量表',
        '筛查', '转介', '疗效', '适应症', '禁忌症', '不良反应',
        '临床应用', '临床管理', '质量控制', '实践指南', '参考文献',
        '目标', '价值观', '传承', '心理学', '心理治疗', '心理调节',
        '心理影响', '心理适应', '心理康复', '心理愈合', '心理调节',
    }
    MAX_DF_RATIO = 0.25
    idf = {}
    domain_stop = set()
    for term, freq in df.items():
        if freq / N > MAX_DF_RATIO or term in MANUAL_CLINICAL_STOP:
            idf[term] = 0.0
            domain_stop.add(term)
        else:
            # smoothed idf; terms in all docs → ~0 weight (the desired effect)
            idf[term] = math.log((N + 1) / (freq + 1)) + 1.0
    print(f"  domain stopwords (manual+DF>{int(MAX_DF_RATIO*100)}%): {len(domain_stop)} terms zeroed")

    # TF-IDF vectors + precomputed L2 norms
    for d in docs:
        vec = {}
        for term, c in d['counts'].items():
            tf = 1.0 + math.log(c)  # sublinear tf
            vec[term] = tf * idf.get(term, 0.0)
        # drop zero-weight terms (ubiquitous words)
        vec = {t: w for t, w in vec.items() if w > 0}
        norm = math.sqrt(sum(w * w for w in vec.values())) or 1.0
        d['vec'] = vec
        d['norm'] = norm
        # top weighted terms for guardrail overlap check
        d['top'] = {t for t, _ in sorted(vec.items(), key=lambda kv: -kv[1])[:TOP_TERM_OVERLAP]}

    return docs, idf


def cosine(a, b):
    """Cosine similarity between two precomputed doc dicts."""
    # iterate over the smaller vector
    if len(a['vec']) > len(b['vec']):
        a, b = b, a
    dot = 0.0
    for t, w in a['vec'].items():
        wb = b['vec'].get(t)
        if wb:
            dot += w * wb
    return dot / (a['norm'] * b['norm'])


def shared_top_terms(a, b, k=RELATION_TERMS):
    """The k highest-IDF terms present in both docs → meaningful relation label."""
    shared = set(a['vec'].keys()) & set(b['vec'].keys())
    if not shared:
        return []
    # weight by combined TF-IDF weight as a proxy for joint importance
    ranked = sorted(shared, key=lambda t: -(a['vec'][t] + b['vec'][t]))
    return ranked[:k]


# --------------------------------------------------------------------------- #
# Frontmatter rewrite (pyyaml-free, block-aware, overwrite-capable)
# --------------------------------------------------------------------------- #

def rewrite_cross_refs(content: str, refs) -> str:
    """Overwrite the cross_refs block in frontmatter. `refs` is a list of
    (rel_path, relation_list) tuples. Returns new content; unchanged on failure."""
    if not content.lstrip().startswith('---'):
        return content
    end = content.find('\n---', 3)
    if end == -1:
        return content
    head = content[:end]
    tail_start = content.find('\n', end + 1)
    tail = content[tail_start:] if tail_start != -1 else ''

    # Build the new cross_refs block
    if refs:
        lines = ['cross_refs:']
        for rel, relation in refs:
            rel_str = '/'.join(relation) if relation else ''
            lines.append(f'  - path: "{rel}"')
            lines.append(f'    relation: "{rel_str}"')
        new_block = '\n'.join(lines)
    else:
        new_block = 'cross_refs: []'

    # Strip an existing cross_refs block from head.
    # head begins with the opening '---' fence (content[:end] captures from
    # the start up to the closing '\n---'). We split into lines, drop the
    # opening fence (we re-add it), drop any old cross_refs block, then
    # rebuild the frontmatter body cleanly.
    fm_lines = head.split('\n')
    # remove the leading '---' fence line(s); we re-emit exactly one.
    while fm_lines and fm_lines[0].strip() == '---':
        fm_lines.pop(0)
    out = []
    skipping = False
    for ln in fm_lines:
        if skipping:
            # end of cross_refs block: a new top-level key or a fence
            if re.match(r'^[A-Za-z_][A-Za-z0-9_]*:', ln) or ln.strip() == '---':
                skipping = False
                out.append(ln)
            else:
                continue  # drop continuation lines of old cross_refs
        else:
            if re.match(r'^cross_refs\s*:', ln):
                skipping = True
                continue
            out.append(ln)
    fm_body = '\n'.join(out).strip()
    new_content = '---\n' + fm_body + '\n' + new_block + '\n---' + tail
    return new_content


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main():
    args = sys.argv[1:]
    dry_run = '--apply' not in args
    verbose = '--verbose' in args or '-v' in args
    sample_n = 10
    for i, a in enumerate(args):
        if a == '--sample' and i + 1 < len(args):
            try:
                sample_n = int(args[i + 1])
            except ValueError:
                pass

    print("Building corpus (tokenize + TF-IDF)...")
    docs, idf = build_corpus()
    print(f"Indexed {len(docs)} content documents, {len(idf)} unique terms.")

    # Group by pillar for cross-pillar matching
    by_pillar = defaultdict(list)
    for d in docs:
        by_pillar[d['pillar']].append(d)

    print("Computing cross-pillar references...")
    matches = {}  # rel -> list of (sim, other_rel, relation_terms)
    for d in docs:
        cands = []
        my_pillar = d['pillar']
        for pillar, plist in by_pillar.items():
            if pillar == my_pillar:
                continue
            # Skip mirror-group pillars (06 mirrors 02/03): cross-links there
            # are near-duplicate self-references (md5-identical files), not
            # meaningful cross-pillar discovery.
            if any(my_pillar in g and pillar in g for g in MIRROR_GROUPS):
                continue
            for other in plist:
                # guardrail #1: must share ≥ MIN_SHARED_TERMS top-weighted
                # terms — a single shared word (意义/智慧/恐惧) is too weak to
                # establish a genuine cross-domain relationship.
                shared = d['top'] & other['top']
                if len(shared) < MIN_SHARED_TERMS:
                    continue
                sim = cosine(d, other)
                if sim >= SIM_THRESHOLD:
                    rel = shared_top_terms(d, other)
                    # guardrail #2: if every shared term is a domain stopword
                    # (zeroed IDF, e.g. 治疗/循证/心理学), the link rests on
                    # boilerplate skeleton only — reject it.
                    if not rel:
                        continue
                    cands.append((sim, other['rel'], rel))
        cands.sort(key=lambda x: -x[0])
        matches[d['rel']] = cands[:MAX_REFS]

    has_refs = sum(1 for m in matches.values() if m)
    print(f"\n=== Cross-Reference Generation (v2 TF-IDF) Summary ===")
    print(f"Total docs:        {len(docs)}")
    print(f"With cross-refs:   {has_refs}")
    print(f"Without (no match):{len(docs) - has_refs}")
    print(f"Threshold:         cosine >= {SIM_THRESHOLD}, top-{MAX_REFS}")

    if dry_run:
        # Print sample matchups to validate semantic quality
        print(f"\n--- {sample_n} sample matchups (semantic validation) ---")
        # Prefer diverse, high-signal samples
        sample_keys = sorted(
            [k for k, m in matches.items() if m],
            key=lambda k: -(matches[k][0][0] if matches[k] else 0)
        )[:sample_n]
        for k in sample_keys:
            print(f"\n📄 {k}")
            for sim, other_rel, rel_terms in matches[k]:
                print(f"   → {other_rel}  (cos={sim:.3f}, rel={ '/'.join(rel_terms) })")
        print("\n[DRY RUN] No files modified. Re-run with --apply to write.")
        return

    # APPLY
    written = 0
    for d in docs:
        refs = matches.get(d['rel'], [])
        try:
            content = d['path'].read_text(encoding='utf-8')
        except Exception:
            continue
        new = rewrite_cross_refs(content, [(r, t) for _, r, t in refs])
        if new != content:
            d['path'].write_text(new, encoding='utf-8')
            written += 1
        if verbose:
            print(f"  {'✓' if refs else '·'} {d['rel']} → {len(refs)} refs")
    print(f"\n✅ Wrote cross_refs to {written} files (overwriting old blocks).")


if __name__ == '__main__':
    main()
