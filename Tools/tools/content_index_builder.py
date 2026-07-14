#!/usr/bin/env python3
"""生成 Knowledge Base Explorer 所需的全库内容索引。"""

from __future__ import annotations

import json
import math
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

SCRIPT_DIR = Path(__file__).parent.resolve()
TOOLS_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = TOOLS_DIR.parent.resolve()
DATA_DIR = TOOLS_DIR / "data"
OUTPUT_FILE = DATA_DIR / "content_index.json"
WORD_COUNT_FILE = DATA_DIR / "word_count_history.json"
QUALITY_FILE = DATA_DIR / "quality_report.json"

TEXT_EXTENSIONS = {
    ".md",
    ".json",
    ".py",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".txt",
    ".yml",
    ".yaml",
}

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    ".qoder",
    ".trae",
}

EXCLUDED_FILES = {
    OUTPUT_FILE.name,
}

PILLAR_LABELS = {
    ".": "Root 根目录",
    "01-智慧传统": "Wisdom Traditions 智慧传承",
    "02-心智心理": "Mind & Psychology 心智与心理学",
    "03-生命科学": "Bio-Science & Medicine 生命科学与生物医学",
    "04-人文艺术": "Humanities & Arts 人文与艺术疗愈",
    "05-实践成长": "Praxis & Growth 实践与个人增长",
    "06-临床专题": "Clinical Topics 临床专题",
    "07-行业观察": "Industry Insights 行业观察",
    "Tools": "Tools & Operations 工具与治理",
}

ROLE_ORDER = [
    "index",
    "readme",
    "overview",
    "framework",
    "guide",
    "template",
    "system_design",
    "taxonomy",
    "case_library",
    "tool",
    "web_asset",
    "data",
    "content",
]

ROLE_LABELS = {
    "index": "导航索引",
    "readme": "说明文档",
    "overview": "概览文档",
    "framework": "方法框架",
    "guide": "指南手册",
    "template": "模板清单",
    "system_design": "系统设计",
    "taxonomy": "分类体系",
    "case_library": "案例资料",
    "tool": "工具脚本",
    "web_asset": "前端资产",
    "data": "结构化数据",
    "content": "正文内容",
}

PROTECTED_EXTENSIONS = {
    ".json",
    ".py",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".yml",
    ".yaml",
}

SAFE_ASSET_LABELS = {
    ".json": "JSON 结构化数据",
    ".py": "Python 工具脚本",
    ".html": "HTML 页面资源",
    ".css": "CSS 样式资源",
    ".js": "JavaScript 交互脚本",
    ".ts": "TypeScript 交互脚本",
    ".yml": "YAML 配置资源",
    ".yaml": "YAML 配置资源",
}


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def slug_to_title(stem: str) -> str:
    cleaned = re.sub(r"[_-]+", " ", stem).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned or stem


