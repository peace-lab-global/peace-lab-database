#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# PCL-5 创伤后应激障碍检查表 | PTSD Checklist (Screen 5)
# Part of Peace Lab Database — Diagnostic Screening Tools
#
# References:
#   - Weathers, F.W., et al. (2013). The PTSD Checklist for DSM-5 (PCL-5).
#   - American Psychiatric Association. (2013). DSM-5.
#
# DISCLAIMER: This is a SCREENING tool only. It is NOT a clinical diagnosis.
# A positive screen indicates the need for further evaluation by a qualified
# mental health professional. If you are in crisis, please contact emergency
# services immediately.
###############################################################################

# ── ANSI Colors ──────────────────────────────────────────────────────────────
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
MAGENTA='\033[1;35m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
DIM='\033[2m'
UNDERLINE='\033[4m'
NC='\033[0m'  # No Color

# ── Configuration ────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="${REPO_ROOT}/data/screener-logs"
mkdir -p "$LOG_DIR"
TIMESTAMP="$(date '+%Y%m%d_%H%M%S')"
LOG_FILE="${LOG_DIR}/pcl5_${TIMESTAMP}.txt"

# Score thresholds
TOTAL_THRESHOLD=31

# ── PCL-5 Item Definitions ───────────────────────────────────────────────────
# Format: "ID|Cluster|Chinese text"
declare -a ITEMS=(
  # Cluster B: 闯入症状 (Intrusion Symptoms)
  "B1|B|在过去一个月中，反复回忆起创伤事件中令人痛苦的记忆、想法或画面"
  "B2|B|在过去一个月中，反复做与创伤事件有关的噩梦"
  "B3|B|在过去一个月中，突然感觉或表现得好像创伤事件正在重新发生（闪回）"
  "B4|B|在过去一个月中，当接触到与创伤事件相关的提醒物时，感到强烈的心理痛苦"
  "B5|B|在过去一个月中，当接触到与创伤事件相关的提醒物时，产生强烈的生理反应（心跳加速、出汗、呼吸困难等）"

  # Cluster C: 回避症状 (Avoidance Symptoms)
  "C1|C|在过去一个月中，回避与创伤事件相关的令人痛苦的记忆、想法或感受"
  "C2|C|在过去一个月中，回避与创伤事件相关的外部提示物（人、地点、对话、活动、物品或情境）"

  # Cluster D: 认知和情绪改变 (Negative Cognitions and Mood)
  "D1|D|在过去一个月中，无法记住创伤事件的重要部分"
  "D2|D|在过去一个月中，对自己、他人或世界产生了强烈的负性信念（如"我很坏"、"没有人可以信任"、"世界非常危险"）"
  "D3|D|在过去一个月中，对自己或他人为什么会发生创伤事件的原因或后果产生扭曲的自责或责备"
  "D4|D|在过去一个月中，持续体验到恐惧、愤怒、内疚、羞耻等负性情绪"
  "D5|D|在过去一个月中，对以前重要的活动明显失去兴趣或减少参与"
  "D6|D|在过去一个月中，感到与他人疏远或疏离"
  "D7|D|在过去一个月中，难以体验到积极情绪（如无法感到幸福、满足或爱）"

  # Cluster E: 高警觉和反应性 (Alterations in Arousal and Reactivity)
  "E1|E|在过去一个月中，易激惹或出现愤怒的言语或身体行为（对人或物发怒）"
  "E2|E|在过去一个月中，出现鲁莽或自毁行为（如危险驾驶、过度饮酒、自伤等）"
  "E3|E|在过去一个月中，过度警觉"
  "E4|E|在过去一个月中，惊跳反应增强（容易受惊）"
  "E5|E|在过去一个月中，注意力难以集中"
  "E6|E|在过去一个月中，入睡困难或睡眠不安"
)

# Cluster labels with color codes
declare -A CLUSTER_NAMES=(
  [B]="${RED}闯入症状 (Intrusion)${NC}"
  [C]="${MAGENTA}回避症状 (Avoidance)${NC}"
  [D]="${BLUE}认知和情绪改变 (Neg. Cognitions & Mood)${NC}"
  [E]="${YELLOW}高警觉和反应性 (Arousal & Reactivity)${NC}"
)

declare -A CLUSTER_PLAIN=(
  [B]="闯入症状 (Intrusion)"
  [C]="回避症状 (Avoidance)"
  [D]="认知和情绪改变 (Negative Cognitions & Mood)"
  [E]="高警觉和反应性 (Alterations in Arousal & Reactivity)"
)

