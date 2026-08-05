#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# MBI 职业倦怠量表 | Maslach Burnout Inventory (Simplified)
# Part of Peace Lab Database Diagnostic Tools
# ============================================================

# ANSI Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/../../logs/diagnostic"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${LOG_DIR}/mbi_screen_${TIMESTAMP}.log"

# --- Disclaimer ---
echo ""
echo -e "${MAGENTA}================================================================${NC}"
echo -e "${BOLD}  MBI 职业倦怠量表 | Maslach Burnout Inventory${NC}"
echo -e "${BOLD}  简化筛查版 (Simplified Screening Version)${NC}"
echo -e "${MAGENTA}================================================================${NC}"
echo ""
echo -e "${YELLOW}⚠  免责声明 / DISCLAIMER:${NC}"
echo -e "${DIM}本筛查工具仅供初步自我评估参考，不能替代专业的心理诊断。"
echo -e "如果您感到严重的心理困扰，请寻求专业心理咨询师或医生的帮助。"
echo -e "This tool is for preliminary self-assessment only and does NOT"
echo -e "replace professional diagnosis. Seek help if in distress.${NC}"
echo ""
echo -e "${DIM}计分方式: 0=从不 1=每年几次 2=每月一次 3=每月几次"
echo -e "         4=每周一次 5=每周几次 6=每天${NC}"
echo ""
echo -e "${CYAN}按 Enter 开始...${NC}"
read -r

# --- Questions ---
declare -a QUESTIONS=(
  "[Q1] 工作让我感到身心俱疲"
  "[Q2] 下班后我感到精疲力竭"
  "[Q3] 早上想到要工作就感到疲惫"
  "[Q4] 我对工作对象变得越来越冷漠"
  "[Q5] 我对工作不像以前那样热情"
  "[Q6] 我怀疑自己工作的意义"
  "[Q7] 我能有效地解决工作中的问题 [R]"
  "[Q8] 我觉得自己对工作有积极贡献 [R]"
  "[Q9] 我对自己的工作能力有信心 [R]"
)

declare -a ANSWERS=()

echo -e "${BOLD}${CYAN}━━━ 开始作答 / Begin ━━━${NC}"
echo ""

for i in "${!QUESTIONS[@]}"; do
  qnum=$((i + 1))
  while true; do
    echo -e "${BOLD}${QUESTIONS[$i]}${NC}"
    echo -n "  评分 (0-6): "
    read -r score
    if [[ "$score" =~ ^[0-6]$ ]]; then
      ANSWERS+=("$score")
      break
    else
      echo -e "  ${RED}请输入 0 到 6 之间的数字。${NC}"
    fi
  done
  echo ""
done

# --- Scoring ---
EE_SUM=0
DP_SUM=0
PA_RAW=0

# Q1-Q3: Emotional Exhaustion
for i in 0 1 2; do
  EE_SUM=$((EE_SUM + ANSWERS[$i]))
done

# Q4-Q6: Depersonalization
for i in 3 4 5; do
  DP_SUM=$((DP_SUM + ANSWERS[$i]))
done

# Q7-Q9: Personal Accomplishment (reverse scored)
for i in 6 7 8; do
  rev=$((6 - ANSWERS[$i]))
  PA_RAW=$((PA_RAW + rev))
done

# --- Interpretation ---
EE_HIGH=0; DP_HIGH=0; PA_LOW=0
BURNOUT_INDICATORS=0

(( EE_SUM >= 27 )) && EE_HIGH=1 && ((BURNOUT_INDICATORS++))
(( DP_SUM >= 10 )) && DP_HIGH=1 && ((BURNOUT_INDICATORS++))
(( PA_RAW <= 33 )) && PA_LOW=1 && ((BURNOUT_INDICATORS++))

if (( BURNOUT_INDICATORS == 0 )); then
  LEVEL="低 (Low)"
  LEVEL_COLOR="$GREEN"
elif (( BURNOUT_INDICATORS == 1 )); then
  LEVEL="中 (Moderate)"
  LEVEL_COLOR="$YELLOW"
else
  LEVEL="高 (High)"
  LEVEL_COLOR="$RED"
fi

# --- Results ---
echo ""
echo -e "${MAGENTA}================================================================${NC}"
echo -e "${BOLD}  评估结果 / Results${NC}"
echo -e "${MAGENTA}================================================================${NC}"
echo ""

# Dimension scores
echo -e "${BOLD}维度得分 / Dimension Scores:${NC}"
echo ""

if (( EE_HIGH )); then
  echo -e "  情绪耗竭 (EE):   ${RED}${BOLD}${EE_SUM}/54  ▲ 高情绪耗竭${NC}"
