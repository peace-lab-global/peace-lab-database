#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# ISI 失眠严重程度指数 | Insomnia Severity Index
# Peace Lab Database - Diagnostic Screening Tool
# ============================================================
# Reference: Bastien CH, Vallières A, Morin CM (2001).
#   Validation of the Insomnia Severity Index as an outcome
#   measure for insomnia research. Sleep Medicine, 2(4), 297-307.
# ============================================================

# --- ANSI Color Definitions ---
BOLD='\033[1m'
DIM='\033[2m'
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
WHITE='\033[1;37m'
BG_BLUE='\033[44m'
BG_RED='\033[41m'
BG_GREEN='\033[42m'
BG_YELLOW='\033[43m'
RESET='\033[0m'

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="${REPO_ROOT}/data/diagnostic-logs"
TIMESTAMP="$(date '+%Y%m%d_%H%M%S')"
LOG_FILE="${LOG_DIR}/isi_${TIMESTAMP}.txt"

# --- Ensure log directory exists ---
mkdir -p "$LOG_DIR"

# --- ISI Questions (Chinese) ---
QUESTIONS=(
  "入睡困难程度"
  "保持睡眠困难程度"
  "早醒问题"
  "对当前睡眠模式的满意度"
  "睡眠问题对日常功能的影响程度"
  "睡眠问题引起他人注意的程度"
  "因睡眠问题引起的担忧/苦恼程度"
)

QUESTION_LABELS=(
  "Q1"
  "Q2"
  "Q3"
  "Q4"
  "Q5"
  "Q6"
  "Q7"
)

# --- Helper Functions ---

print_separator() {
  printf "${CYAN}%s${RESET}\n" "────────────────────────────────────────────────────────"
}

print_header() {
  echo ""
  printf "${BG_BLUE}${WHITE}${BOLD}                                                            ${RESET}\n"
  printf "${BG_BLUE}${WHITE}${BOLD}   ISI 失眠严重程度指数 | Insomnia Severity Index          ${RESET}\n"
  printf "${BG_BLUE}${WHITE}${BOLD}   Peace Lab Database · 睡眠质量筛查工具                   ${RESET}\n"
  printf "${BG_BLUE}${WHITE}${BOLD}                                                            ${RESET}\n"
  echo ""
}

print_disclaimer() {
  printf "${YELLOW}${BOLD}⚠  免责声明 / DISCLAIMER${RESET}\n"
  print_separator
  printf "${DIM}"
  printf "本工具仅供筛查参考，不能替代专业医学诊断。\n"
  printf "This tool is for screening purposes only and does NOT\n"
  printf "replace a professional medical diagnosis.\n"
  printf "\n"
  printf "如果您正在经历严重的睡眠问题，请及时咨询医疗专业人员。\n"
  printf "If you are experiencing severe sleep problems, please\n"
  printf "consult a healthcare professional promptly.\n"
  printf "${RESET}"
  print_separator
  echo ""
}

print_scale_reference() {
  printf "${BOLD}评分标准 / Scoring Scale:${RESET}\n"
  printf "  ${GREEN}0${RESET} = 无       (None)          "
  printf "${GREEN}1${RESET} = 轻度   (Mild)\n"
  printf "  ${YELLOW}2${RESET} = 中度     (Moderate)       "
  printf "${RED}3${RESET} = 重度   (Severe)\n"
  printf "  ${MAGENTA}4${RESET} = 极重度   (Very Severe)\n"
  echo ""
  print_separator
  echo ""
}

ask_question() {
  local q_num="$1"
  local q_label="$2"
  local q_text="$3"
  local score=""

  printf "${BOLD}${BLUE}%s${RESET} ${WHITE}%s${RESET}\n" "$q_label" "$q_text"
  printf "${DIM}    请评分 (0-4): ${RESET}"

  while true; do
    read -r score
    if [[ "$score" =~ ^[0-4]$ ]]; then
      break
    else
      printf "${RED}    ✗ 请输入有效数字 (0-4): ${RESET}"
    fi
  done

  echo "$score"
}

get_severity() {
  local score="$1"
  if (( score <= 7 )); then
    echo "无临床意义|No clinical significance"
  elif (( score <= 14 )); then
    echo "亚阈值失眠|Subthreshold insomnia"
  elif (( score <= 21 )); then
    echo "临床失眠-中度|Clinical insomnia - moderate"
  else
    echo "临床失眠-重度|Clinical insomnia - severe"
  fi
}

get_severity_color() {
  local score="$1"
  if (( score <= 7 )); then
    echo "$GREEN"
  elif (( score <= 14 )); then
    echo "$YELLOW"
  elif (( score <= 21 )); then
    echo "$RED"
  else
    echo "$MAGENTA"
  fi
}