declare -A CLUSTER_COUNT=(
  [B]=5
  [C]=2
  [D]=7
  [E]=6
)

# Scale labels
declare -a SCALE_LABELS=("一点也不" "有一点  " "中    度" "相当  多" "极    度")

# ── Helper Functions ──────────────────────────────────────────────────────────

print_line() {
  printf '%*s\n' 70 '' | tr ' ' '─'
}

print_double_line() {
  printf '%*s\n' 70 '' | tr ' ' '═'
}

print_header() {
  echo ""
  print_double_line
  echo -e "${WHITE}${BOLD}"
  echo "    ╔══════════════════════════════════════════════════════════════╗"
  echo "    ║  PCL-5 创伤后应激障碍检查表  |  PTSD Checklist for DSM-5  ║"
  echo "    ╚══════════════════════════════════════════════════════════════╝"
  echo -e "${NC}"
  print_double_line
  echo ""
}

print_disclaimer() {
  echo -e "${RED}${BOLD}⚠  免责声明 / DISCLAIMER${NC}"
  print_line
  echo -e "${DIM}本工具仅为筛查工具，不构成临床诊断。阳性筛查结果表明需要"
  echo -e "由有资质的心理健康专业人员进行进一步评估。"
  echo -e ""
  echo -e "This is a SCREENING tool only. It is NOT a clinical diagnosis."
  echo -e "A positive screen requires further evaluation by a qualified"
  echo -e "mental health professional.${NC}"
  echo ""
  echo -e "${RED}${BOLD}如果您正处于危机中，请立即拨打紧急服务电话。"
  echo -e "If you are in crisis, please call emergency services immediately.${NC}"
  echo ""
  print_line
  echo ""
}

print_scale() {
  echo -e "${BOLD}评分标准 / Rating Scale:${NC}"
  echo -e "  ${GREEN}0${NC} = 一点也不 (Not at all)"
  echo -e "  ${CYAN}1${NC} = 有一点   (A little bit)"
  echo -e "  ${YELLOW}2${NC} = 中度     (Moderately)"
  echo -e "  ${MAGENTA}3${NC} = 相当多   (Quite a bit)"
  echo -e "  ${RED}4${NC} = 极度     (Extremely)"
  echo ""
}

# ── Main Script ──────────────────────────────────────────────────────────────