else
  echo -e "  情绪耗竭 (EE):   ${GREEN}${EE_SUM}/54${NC}"
fi

if (( DP_HIGH )); then
  echo -e "  去人格化 (DP):   ${RED}${BOLD}${DP_SUM}/36  ▲ 高去人格化${NC}"
else
  echo -e "  去人格化 (DP):   ${GREEN}${DP_SUM}/36${NC}"
fi

if (( PA_LOW )); then
  echo -e "  个人成就感 (PA): ${RED}${BOLD}${PA_RAW}/54  ▼ 低个人成就感${NC}"
else
  echo -e "  个人成就感 (PA): ${GREEN}${PA_RAW}/54${NC}"
fi

echo ""
echo -e "  ${BOLD}综合倦怠水平:${NC}  ${LEVEL_COLOR}${BOLD}${LEVEL}${NC}"
echo ""

# --- Bar chart ---
print_bar() {
  local label=$1 val=$2 max=$3 threshold=$4 reverse=$5
  local width=30
  local filled=$(( val * width / max ))
  local bar=""
  for ((j=0; j<width; j++)); do
    if (( j < filled )); then
      bar+="█"
    else
      bar+="░"
    fi
  done
  local color="$GREEN"
  if (( reverse == 0 )); then
    (( val >= threshold )) && color="$RED"
  else
    (( val <= threshold )) && color="$RED"
  fi
  echo -e "  ${DIM}${label}${NC} ${color}${bar}${NC} ${val}/${max}"
}

echo -e "${BOLD}可视化 / Visualization:${NC}"
print_bar "EE" "$EE_SUM" 54 27 0
print_bar "DP" "$DP_SUM" 36 10 0
print_bar "PA" "$PA_RAW" 54 33 1

echo ""

# --- Recommendations ---
echo -e "${BOLD}建议 / Recommendations:${NC}"
echo ""

if (( BURNOUT_INDICATORS == 0 )); then
  echo -e "  ${GREEN}✓ 您目前的职业倦怠风险较低。${NC}"
  echo -e "  ${GREEN}  继续保持良好的工作生活平衡。${NC}"
  echo -e "  ${GREEN}  Continue maintaining healthy work-life balance.${NC}"
elif (( BURNOUT_INDICATORS == 1 )); then
  echo -e "  ${YELLOW}△ 您存在一定程度的职业倦怠迹象。${NC}"
  echo -e "  ${YELLOW}  建议关注相关维度，适当调整工作节奏。${NC}"
  echo -e "  ${YELLOW}  Consider adjusting workload and self-care.${NC}"
  if (( EE_HIGH )); then
    echo -e "  ${YELLOW}  → 注意休息和压力管理。${NC}"
  fi
  if (( DP_HIGH )); then
    echo -e "  ${YELLOW}  → 重新寻找工作的意义和热情。${NC}"
  fi
  if (( PA_LOW )); then
    echo -e "  ${YELLOW}  → 关注自身成就和能力发展。${NC}"
  fi
else
  echo -e "  ${RED}✗ 您存在明显的职业倦怠风险。${NC}"
  echo -e "  ${RED}  强烈建议寻求专业心理咨询支持。${NC}"
  echo -e "  ${RED}  Strongly recommend seeking professional support.${NC}"
  echo -e ""
  echo -e "  ${CYAN}  资源 / Resources:${NC}"
  echo -e "  ${DIM}  • 全国心理援助热线: 400-161-9995${NC}"
  echo -e "  ${DIM}  • 北京心理危机研究与干预中心: 010-82951332${NC}"
  echo -e "  ${DIM}  • 生命热线: 400-821-1215${NC}"
fi

echo ""
echo -e "${DIM}参考阈值 / Thresholds: EE≥27 高 | DP≥10 高 | PA≤33 低${NC}"
echo ""

# --- Save log ---
{
  echo "MBI Screening Log - $(date '+%Y-%m-%d %H:%M:%S')"
  echo "================================================="
  echo ""
  echo "Responses:"
  for i in "${!QUESTIONS[@]}"; do
    echo "  ${QUESTIONS[$i]}: ${ANSWERS[$i]}"
  done
  echo ""
  echo "Scores:"
  echo "  Emotional Exhaustion (EE): ${EE_SUM}/54"
  echo "  Depersonalization (DP):    ${DP_SUM}/36"
  echo "  Personal Accomplishment (PA): ${PA_RAW}/54"
  echo "  Burnout Indicators: ${BURNOUT_INDICATORS}/3"
  echo "  Overall Level: ${LEVEL}"
} > "$LOG_FILE"

echo -e "${DIM}结果已保存至: ${LOG_FILE}${NC}"
echo ""