print_results() {
  local total="$1"
  shift
  local answers=("$@")
  local severity_info
  severity_info="$(get_severity "$total")"
  local severity_cn="${severity_info%%|*}"
  local severity_en="${severity_info##*|}"
  local sev_color
  sev_color="$(get_severity_color "$total")"

  echo ""
  print_separator
  printf "${BG_GREEN}${WHITE}${BOLD}              📊 评估结果 / Assessment Results              ${RESET}\n"
  print_separator
  echo ""

  # Score breakdown
  printf "${BOLD}评分明细 / Score Breakdown:${RESET}\n"
  for i in "${!QUESTIONS[@]}"; do
    printf "  %s %-30s  %s/4${RESET}\n" \
      "${QUESTION_LABELS[$i]}" "${QUESTIONS[$i]}" "${CYAN}${answers[$i]}"
  done
  echo ""
  print_separator

  # Total score with bar visualization
  local bar_len=$(( total * 2 ))
  local bar=""
  for (( j=0; j<28; j++ )); do
    if (( j < total )); then
      bar+="█"
    else
      bar+="░"
    fi
  done

  printf "${BOLD}总分 / Total Score: ${sev_color}%d / 28${RESET}\n" "$total"
  printf "${sev_color}  [%s]${RESET}\n" "$bar"
  echo ""

  # Severity classification
  printf "${BOLD}严重程度分类 / Severity Classification:${RESET}\n"
  printf "  ${sev_color}${BOLD}▸ %s${RESET}\n" "$severity_cn"
  printf "  ${DIM}  %s${RESET}\n" "$severity_en"
  echo ""

  # Classification reference
  printf "${DIM}分类参考 / Classification Reference:${RESET}\n"
  if (( total <= 7 )); then
    printf "  ${GREEN}${BOLD}●${RESET}  0-7:   无临床意义 (No clinical significance)    ${GREEN}◀ 当前${RESET}\n"
  else
    printf "  ${DIM}●  0-7:   无临床意义 (No clinical significance)${RESET}\n"
  fi
  if (( total >= 8 && total <= 14 )); then
    printf "  ${YELLOW}${BOLD}●${RESET}  8-14:  亚阈值失眠 (Subthreshold insomnia)       ${YELLOW}◀ 当前${RESET}\n"
  else
    printf "  ${DIM}●  8-14:  亚阈值失眠 (Subthreshold insomnia)${RESET}\n"
  fi
  if (( total >= 15 && total <= 21 )); then
    printf "  ${RED}${BOLD}●${RESET}  15-21: 临床失眠-中度 (Clinical - moderate)      ${RED}◀ 当前${RESET}\n"
  else
    printf "  ${DIM}●  15-21: 临床失眠-中度 (Clinical - moderate)${RESET}\n"
  fi
  if (( total >= 22 )); then
    printf "  ${MAGENTA}${BOLD}●${RESET}  22-28: 临床失眠-重度 (Clinical - severe)       ${MAGENTA}◀ 当前${RESET}\n"
  else
    printf "  ${DIM}●  22-28: 临床失眠-重度 (Clinical - severe)${RESET}\n"
  fi
  echo ""
  print_separator

  # Recommendations
  printf "${BOLD}💡 建议 / Recommendations:${RESET}\n"
  echo ""

  if (( total <= 7 )); then
    printf "  ${GREEN}✓${RESET} 您的睡眠质量良好，无明显失眠问题。\n"
    printf "    Your sleep quality is good with no significant insomnia.\n"
    echo ""
    printf "  ${GREEN}✓${RESET} 继续保持良好的睡眠卫生习惯。\n"
    printf "    Continue maintaining good sleep hygiene.\n"
  fi

  if (( total >= 8 )); then
    printf "  ${YELLOW}▸${RESET} ${BOLD}睡眠卫生建议 / Sleep Hygiene:${RESET}\n"
    printf "    · 固定作息时间，包括周末\n"
    printf "    · Maintain consistent sleep/wake times, including weekends\n"
    printf "    · 避免睡前使用电子设备 (蓝光)\n"
    printf "    · Avoid screens before bed (blue light)\n"
    printf "    · 限制咖啡因和酒精摄入\n"
    printf "    · Limit caffeine and alcohol intake\n"
    printf "    · 保持卧室凉爽、安静、黑暗\n"
    printf "    · Keep bedroom cool, quiet, and dark\n"
    echo ""
  fi

  if (( total >= 8 && total <= 14 )); then
    printf "  ${YELLOW}▸${RESET} ${BOLD}认知行为疗法 (CBT-I) 可能有益。${RESET}\n"
    printf "    Cognitive Behavioral Therapy for Insomnia (CBT-I) may be beneficial.\n"
    printf "    ${DIM}推荐自助CBT-I资源或与治疗师预约咨询。${RESET}\n"
    printf "    ${DIM}Consider self-help CBT-I resources or booking a session.${RESET}\n"
  fi

  if (( total >= 15 )); then
    printf "  ${RED}▸${RESET} ${BOLD}强烈建议寻求专业睡眠医学评估。${RESET}\n"
    printf "    ${RED}Strongly recommended: seek professional sleep medicine evaluation.${RESET}\n"
    echo ""
    printf "  ${RED}▸${RESET} ${BOLD}推荐转介 / Referrals:${RESET}\n"
    printf "    · CBT-I (失眠认知行为疗法) - 一线治疗方案\n"
    printf "      CBT-I - first-line treatment for insomnia\n"
    printf "    · 睡眠医学专科医生\n"
    printf "      Sleep medicine specialist\n"
    printf "    · 可能需要多导睡眠监测 (PSG)\n"
    printf "      Polysomnography (PSG) may be recommended\n"
  fi

  if (( total >= 22 )); then
    echo ""
    printf "  ${BG_RED}${WHITE}${BOLD}  ⚠ 紧急建议 / URGENT RECOMMENDATION                       ${RESET}\n"
    printf "  ${RED}${BOLD}  您的评分表明重度失眠，严重影响生活质量。${RESET}\n"
    printf "  ${RED}  Your score indicates severe insomnia significantly${RESET}\n"
    printf "  ${RED}  impacting quality of life.${RESET}\n"
    echo ""
    printf "  ${RED}${BOLD}  → 请立即预约专业医疗评估。${RESET}\n"
    printf "  ${RED}${BOLD}  → Please seek immediate professional evaluation.${RESET}\n"
    echo ""
    printf "  ${DIM}  如您有自杀或自伤想法，请立即拨打急救电话：${RESET}\n"
    printf "  ${DIM}  If you have thoughts of self-harm, call emergency services:${RESET}\n"
    printf "  ${BOLD}  · 中国心理危机干预热线: 400-161-9995${RESET}\n"
    printf "  ${BOLD}  · 北京心理危机研究与干预中心: 010-82951332${RESET}\n"
    printf "  ${BOLD}  · 全国24小时心理援助热线: 400-161-9995${RESET}\n"
    printf "  ${BOLD}  · International: 988 Suicide & Crisis Lifeline (US)${RESET}\n"
  fi

  echo ""
  print_separator

  # Disclaimer footer
  printf "${DIM}本筛查结果仅供临床参考，不构成医学诊断。\n"
  printf "This screening result is for clinical reference only\n"
  printf "and does not constitute a medical diagnosis.${RESET}\n"
  print_separator
  echo ""
}

