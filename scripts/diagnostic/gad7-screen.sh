#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# GAD-7 广泛性焦虑障碍筛查 | Generalized Anxiety Disorder Screener
# Part of Peace Lab Database Diagnostic Tools
# ============================================================================

# ANSI Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Script directory and log path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/../../logs/diagnostic"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${LOG_DIR}/gad7_${TIMESTAMP}.log"

# Questions array
QUESTIONS=(
  "感觉紧张、焦虑或急切"
  "不能够停止或控制担忧"
  "对各种各样的事情担忧过多"
  "很难放松下来"
  "由于不安而无法静坐"
  "变得容易烦恼或急躁"
  "感到似乎将有可怕的事情发生"
)

# Score answers array
SCORES=()

# ---- Header ----
echo ""
echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║                                                                  ║${NC}"
echo -e "${CYAN}${BOLD}║   GAD-7 广泛性焦虑障碍筛查                                       ║${NC}"
echo -e "${CYAN}${BOLD}║   Generalized Anxiety Disorder Screener                           ║${NC}"
echo -e "${CYAN}${BOLD}║                                                                  ║${NC}"
echo -e "${CYAN}${BOLD}║   ${GREEN}Peace Lab Database — Diagnostic Tools${CYAN}                        ║${NC}"
echo -e "${CYAN}${BOLD}║                                                                  ║${NC}"
echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ---- Disclaimer ----
echo -e "${YELLOW}${BOLD}[免责声明 | DISCLAIMER]${NC}"
echo -e "${YELLOW}此筛查工具仅供教育和初步评估用途，不能替代专业医疗诊断。"
echo -e "如果您正在经历严重困扰，请立即联系心理健康专业人士或拨打紧急求助热线。"
echo -e ""
echo -e "This screening tool is for educational and preliminary assessment purposes only."
echo -e "It does not replace professional medical diagnosis. If you are in distress,"
echo -e "please contact a mental health professional or call an emergency helpline.${NC}"
echo ""
echo -e "${BLUE}过去两周内，以下问题困扰您的频率如何？"
echo -e "Over the last 2 weeks, how often have you been bothered by the following?${NC}"
echo ""
echo -e "${MAGENTA}评分标准 | Scoring:${NC}"
echo -e "  0 = 完全完全没有 (Not at all)"
echo -e "  1 = 好几天 (Several days)"
echo -e "  2 = 一半以上的天数 (More than half the days)"
echo -e "  3 = 几乎每天 (Nearly every day)"
echo ""
echo -e "${CYAN}──────────────────────────────────────────────────────────────────${NC}"

# ---- Collect Answers ----
TOTAL=0
for i in "${!QUESTIONS[@]}"; do
  qnum=$((i + 1))
  while true; do
    echo ""
    echo -e "${BOLD}问题 ${qnum}/7:${NC} ${QUESTIONS[$i]}"
    echo -n -e "${GREEN}请输入评分 (0-3): ${NC}"
    read -r answer
    if [[ "$answer" =~ ^[0-3]$ ]]; then
      SCORES+=("$answer")
      TOTAL=$((TOTAL + answer))
      break
    else
      echo -e "${RED}无效输入，请输入 0、1、2 或 3。${NC}"
    fi
  done
done

# ---- Results ----
echo ""
echo -e "${CYAN}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}  结果 | Results${NC}"
echo -e "${CYAN}──────────────────────────────────────────────────────────────────${NC}"

for i in "${!QUESTIONS[@]}"; do
  qnum=$((i + 1))
  printf "  Q%d: %-40s %s分\n" "$qnum" "${QUESTIONS[$i]}" "${SCORES[$i]}"
done

echo -e "${CYAN}──────────────────────────────────────────────────────────────────${NC}"
echo -e "${BOLD}  总分 | Total Score: ${TOTAL} / 21${NC}"
echo ""

# Severity classification
SEVERITY=""
SEVERITY_EN=""
COLOR=""
RECOMMEND=""
PROFESSIONAL=""

if (( TOTAL <= 4 )); then
  SEVERITY="无/最小焦虑"
  SEVERITY_EN="Minimal Anxiety"
  COLOR="$GREEN"
  RECOMMEND="您的焦虑水平在正常范围内。继续保持健康的生活方式。"
elif (( TOTAL <= 9 )); then
  SEVERITY="轻度焦虑"
  SEVERITY_EN="Mild Anxiety"
  COLOR="$YELLOW"
  RECOMMEND="您可能存在轻度焦虑。建议关注自身情绪变化，尝试放松技巧，如冥想、运动等。若症状持续，请咨询专业人士。"
elif (( TOTAL <= 14 )); then
  SEVERITY="中度焦虑"
  SEVERITY_EN="Moderate Anxiety"
  COLOR="$MAGENTA"
  RECOMMEND="您可能存在中度焦虑。强烈建议预约心理健康专业人士进行进一步评估。可尝试认知行为疗法(CBT)等循证治疗方法。"
else
  SEVERITY="重度焦虑"
  SEVERITY_EN="Severe Anxiety"
  COLOR="$RED"
  RECOMMEND="您的焦虑评分提示重度焦虑。请尽快联系心理健康专业人士进行评估和治疗。"
  PROFESSIONAL="yes"
fi

echo -e "  ${BOLD}严重程度 | Severity:${NC} ${COLOR}${BOLD}${SEVERITY} (${SEVERITY_EN})${NC}"
echo ""
echo -e "  ${BOLD}建议 | Recommendation:${NC}"
echo -e "  ${COLOR}${RECOMMEND}${NC}"

if [[ "$PROFESSIONAL" == "yes" ]]; then
  echo ""
  echo -e "  ${RED}${BOLD}⚠ 重要提示：您的评分较高（≥15），强烈建议尽快寻求专业心理健康评估。${NC}"
  echo -e "  ${RED}${BOLD}⚠ IMPORTANT: Your score is elevated (≥15). Professional evaluation is strongly recommended.${NC}"
fi

echo ""
echo -e "${CYAN}══════════════════════════════════════════════════════════════════${NC}"

# ---- Save Log ----
{
  echo "========================================"
  echo "GAD-7 Screening Result"
  echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "========================================"
  for i in "${!QUESTIONS[@]}"; do
    qnum=$((i + 1))
    echo "Q${qnum}: ${QUESTIONS[$i]} => ${SCORES[$i]}"
  done
  echo "----------------------------------------"
  echo "Total Score: ${TOTAL} / 21"
  echo "Severity: ${SEVERITY} (${SEVERITY_EN})"
  echo "Recommendation: ${RECOMMEND}"
  if [[ "$PROFESSIONAL" == "yes" ]]; then
    echo "ALERT: Professional evaluation recommended (score >= 15)"
  fi
  echo "========================================"
} > "$LOG_FILE"

echo ""
echo -e "${GREEN}结果已保存至: ${LOG_FILE}${NC}"
echo ""
