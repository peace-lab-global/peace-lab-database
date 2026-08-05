#!/usr/bin/env bash
set -euo pipefail

# ─── ANSI Colors ───
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
MAGENTA='\033[35m'
CYAN='\033[36m'
WHITE='\033[97m'
BG_BLUE='\033[44m'
BG_MAGENTA='\033[45m'
BG_RED='\033[41m'
BG_GREEN='\033[42m'
BG_YELLOW='\033[43m'

# ─── Script Directory & Log Setup ───
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$REPO_ROOT/logs/perma"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/perma_${TIMESTAMP}.log"

# ─── Header ───
echo ""
echo -e "${BG_BLUE}${WHITE}${BOLD}                                                              ${RESET}"
echo -e "${BG_BLUE}${WHITE}${BOLD}   PERMA 幸福感评估 | PERMA Profiler                         ${RESET}"
echo -e "${BG_BLUE}${WHITE}${BOLD}   Peace Lab Database Diagnostic                              ${RESET}"
echo -e "${BG_BLUE}${WHITE}${BOLD}                                                              ${RESET}"
echo ""
echo -e "${DIM}基于 Martin Seligman 的 PERMA 幸福模型${RESET}"
echo -e "${DIM}Based on Martin Seligman's PERMA Well-Being Model${RESET}"
echo ""
echo -e "${CYAN}─── 维度说明 Dimensions ───${RESET}"
echo -e "  ${MAGENTA}P${RESET} 积极情绪 Positive Emotion   ${MAGENTA}E${RESET} 投入 Engagement"
echo -e "  ${MAGENTA}R${RESET} 人际关系 Relationships       ${MAGENTA}M${RESET} 意义 Meaning"
echo -e "  ${MAGENTA}A${RESET} 成就 Accomplishment"
echo ""
echo -e "${YELLOW}评分范围 Rating: 0 (完全不同意) ─── 10 (完全同意)${RESET}"
echo -e "${DIM}请输入 0-10 之间的整数 (输入 q 退出)${RESET}"
echo ""

# ─── Disclaimer ───
echo -e "${BG_YELLOW}${BOLD} ⚠ 免责声明 Disclaimer ${RESET}"
echo -e "${DIM}本评估仅供自我反思和教育用途，不构成临床诊断。${RESET}"
echo -e "${DIM}This tool is for self-reflection and educational purposes only.${RESET}"
echo -e "${DIM}It is NOT a clinical assessment. Seek professional help if needed.${RESET}"
echo ""

# ─── Questions ───
declare -a QUESTIONS=(
  # P: Positive Emotion
  "总体而言，我感到快乐"
  "我经常感受到积极的情绪"
  "我对自己的生活感到满意"
  # E: Engagement
  "我经常全身心投入到正在做的事情中"
  "我经常体验到心流状态"
  "我做的事情让我感到充实"
  # R: Relationships
  "我有亲密的人可以依靠"
  "我的人际关系让我感到满足"
  "我感到被他人关心"
  # M: Meaning
  "我的生活有明确的方向和目的"
  "我的日常活动是有意义的"
  "我为比自己更大的事情做贡献"
  # A: Accomplishment
  "我在追求重要目标方面取得进展"
  "我有能力完成自己设定的目标"
  "在大多数事情上，我都表现出色"
)

declare -a DIM_NAMES=("积极情绪" "投入" "人际关系" "意义" "成就")
declare -a DIM_EN=("Positive Emotion" "Engagement" "Relationships" "Meaning" "Accomplishment")
declare -a DIM_CODES=("P" "E" "R" "M" "A")
declare -a DIM_COLORS=("$MAGENTA" "$CYAN" "$GREEN" "$BLUE" "$YELLOW")

declare -a SCORES=()

# ─── Collect Responses ───
for i in "${!QUESTIONS[@]}"; do
  q_num=$((i + 1))
  dim_idx=$((i / 3))
  dim_code="${DIM_CODES[$dim_idx]}"

  while true; do
    echo -ne "${BOLD}Q${q_num} ${DIM_COLORS[$dim_idx]}[${dim_code}]${RESET} ${QUESTIONS[$i]}${RESET}\n"
    echo -ne "    ${DIM}评分 (0-10): ${RESET}"
    read -r answer

    if [[ "$answer" == "q" || "$answer" == "Q" ]]; then
      echo -e "${RED}已退出评估。Assessment cancelled.${RESET}"
      exit 0
    fi

    if [[ "$answer" =~ ^[0-9]+$ ]] && (( answer >= 0 && answer <= 10 )); then
      SCORES+=("$answer")
      echo -e "    ${GREEN}✓ ${answer}/10${RESET}"
      echo ""
      break
    else
      echo -e "    ${RED}✗ 请输入 0-10 之间的整数 Please enter 0-10${RESET}"
      echo ""
    fi
  done
