#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# PHQ-9 Depression Screening Tool
# Peace Lab Database — 乐和平实验室
# ============================================================================

# ANSI color codes
RED='\033[1;31m'
YELLOW='\033[1;33m'
GREEN='\033[1;32m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

# Log directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/../../logs/phq9"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${LOG_DIR}/phq9_${TIMESTAMP}.log"

# PHQ-9 questions in Chinese
QUESTIONS=(
  "做事时提不起劲或没有兴趣"
  "感到心情低落、沮丧或绝望"
  "入睡困难、睡不安稳或睡眠过多"
  "感觉疲倦或没有活力"
  "食欲不振或吃太多"
  "觉得自己很糟或很失败，或让自己或家人失望"
  "注意力难以集中"
  "动作或说话速度慢到别人可以察觉，或坐立不安"
  "有不如死掉或用某种方式伤害自己的念头"
)

# Function to validate input (0-3)
get_score() {
  local q_num=$1
  local q_text=$2
  local score
  while true; do
    echo -e "  ${CYAN}Q${q_num}${NC}：${BOLD}${q_text}${NC}"
    echo -e "     ${DIM}0=完全没有 | 1=好几天 | 2=一半以上的天数 | 3=几乎每天${NC}"
    read -rp "  你的评分 (0-3): " score
    if [[ "$score" =~ ^[0-3]$ ]]; then
      echo ""
      return "$score"
    fi
    echo -e "  ${RED}请输入 0 到 3 之间的数字 | Please enter a number between 0 and 3${NC}"
    echo ""
  done
}

# ─── Header ──────────────────────────────────────────────────────────────────
clear 2>/dev/null || true
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  PHQ-9 抑郁筛查工具 | PHQ-9 Depression Screening${NC}"
echo -e "${BLUE}  乐和平实验室 · Peace Lab Database${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${DIM}在过去两周里，你有多少时候受到以下问题困扰？${NC}"
echo -e "${DIM}Over the last 2 weeks, how often have you been bothered by the following?${NC}"
echo ""

# ─── Collect Answers ─────────────────────────────────────────────────────────
SCORES=()
TOTAL=0

for i in $(seq 0 8); do
  q_num=$((i + 1))
  get_score "$q_num" "${QUESTIONS[$i]}"
  score=$?
  SCORES+=("$score")
  TOTAL=$((TOTAL + score))
done

# ─── Determine Severity ─────────────────────────────────────────────────────
if (( TOTAL <= 4 )); then
  SEVERITY_CN="无/最小"
  SEVERITY_EN="Minimal"
  COLOR="$GREEN"
  LEVEL="minimal"
elif (( TOTAL <= 9 )); then
  SEVERITY_CN="轻度"
  SEVERITY_EN="Mild"
  COLOR="$GREEN"
  LEVEL="mild"
elif (( TOTAL <= 14 )); then
  SEVERITY_CN="中度"
  SEVERITY_EN="Moderate"
  COLOR="$YELLOW"
  LEVEL="moderate"
elif (( TOTAL <= 19 )); then
  SEVERITY_CN="中重度"
  SEVERITY_EN="Moderately Severe"
  COLOR="$RED"
  LEVEL="moderately_severe"
else
  SEVERITY_CN="重度"
  SEVERITY_EN="Severe"
  COLOR="$RED"
  LEVEL="severe"
fi