def clean_text(text: str) -> str:
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[>*\-+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def summarize_roles(roles: List[str]) -> str:
    labels = [ROLE_LABELS[role] for role in roles if role in ROLE_LABELS]
    unique_labels = list(dict.fromkeys(labels))
    return " / ".join(unique_labels[:2]) or ROLE_LABELS["content"]


def summarize_structured_content(content: str) -> str:
    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        return "结构化内容格式异常，页面仅展示安全摘要与元数据"

    if isinstance(payload, dict):
        return f"顶层对象，共 {len(payload)} 个键"
    if isinstance(payload, list):
        return f"顶层数组，共 {len(payload)} 项"
    return f"顶层值类型：{type(payload).__name__}"


def extract_excerpt(content: str, ext: str, relative_path: Path, roles: List[str], line_count: int) -> str:
    if ext == ".md":
        chunks = [segment.strip() for segment in re.split(r"\n\s*\n", content) if segment.strip()]
        for chunk in chunks:
            if chunk.startswith("#") or chunk.startswith("---"):
                continue
            cleaned = clean_text(chunk)
            if len(cleaned) >= 24:
                return cleaned[:220]
        return clean_text(content[:220])

    if ext == ".json":
        return (
            f"{SAFE_ASSET_LABELS[ext]} · {summarize_roles(roles)} · {line_count} 行 · "
            f"{summarize_structured_content(content)}。页面默认隐藏原始值，仅展示安全摘要与元数据。"
        )

    if ext in PROTECTED_EXTENSIONS:
        asset_label = SAFE_ASSET_LABELS.get(ext, f"{relative_path.suffix.upper()} 受保护资产")
        return (
            f"{asset_label} · {summarize_roles(roles)} · {line_count} 行 · "
            "页面默认隐藏源码与原始配置，仅展示安全摘要与元数据。"
        )

    cleaned = clean_text(content[:220])
    if cleaned:
        return cleaned[:220]
    return f"{relative_path.name} · {line_count} 行文本资产"


def extract_markdown_outline(content: str) -> List[Dict[str, str]]:
    outline: List[Dict[str, str]] = []
    for line in content.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        outline.append({
            "level": len(match.group(1)),
            "text": match.group(2).strip(),
        })
        if len(outline) >= 12:
            break
    return outline


def detect_roles(path: Path, ext: str) -> List[str]:
    name_lower = path.name.lower()
    stem_lower = path.stem.lower()
    roles: List[str] = []

    if name_lower == "index.md":
        roles.append("index")
    if name_lower.startswith("readme"):
        roles.append("readme")
    if "overview" in stem_lower:
        roles.append("overview")
    if "framework" in stem_lower:
        roles.append("framework")
    if any(token in stem_lower for token in ["guide", "handbook", "playbook", "manual"]):
        roles.append("guide")
    if any(token in stem_lower for token in ["template", "templates", "checklist"]):
        roles.append("template")
    if "system" in stem_lower or "design" in stem_lower:
        roles.append("system_design")
    if "taxonomy" in stem_lower:
        roles.append("taxonomy")
    if "case" in stem_lower or "library" in stem_lower:
        roles.append("case_library")
    if ext == ".py":
        roles.append("tool")
    if ext in {".html", ".css", ".js", ".ts"}:
        roles.append("web_asset")
    if ext == ".json":
        roles.append("data")
    if ext == ".md" and not roles:
        roles.append("content")
    return list(dict.fromkeys(roles or ["content"]))


def primary_role(roles: List[str]) -> str:
    for role in ROLE_ORDER:
        if role in roles:
            return role
    return roles[0] if roles else "content"


def extract_tags(relative_path: Path, title: str) -> List[str]:
    raw_tokens = list(relative_path.parts[:-1]) + re.split(r"[_\-/\s]+", relative_path.stem) + re.split(r"[_\-/\s]+", title)
    tags: List[str] = []
    seen = set()
    for token in raw_tokens:
        token = token.strip()
        if not token or token.isdigit() or len(token) < 3:
            continue
        normalized = token.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        tags.append(token)
        if len(tags) >= 12:
            break
    return tags


def build_entry(file_path: Path) -> Dict:
    relative_path = file_path.relative_to(PROJECT_ROOT)
    relative_str = relative_path.as_posix()
    ext = file_path.suffix.lower()
    content = file_path.read_text(encoding="utf-8")
    stat = file_path.stat()
    top_dir = relative_path.parts[0] if len(relative_path.parts) > 1 else "."
    title = slug_to_title(file_path.stem)
    outline: List[Dict[str, str]] = []

    if ext == ".md":
        first_heading = re.search(r"^#\s+(.+?)\s*$", content, flags=re.MULTILINE)
        if first_heading:
            title = first_heading.group(1).strip()
        outline = extract_markdown_outline(content)

    roles = detect_roles(relative_path, ext)
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", content))
    english_words = len(re.findall(r"[A-Za-z]+", content))
    line_count = content.count("\n") + (0 if not content or content.endswith("\n") else 1)
    excerpt = extract_excerpt(content, ext, relative_path, roles, line_count)
    reading_minutes = max(1, math.ceil((chinese_chars / 420) + (english_words / 230)))

    signals = {
        "navigation": any(role in roles for role in ["index", "readme", "overview"]),
        "structured": ext == ".json" or "taxonomy" in roles,
        "tooling": top_dir == "Tools" or ext in {".py", ".html", ".css", ".js", ".ts"},
        "methodology": any(role in roles for role in ["framework", "guide", "system_design"]),
    }

    return {
        "path": relative_str,
        "name": file_path.name,
        "stem": file_path.stem,
        "title": title,
        "excerpt": excerpt,
        "ext": ext or "(none)",
        "top_dir": top_dir,
        "top_dir_label": PILLAR_LABELS.get(top_dir, top_dir),
        "directory": relative_path.parent.as_posix() if relative_path.parent.as_posix() != "." else ".",
        "depth": max(0, len(relative_path.parts) - 1),
        "size": stat.st_size,
        "lines": line_count,
        "chars": len(content),
        "reading_minutes": reading_minutes,
        "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
        "modified_ts": int(stat.st_mtime),
        "preview_policy": "metadata_only" if ext in PROTECTED_EXTENSIONS else "full_text",
        "roles": roles,
        "primary_role": primary_role(roles),
        "tags": extract_tags(relative_path, title),
        "outline": outline,
        "signals": signals,
    }


def aggregate_directories(files: List[Dict]) -> List[Dict]:
    buckets: Dict[str, Dict] = {}

    def ensure_bucket(path: str, top_dir: str) -> Dict:
        if path not in buckets:
            path_obj = Path(path) if path != "." else Path(".")
            buckets[path] = {
                "path": path,
                "name": path_obj.name if path != "." else ".",
                "top_dir": top_dir,
                "depth": 0 if path == "." else len(Path(path).parts),
                "file_count": 0,
                "total_chars": 0,
                "total_bytes": 0,
                "latest_modified_ts": 0,
            }
        return buckets[path]

    for file in files:
        directory = file["directory"]
        ancestors = ["."]
        if directory != ".":
            segments = directory.split("/")
            current_parts: List[str] = []
            for segment in segments:
                current_parts.append(segment)
                ancestors.append("/".join(current_parts))
        for ancestor in dict.fromkeys(ancestors):
            bucket = ensure_bucket(ancestor, file["top_dir"])
            bucket["file_count"] += 1
            bucket["total_chars"] += file["chars"]
            bucket["total_bytes"] += file["size"]
            bucket["latest_modified_ts"] = max(bucket["latest_modified_ts"], file["modified_ts"])

    directories = list(buckets.values())
    directories.sort(key=lambda item: (-item["file_count"], item["path"]))
    return directories


def scan_files() -> List[Dict]:
    files: List[Dict] = []
    for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS and not name.startswith(".")]
        current_dir = Path(dirpath)
        for filename in filenames:
            if filename in EXCLUDED_FILES or filename.startswith("."):
                continue
            file_path = current_dir / filename
            if file_path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            try:
                files.append(build_entry(file_path))
            except UnicodeDecodeError:
                continue
    files.sort(key=lambda item: item["path"])
    return files


