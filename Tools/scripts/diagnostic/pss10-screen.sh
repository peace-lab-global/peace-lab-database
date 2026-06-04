#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# PSS-10 压力知觉量表 | Perceived Stress Scale (10-item)
# Part of Peace Lab Database diagnostic toolkit
# =============================================================================

# --- ANSI Colors ---
BOLD='\033[1m'
DIM='\033[2m'
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/../../logs/diagnostic"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${LOG_DIR}/pss10_${TIMESTAMP}.log"

# --- Questions (Chinese) ---
# Format: "question_text|is_reverse"
QUESTIONS=(
  "由于发生了意想不到的事情而感到不安？|0"
  "感到无法控制生活中重要的事情？|0"
  "感到紧张和有压力？|0"
  "成功地处理了恼人的生活麻烦？|1"
  "有效地应对了生活中重要的变化？|1"
  "对自己处理个人问题的能力感到自信？|1"
  "觉得事情按自己的意愿进行？|1"
  "发现自己无法处理所有必须做的事情？|0"
  "能够控制生活中的烦恼？|1"
  "觉得困难堆积得太多以至于无法克服？|0"
)

REVERSE_MAP=(4 3 2 1 0)  # 0->4, 1->3, 2->2, 3->1, 4->0

# --- Helper: log to file ---
log() {
  echo "$1" >> "$LOG_FILE"
}

# --- Header ---
clear
echo ""
echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║  PSS-10 压力知觉量表 | Perceived Stress Scale              ║${NC}"
echo -e "${CYAN}${BOLD}║  Peace Lab Database · Diagnostic Screening                  ║${NC}"
echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${DIM}本工具基于 Cohen, Kamarck & Mermelstein (1983) 压力知觉量表。${NC}"
echo -e "${DIM}在过去一个月中，您感到以下情况的频率如何？${NC}"
echo ""
echo -e "${YELLOW}评分标准:${NC}"
echo -e "  ${BOLD}0${NC} = 从不    ${BOLD}1${NC} = 偶尔    ${BOLD}2${NC} = 有时    ${BOLD}3${NC} = 时常    ${BOLD}4${NC} = 总是"
echo ""
echo -e "${DIM}标注 (R) 的题目为反向计分项。${NC}"
echo -e "${DIM}──────────────────────────────────────────────────────────────${NC}"
echo ""

# --- Collect Responses ---
total=0
answers=()
for i in "${!QUESTIONS[@]}"; do
  IFS='|' read -r q_text q_reverse <<< "${QUESTIONS[$i]}"
  q_num=$((i + 1))

  if [[ "$q_reverse" == "1" ]]; then
    marker="${MAGENTA}(R)${NC}"
  else
    marker=""
  fi

  while true; do
    echo -ne "${BLUE}${BOLD}Q${q_num}${NC} ${marker} ${q_text} "
    read -rp "[0-4]: " answer
    if [[ "$answer" =~ ^[0-4]$ ]]; then
      break
    else
      echo -e "  ${RED}请输入 0 到 4 之间的数字。${NC}"
    fi
  done

  if [[ "$q_reverse" == "1" ]]; then
    score=${REVERSE_MAP[$answer]}
  else
    score=$answer
  fi

  total=$((total + score))
  answers+=("$answer")
  echo ""
done

# --- Score Interpretation ---
if   (( total <= 13 )); then
  level="低压力 (Low stress)"
  color="$GREEN"
  emoji="🟢"
elif (( total <= 26 )); then
  level="中等压力 (Moderate stress)"
  color="$YELLOW"
  emoji="🟡"
else
  level="高压力 (High perceived stress)"
  color="$RED"
  emoji="🔴"
fi

# --- Results Display ---
echo -e "${DIM}══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}${BOLD}【评估结果 / Results】${NC}"
echo ""
echo -e "  总分 Total Score: ${BOLD}${color}${total} / 40${NC}"
echo -e "  压力等级 Level:   ${color}${emoji} ${level}${NC}"
echo ""

# --- Stress Management Recommendations ---
echo -e "${CYAN}${BOLD}【建议 / Recommendations】${NC}"
echo ""
if (( total <= 13 )); then
  echo -e "  ${GREEN}您的压力水平较低，状态良好。建议：${NC}"
  echo -e "  • 继续保持健康的生活方式和积极的心态"
  echo -e "  • 定期进行自我觉察，关注身心变化"
  echo -e "  • 维持良好的社交关系和兴趣爱好"
elif (( total <= 26 )); then
  echo -e "  ${YELLOW}您正经历中等程度的压力。建议：${NC}"
  echo -e "  • 规律运动（如散步、瑜伽、太极等）"
  echo -e "  • 练习深呼吸、冥想或正念放松"
  echo -e "  • 与信任的人倾诉，寻求社会支持"
  echo -e "  • 合理安排时间，减少不必要的负担"
  echo -e "  • 如持续感到不适，建议咨询专业心理健康服务"
else
  echo -e "  ${RED}您的压力水平较高，请重视身心健康。建议：${NC}"
  echo -e "  • 尽快寻求专业心理咨询或医疗支持"
  echo -e "  • 联系信任的家人或朋友，不要独自承受"
  echo -e "  • 减少压力源，优先处理最重要的事务"
  echo -e "  • 保证充足睡眠和基本自我照顾"
  echo -e "  • 如有危机情况，请拨打心理援助热线："
  echo -e "    - 全国心理援助热线: ${BOLD}400-161-9995${NC}"
  echo -e "    - 北京心理危机研究与干预中心: ${BOLD}010-82951332${NC}"
  echo -e "    - 生命热线: ${BOLD}400-821-1215${NC}"
fi
echo ""

# --- Disclaimer ---
echo -e "${DIM}──────────────────────────────────────────────────────────────${NC}"
echo -e "${DIM}${BOLD}免责声明 / Disclaimer:${NC}"
echo -e "${DIM}本筛查工具仅供教育和自我觉察用途，不能替代专业的医学诊断。${NC}"
echo -e "${DIM}如您正在经历严重的心理困扰，请咨询合格的心理健康专业人员。${NC}"
echo -e "${DIM}This screening tool is for educational purposes only and is not${NC}"
echo -e "${DIM}a substitute for professional medical diagnosis or treatment.${NC}"
echo -e "${DIM}──────────────────────────────────────────────────────────────${NC}"
echo ""

# --- Save Log ---
{
  echo "============================================"
  echo "PSS-10 Screening Results"
  echo "Peace Lab Database"
  echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "============================================"
  echo ""
  for i in "${!QUESTIONS[@]}"; do
    IFS='|' read -r q_text q_reverse <<< "${QUESTIONS[$i]}"
    q_num=$((i + 1))
    ans=${answers[$i]}
    if [[ "$q_reverse" == "1" ]]; then
      score=${REVERSE_MAP[$ans]}
      echo "Q${q_num} [R]: raw=${ans} reversed=${score}  ${q_text}"
    else
      echo "Q${q_num}:    raw=${ans} score=${ans}  ${q_text}"
    fi
  done
  echo ""
  echo "---"
  echo "Total Score: ${total} / 40"
  echo "Level: ${level}"
  echo "============================================"
} > "$LOG_FILE"

echo -e "${DIM}结果已保存至: ${LOG_FILE}${NC}"
echo -e "${DIM}Results saved to: ${LOG_FILE}${NC}"
echo ""
echo -e "${CYAN}感谢您使用 Peace Lab 压力知觉筛查工具。${NC}"
echo -e "${CYAN}Take care of yourself. 💚${NC}"
echo ""