# ─── Output Results ──────────────────────────────────────────────────────────
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  筛查结果 | Screening Results${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Print individual scores
echo -e "  ${DIM}各题评分 | Individual Scores:${NC}"
for i in $(seq 0 8); do
  q_num=$((i + 1))
  printf "    Q%d: %d\n" "$q_num" "${SCORES[$i]}"
done
echo ""

echo -e "  ${BOLD}总分 | Total Score: ${COLOR}${TOTAL}${NC} / 27"
echo -e "  ${BOLD}严重程度 | Severity: ${COLOR}${SEVERITY_CN} (${SEVERITY_EN})${NC}"
echo ""

# ─── Crisis Warning (Q9 >= 1) ───────────────────────────────────────────────
if (( SCORES[8] >= 1 )); then
  echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${RED}  ⚠  危机警告 | CRISIS WARNING ⚠${NC}"
  echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  echo -e "  ${RED}${BOLD}你报告了自伤或自杀的想法。请立即寻求帮助。${NC}"
  echo -e "  ${RED}${BOLD}You reported thoughts of self-harm or suicide. Please seek help immediately.${NC}"
  echo ""
  echo -e "  ${BOLD}危机热线 | Crisis Hotlines:${NC}"
  echo -e "    🇨🇳 中国心理危机干预热线:  ${BOLD}400-161-9995${NC}"
  echo -e "    🇨🇳 北京心理危机研究与干预中心: ${BOLD}010-82951332${NC}"
  echo -e "    🇨🇳 生命热线 (24h):  ${BOLD}400-821-1215${NC}"
  echo -e "    🇺🇸 National Suicide Prevention Lifeline: ${BOLD}988${NC}"
  echo -e "    🌍 International Association for Suicide Prevention: ${BOLD}https://www.iasp.info/resources/Crisis_Centres/${NC}"
  echo ""
  echo -e "  ${RED}${BOLD}请记住：你并不孤单。帮助就在身边。${NC}"
  echo -e "  ${RED}${BOLD}Remember: You are not alone. Help is available.${NC}"
  echo ""
  echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
fi

# ─── Recommendations ─────────────────────────────────────────────────────────
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}  建议 | Recommendations${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

case "$LEVEL" in
  minimal)
    echo -e "  ${GREEN}• 症状轻微，无需特殊干预。保持健康的生活方式。${NC}"
    echo -e "  ${GREEN}• Symptoms are minimal. No special intervention needed.${NC}"
    echo -e "  ${GREEN}  Continue maintaining a healthy lifestyle.${NC}"
    ;;
  mild)
    echo -e "  ${GREEN}• 建议观察等待，2-4周后复查。可考虑心理咨询。${NC}"
    echo -e "  ${GREEN}• Watchful waiting recommended. Re-screen in 2-4 weeks.${NC}"
    echo -e "  ${GREEN}  Consider counseling or support groups.${NC}"
    ;;
  moderate)
    echo -e "  ${YELLOW}• 建议寻求专业心理咨询或心理治疗。${NC}"
    echo -e "  ${YELLOW}• Professional counseling or psychotherapy is recommended.${NC}"
    echo -e "  ${YELLOW}  Please consult a mental health professional.${NC}"
    ;;
  moderately_severe)
    echo -e "  ${RED}• 强烈建议立即寻求专业帮助，可能需要药物治疗和心理治疗。${NC}"
    echo -e "  ${RED}• Strongly recommend seeking professional help immediately.${NC}"
    echo -e "  ${RED}  Pharmacotherapy and/or psychotherapy may be needed.${NC}"
    ;;
  severe)
    echo -e "  ${RED}• 请立即寻求专业帮助！可能需要药物治疗和心理治疗。${NC}"
    echo -e "  ${RED}• Seek professional help IMMEDIATELY!${NC}"
    echo -e "  ${RED}  Pharmacotherapy and/or psychotherapy are likely needed.${NC}"
    ;;
esac

echo ""

# ─── Disclaimer ──────────────────────────────────────────────────────────────
echo -e "${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${DIM}  免责声明 | Disclaimer${NC}"
echo -e "${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${DIM}  本工具仅供筛查使用，不能替代专业临床诊断。${NC}"
echo -e "${DIM}  结果仅供参考，请咨询合格的医疗专业人员。${NC}"
echo -e "${DIM}  This tool is for screening only and does not replace${NC}"
echo -e "${DIM}  a professional clinical diagnosis. Results are for${NC}"
echo -e "${DIM}  reference only. Please consult a qualified healthcare${NC}"
echo -e "${DIM}  professional for a formal assessment.${NC}"
echo -e "${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ─── Save Log ────────────────────────────────────────────────────────────────
{
  echo "PHQ-9 Screening Results"
  echo "========================"
  echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
  echo ""
  echo "Scores:"
  for i in $(seq 0 8); do
    printf "  Q%d: %d — %s\n" "$((i+1))" "${SCORES[$i]}" "${QUESTIONS[$i]}"
  done
  echo ""
  echo "Total: ${TOTAL} / 27"
  echo "Severity: ${SEVERITY_CN} (${SEVERITY_EN})"
  if (( SCORES[8] >= 1 )); then
    echo "Q9 Flag: YES — Self-harm thoughts reported"
  fi
} > "$LOG_FILE"

echo -e "${DIM}  结果已保存 | Results saved to: ${LOG_FILE}${NC}"
echo ""