done

# ─── Calculate Scores ───
declare -a DIM_SCORES=()
for d in 0 1 2 3 4; do
  start=$((d * 3))
  sum=0
  for j in 0 1 2; do
    sum=$((sum + SCORES[start + j]))
  done
  avg=$(awk "BEGIN {printf \"%.1f\", $sum / 3}")
  DIM_SCORES+=("$avg")
done

overall=0
for s in "${DIM_SCORES[@]}"; do
  overall=$(awk "BEGIN {printf \"%.1f\", $overall + $s}")
done
overall=$(awk "BEGIN {printf \"%.1f\", $overall / 5}")

# ─── Interpretation Function ───
get_level() {
  local score=$1
  local level
  level=$(awk "BEGIN {printf \"%d\", $score}")
  if (( level <= 3 )); then
    echo "low"
  elif (( level <= 6 )); then
    echo "mid"
  else
    echo "high"
  fi
}

level_label() {
  case "$1" in
    low)  echo -e "${RED}低幸福感 (Low well-being)${RESET}" ;;
    mid)  echo -e "${YELLOW}中等幸福感 (Moderate well-being)${RESET}" ;;
    high) echo -e "${GREEN}高幸福感 (High well-being / flourishing)${RESET}" ;;
  esac
}

# ─── Bar Chart Function ───
render_bar() {
  local score=$1
  local width=20
  local filled
  filled=$(awk "BEGIN {printf \"%d\", $score / 10 * $width}")
  local empty=$((width - filled))
  local bar=""
  for ((j=0; j<filled; j++)); do bar+="█"; done
  for ((j=0; j<empty; j++)); do bar+="░"; done
  echo "$bar"
}

# ─── Results ───
echo ""
echo -e "${BG_MAGENTA}${WHITE}${BOLD}                                                              ${RESET}"
echo -e "${BG_MAGENTA}${WHITE}${BOLD}   📊 评估结果 | Assessment Results                           ${RESET}"
echo -e "${BG_MAGENTA}${WHITE}${BOLD}                                                              ${RESET}"
echo ""

echo -e "${BOLD}  维度          得分    等级    可视化${RESET}"
echo -e "  ${DIM}─────────────────────────────────────────────────────${RESET}"

weakest_idx=0
weakest_score=11

for d in 0 1 2 3 4; do
  code="${DIM_CODES[$d]}"
  dim_cn="${DIM_NAMES[$d]}"
  dim_en="${DIM_EN[$d]}"
  score="${DIM_SCORES[$d]}"
  level=$(get_level "$score")
  bar=$(render_bar "$score")

  color="${DIM_COLORS[$d]}"
  case "$level" in
    low)  lvl_icon="🔴"; lvl_color="$RED" ;;
    mid)  lvl_icon="🟡"; lvl_color="$YELLOW" ;;
    high) lvl_icon="🟢"; lvl_color="$GREEN" ;;
  esac

  printf "  %s[%s]%s %-10s %-8s %s %b%b %s %s\n" \
    "$color" "$code" "$RESET" "$dim_cn" "$dim_en" \
    "$score/10" "$lvl_color" "$RESET" "$lvl_icon" "$bar"

  cmp=$(awk "BEGIN {print ($score < $weakest_score) ? 1 : 0}")
  if (( cmp == 1 )); then
    weakest_score=$score
    weakest_idx=$d
  fi
done

echo ""
echo -e "  ${DIM}─────────────────────────────────────────────────────${RESET}"
overall_level=$(get_level "$overall")
echo -e "  ${BOLD}综合 PERMA 得分: ${WHITE}${BOLD}${overall}/10${RESET}  $(level_label "$overall_level")"
echo ""

# ─── Weakest Dimension & Recommendations ───
echo -e "${BG_BLUE}${WHITE}${BOLD} 💡 针对性建议 | Targeted Recommendations ${RESET}"
echo ""
echo -e "  ${BOLD}最需提升的维度: ${DIM_COLORS[$weakest_idx]}${DIM_NAMES[$weakest_idx]} (${DIM_EN[$weakest_idx]})${RESET} — 得分 ${RED}${weakest_score}/10${RESET}"
echo ""

case "${DIM_CODES[$weakest_idx]}" in
  P)
    cat <<'EOF'
  🌞 积极情绪提升建议 Positive Emotion:
    • 每天记录3件感恩的事情 (Gratitude journaling)
    • 练习正念冥想，关注当下的美好 (Mindfulness practice)
    • 增加让你感到快乐的日常活动 (Engage in joyful activities)
    • 与乐观积极的人多交流 (Connect with positive people)
    • 定期回顾美好回忆和成就 (Review happy memories)