save_log() {
  local total="$1"
  local severity_info="$2"
  shift 2
  local answers=("$@")

  {
    echo "============================================"
    echo "ISI (Insomnia Severity Index) Screening Log"
    echo "Peace Lab Database"
    echo "============================================"
    echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Host: $(hostname 2>/dev/null || echo 'unknown')"
    echo ""
    echo "--- Responses ---"
    for i in "${!QUESTIONS[@]}"; do
      printf "%s %s: %d/4\n" "${QUESTION_LABELS[$i]}" "${QUESTIONS[$i]}" "${answers[$i]}"
    done
    echo ""
    echo "--- Results ---"
    echo "Total Score: ${total} / 28"
    echo "Severity (CN): ${severity_info%%|*}"
    echo "Severity (EN): ${severity_info##*|}"
    echo ""
    echo "Classification Reference:"
    echo "  0-7:   No clinical significance"
    echo "  8-14:  Subthreshold insomnia"
    echo "  15-21: Clinical insomnia - moderate"
    echo "  22-28: Clinical insomnia - severe"
    if (( total >= 22 )); then
      echo ""
      echo "⚠ URGENT: Immediate professional evaluation recommended."
    fi
    echo ""
    echo "============================================"
    echo "Disclaimer: For screening purposes only."
    echo "Not a substitute for professional diagnosis."
    echo "============================================"
  } > "$LOG_FILE"
}

# ============================================================
# Main
# ============================================================

print_header
print_disclaimer
print_scale_reference

# Collect answers
ANSWERS=()
TOTAL=0

for i in "${!QUESTIONS[@]}"; do
  answer="$(ask_question "$((i+1))" "${QUESTION_LABELS[$i]}" "${QUESTIONS[$i]}")"
  ANSWERS+=("$answer")
  TOTAL=$(( TOTAL + answer ))
  echo ""
done

# Compute severity
SEVERITY="$(get_severity "$TOTAL")"

# Display results
print_results "$TOTAL" "${ANSWERS[@]}"

# Save log
save_log "$TOTAL" "$SEVERITY" "${ANSWERS[@]}"

printf "${DIM}结果已保存至 / Results saved to:${RESET}\n"
printf "${CYAN}  %s${RESET}\n" "$LOG_FILE"
echo ""