main() {
  clear 2>/dev/null || true

  print_header
  print_disclaimer

  read -rp "$(echo -e "${BOLD}按 Enter 开始评估 / Press Enter to begin...${NC}")"
  echo ""

  print_scale

  # Arrays to hold scores
  declare -A cluster_scores=([B]=0 [C]=0 [D]=0 [E]=0)
  declare -a raw_scores=()
  total_score=0
  item_num=0
  current_cluster=""

  for item_def in "${ITEMS[@]}"; do
    IFS='|' read -r id cluster text <<< "$item_def"
    item_num=$((item_num + 1))

    # Print cluster header when cluster changes
    if [[ "$cluster" != "$current_cluster" ]]; then
      current_cluster="$cluster"
      echo ""
      print_line
      echo -e "  ${BOLD}Cluster ${cluster}${NC}: ${CLUSTER_NAMES[$cluster]}"
      echo -e "  ${DIM}(共 ${CLUSTER_COUNT[$cluster]} 项 / ${CLUSTER_COUNT[$cluster]} items)${NC}"
      print_line
      echo ""
    fi

    # Display item
    echo -e "${BOLD}${WHITE}[${item_num}/20] ${id}${NC}"
    echo -e "  ${text}"
    echo ""

    # Read valid input
    while true; do
      read -rp "$(echo -e "  ${BOLD}您的评分 (0-4): ${NC}")" score_input

      # Validate: must be 0, 1, 2, 3, or 4
      if [[ "$score_input" =~ ^[0-4]$ ]]; then
        break
      else
        echo -e "  ${RED}请输入 0-4 之间的数字 / Please enter a number between 0 and 4.${NC}"
      fi
    done

    raw_scores+=("$score_input")
    cluster_scores[$cluster]=$(( ${cluster_scores[$cluster]} + score_input ))
    total_score=$(( total_score + score_input ))

    # Echo confirmation
    echo -e "  ${GREEN}✓ ${SCALE_LABELS[$score_input]} (${score_input})${NC}"
    echo ""
  done

  # ── Results ──────────────────────────────────────────────────────────────
  echo ""
  print_double_line
  echo ""
  echo -e "${WHITE}${BOLD}"
  echo "    ╔══════════════════════════════════════════════════════════════╗"
  echo "    ║              评估结果 / ASSESSMENT RESULTS                 ║"
  echo "    ╚══════════════════════════════════════════════════════════════╝"
  echo -e "${NC}"
  print_double_line
  echo ""

  # Total score
  if (( total_score >= TOTAL_THRESHOLD )); then
    score_color="${RED}"
    score_label="⚠  提示PTSD可能 (Probable PTSD)"
  else
    score_color="${GREEN}"
    score_label="未达到PTSD筛查阈值 (Below probable PTSD threshold)"
  fi

  echo -e "${BOLD}  总分 / Total Score:${NC}"
  echo -e "    ${score_color}${BOLD}${total_score} / 80${NC}"
  echo -e "    ${score_color}${score_label}${NC}"
  echo ""
  echo -e "  ${DIM}筛查阈值 / Screening threshold: ≥ ${TOTAL_THRESHOLD}${NC}"
  echo ""

  # Cluster scores
  print_line
  echo -e "${BOLD}  症状群集得分 / Symptom Cluster Scores:${NC}"
  echo ""

  for cluster in B C D E; do
    max_possible=$(( CLUSTER_COUNT[$cluster] * 4 ))
    pct=$(( cluster_scores[$cluster] * 100 / max_possible ))

    # Build progress bar
    bar_filled=$(( pct / 5 ))
    bar_empty=$(( 20 - bar_filled ))
    bar=""
    for ((i=0; i<bar_filled; i++)); do bar+="█"; done
    for ((i=0; i<bar_empty; i++)); do bar+="░"; done

    if (( pct >= 60 )); then
      bar_color="${RED}"
    elif (( pct >= 40 )); then
      bar_color="${YELLOW}"
    else
      bar_color="${GREEN}"
    fi

    echo -e "  Cluster ${cluster}: ${CLUSTER_NAMES[$cluster]}"
    echo -e "    得分: ${BOLD}${cluster_scores[$cluster]}${NC} / ${max_possible}  "
    echo -e "    ${bar_color}${bar}${NC} ${pct}%"
    echo ""
  done

  # ── Recommendations ────────────────────────────────────────────────────
  print_line
  echo -e "${BOLD}  建议 / Recommendations:${NC}"
  echo ""

  if (( total_score >= 50 )); then
    echo -e "  ${RED}${BOLD}● 高度疑似PTSD${NC}"
    echo -e "  ${RED}  强烈建议尽快寻求专业心理健康评估和治疗。${NC}"
    echo -e "  ${RED}  Strongly recommend seeking professional mental health evaluation${NC}"
    echo -e "  ${RED}  and treatment as soon as possible.${NC}"
  elif (( total_score >= TOTAL_THRESHOLD )); then
    echo -e "  ${YELLOW}${BOLD}● 提示PTSD可能${NC}"
    echo -e "  ${YELLOW}  建议寻求专业心理健康评估以确认诊断。${NC}"
    echo -e "  ${YELLOW}  Recommend seeking professional evaluation for confirmation.${NC}"
  elif (( total_score >= 20 )); then
    echo -e "  ${CYAN}${BOLD}● 亚临床症状${NC}"
    echo -e "  ${CYAN}  虽未达到PTSD筛查阈值，但存在一定症状。${NC}"
    echo -e "  ${CYAN}  建议关注自身心理健康，必要时寻求咨询。${NC}"
    echo -e "  ${CYAN}  Below threshold but some symptoms present. Consider counseling.${NC}"
  else
    echo -e "  ${GREEN}${BOLD}● 症状水平较低${NC}"
    echo -e "  ${GREEN}  当前筛查结果未显示明显的PTSD症状。${NC}"
    echo -e "  ${GREEN}  如仍有困扰，请随时寻求专业帮助。${NC}"
    echo -e "  ${GREEN}  Low symptom level. Seek help if still distressed.${NC}"
  fi

  # Cluster-specific recommendations
  echo ""
  high_clusters=()
  for cluster in B C D E; do
    max_possible=$(( CLUSTER_COUNT[$cluster] * 4 ))
    pct=$(( cluster_scores[$cluster] * 100 / max_possible ))
    if (( pct >= 60 )); then
      high_clusters+=("$cluster")
    fi
  done

  if (( ${#high_clusters[@]} > 0 )); then
    echo -e "  ${YELLOW}${BOLD}重点关注领域 / Elevated Clusters:${NC}"
    for hc in "${high_clusters[@]}"; do
      echo -e "    ▸ Cluster ${hc}: ${CLUSTER_PLAIN[$hc]}"
    done
    echo ""
  fi

  # ── Crisis Warning Check ───────────────────────────────────────────────
  # E2 (index 15, 0-based): 鲁莽或自毁行为 — triggers crisis warning
  # D5 (index 11, 0-based): 兴趣减退
  # D4 (index 10, 0-based): 持续负性情绪
  # E1 (index 14, 0-based): 易激惹或愤怒行为
  e2_score="${raw_scores[15]}"
  d5_score="${raw_scores[11]}"
  d4_score="${raw_scores[10]}"
  e1_score="${raw_scores[14]}"

  if (( e2_score >= 3 )); then
    echo ""
    print_double_line
    echo -e "${RED}${BOLD}"
    echo "    ╔══════════════════════════════════════════════════════════════╗"
    echo "    ║      ⚠  危机警告 / CRISIS WARNING  ⚠                      ║"
    echo "    ╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${RED}${BOLD}  您在「鲁莽或自毁行为」一项报告了较高水平的症状。${NC}"
    echo -e "${RED}${BOLD}  You reported elevated levels on 'reckless or self-destructive behavior'.${NC}"
    echo ""
    echo -e "${WHITE}${BOLD}  如果您或您认识的人正处于危机中，请立即联系：${NC}"
    echo -e "${WHITE}  If you or someone you know is in crisis, contact immediately:${NC}"
    echo ""
    echo -e "    🆘 全国心理援助热线: ${BOLD}400-161-9995${NC}"
    echo -e "    🆘 北京心理危机研究与干预中心: ${BOLD}010-82951332${NC}"
    echo -e "    🆘 生命热线: ${BOLD}400-821-1215${NC}"
    echo -e "    🆘 International Association for Suicide Prevention:"
    echo -e "       ${UNDERLINE}https://www.iasp.info/resources/Crisis_Centres/${NC}"
    echo ""
    print_double_line
  fi

  # ── Save Results ───────────────────────────────────────────────────────
  echo ""
  print_line
  echo -e "${BOLD}  正在保存结果... / Saving results...${NC}"

  {
    echo "================================================================"
    echo "PCL-5 评估结果 | PCL-5 Assessment Results"
    echo "================================================================"
    echo "日期/时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "筛查阈值: ${TOTAL_THRESHOLD}"
    echo ""
    echo "--- 各项评分 / Item Scores ---"
    item_idx=0
    for item_def in "${ITEMS[@]}"; do
      IFS='|' read -r id cluster text <<< "$item_def"
      echo "  ${id}: ${raw_scores[$item_idx]} - ${text}"
      item_idx=$((item_idx + 1))
    done
    echo ""
    echo "--- 症状群集得分 / Cluster Scores ---"
    for cluster in B C D E; do
      max_possible=$(( CLUSTER_COUNT[$cluster] * 4 ))
      echo "  Cluster ${cluster} (${CLUSTER_PLAIN[$cluster]}): ${cluster_scores[$cluster]} / ${max_possible}"
    done
    echo ""
    echo "--- 总分 / Total Score ---"
    echo "  ${total_score} / 80"
    if (( total_score >= TOTAL_THRESHOLD )); then
      echo "  结果: 提示PTSD可能 (Probable PTSD)"
    else
      echo "  结果: 未达到PTSD筛查阈值 (Below threshold)"
    fi
    echo ""
    echo "================================================================"
    echo "免责声明: 本工具仅为筛查工具，不构成临床诊断。"
    echo "DISCLAIMER: This is a screening tool only, not a clinical diagnosis."
    echo "================================================================"
  } > "$LOG_FILE"

  echo -e "  ${GREEN}✓ 结果已保存至: ${LOG_FILE}${NC}"
  echo ""

  # ── Final Summary ──────────────────────────────────────────────────────
  print_double_line
  echo -e "${DIM}"
  echo "  评估完成 | Assessment Complete"
  echo "  总分: ${total_score}/80"
  echo "  日志: ${LOG_FILE}"
  echo -e "${NC}"
  echo -e "${DIM}  注意: 本结果仅作为筛查参考，不替代专业临床评估。"
  echo -e "  Note: Results are for screening reference only and do not"
  echo -e "  replace professional clinical assessment.${NC}"
  echo ""
  print_double_line
  echo ""
}

# ── Run ──────────────────────────────────────────────────────────────────────
main "$@"