EOF
    ;;
  E)
    cat <<'EOF'
  🎯 投入感提升建议 Engagement:
    • 寻找能让你进入心流状态的活动 (Seek flow activities)
    • 设定适度挑战的目标 (Set challenging but achievable goals)
    • 减少干扰，专注当下任务 (Minimize distractions)
    • 发展个人优势和特长 (Develop your strengths)
    • 尝试新事物，探索兴趣 (Explore new interests)
EOF
    ;;
  R)
    cat <<'EOF'
  💞 人际关系提升建议 Relationships:
    • 主动联系关心你的人 (Reach out to loved ones)
    • 每周安排高质量的社交时间 (Schedule quality social time)
    • 练习主动倾听和表达关心 (Practice active listening)
    • 加入社区或兴趣小组 (Join community groups)
    • 学习表达感激和爱意 (Express gratitude and love)
EOF
    ;;
  M)
    cat <<'EOF'
  🌟 意义感提升建议 Meaning:
    • 思考什么对你最重要 (Reflect on core values)
    • 参与志愿服务或公益活动 (Engage in volunteering)
    • 将日常工作与个人价值联系起来 (Connect work to values)
    • 探索精神或哲学层面的实践 (Explore spiritual practices)
    • 为社区或社会做出贡献 (Contribute to community)
EOF
    ;;
  A)
    cat <<'EOF'
  🏆 成就感提升建议 Accomplishment:
    • 设定具体、可衡量的目标 (Set SMART goals)
    • 将大目标分解为小步骤 (Break goals into small steps)
    • 庆祝每一个小进步 (Celebrate small wins)
    • 建立正向反馈循环 (Build positive feedback loops)
    • 学习新技能，提升胜任感 (Learn new skills)
EOF
    ;;
esac

echo ""

# ─── Summary for Strongest Dimension ───
strongest_idx=0
strongest_score=0
for d in 0 1 2 3 4; do
  cmp=$(awk "BEGIN {print (${DIM_SCORES[$d]} > $strongest_score) ? 1 : 0}")
  if (( cmp == 1 )); then
    strongest_score=${DIM_SCORES[$d]}
    strongest_idx=$d
  fi
done

echo -e "  ${BOLD}最强维度: ${DIM_COLORS[$strongest_idx]}${DIM_NAMES[$strongest_idx]} (${DIM_EN[$strongest_idx]})${RESET} — 得分 ${GREEN}${strongest_score}/10${RESET}"
echo -e "  ${DIM}继续发挥这个优势，它可以帮助提升其他维度。${RESET}"
echo -e "  ${DIM}Leverage this strength to uplift other dimensions.${RESET}"
echo ""

# ─── Save Log ───
{
  echo "=========================================="
  echo "PERMA Profiler Results"
  echo "Date: $(date)"
  echo "=========================================="
  echo ""
  echo "Responses (Q1-Q15):"
  for i in "${!QUESTIONS[@]}"; do
    q=$((i + 1))
    dim_idx=$((i / 3))
    echo "  Q${q} [${DIM_CODES[$dim_idx]}] ${QUESTIONS[$i]}: ${SCORES[$i]}/10"
  done
  echo ""
  echo "Dimension Scores:"
  for d in 0 1 2 3 4; do
    echo "  ${DIM_CODES[$d]} ${DIM_EN[$d]}: ${DIM_SCORES[$d]}/10"
  done
  echo ""
  echo "Overall PERMA Score: ${overall}/10"
  echo "Weakest Dimension: ${DIM_CODES[$weakest_idx]} ${DIM_EN[$weakest_idx]} (${weakest_score}/10)"
  echo "Strongest Dimension: ${DIM_CODES[$strongest_idx]} ${DIM_EN[$strongest_idx]} (${strongest_score}/10)"
  echo ""
  echo "=========================================="
  echo "Disclaimer: For self-reflection only."
  echo "Not a clinical assessment."
  echo "=========================================="
} > "$LOG_FILE"

echo -e "${DIM}────────────────────────────────────────────────────────────${RESET}"
echo -e "${GREEN}${BOLD}  ✓ 评估完成 | Assessment Complete${RESET}"
echo -e "${DIM}  结果已保存至 Results saved to:${RESET}"
echo -e "  ${CYAN}${LOG_FILE}${RESET}"
echo ""
echo -e "${DIM}  若您正经历心理健康困扰，请寻求专业帮助。${RESET}"
echo -e "${DIM}  If you are struggling, please seek professional support.${RESET}"
echo -e "${DIM}  🌐 https://www.samhsa.gov/find-help/national-helpline${RESET}"
echo ""