def build_stats(files: List[Dict]) -> Dict:
    by_ext = Counter(file["ext"] for file in files)
    by_top_dir = Counter(file["top_dir"] for file in files)
    by_role = Counter(file["primary_role"] for file in files)
    total_chars = sum(file["chars"] for file in files)
    total_lines = sum(file["lines"] for file in files)

    word_history = load_json(WORD_COUNT_FILE) or []
    latest_word_count = word_history[-1] if word_history else None
    quality_report = load_json(QUALITY_FILE)

    return {
        "total_files": len(files),
        "total_directories": len({file["directory"] for file in files}),
        "total_chars": total_chars,
        "total_lines": total_lines,
        "by_ext": dict(sorted(by_ext.items(), key=lambda item: (-item[1], item[0]))),
        "by_top_dir": dict(sorted(by_top_dir.items(), key=lambda item: item[0])),
        "by_role": dict(sorted(by_role.items(), key=lambda item: (-item[1], item[0]))),
        "latest_word_count": latest_word_count,
        "quality_snapshot": quality_report,
    }


def build_payload() -> Dict:
    files = scan_files()
    directories = aggregate_directories(files)
    stats = build_stats(files)
    latest_files = sorted(files, key=lambda item: item["modified_ts"], reverse=True)[:16]
    pillars = []
    for top_dir, count in stats["by_top_dir"].items():
        chars = sum(file["chars"] for file in files if file["top_dir"] == top_dir)
        pillars.append({
            "key": top_dir,
            "label": PILLAR_LABELS.get(top_dir, top_dir),
            "file_count": count,
            "char_count": chars,
        })

    return {
        "meta": {
            "project": "Peace Lab Database",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "source_root": ".",
            "content_fetch_base": "../../",
        },
        "stats": stats,
        "pillars": pillars,
        "directories": directories[:240],
        "latest_files": latest_files,
        "files": files,
    }


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Indexed {payload['stats']['total_files']} files -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
