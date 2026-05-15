#!/usr/bin/env bash
#
# Peace Lab Database — MkDocs Serve Manager
# 生产级本地服务启动/停止/构建脚本
#
# Usage:
#   ./serve.sh start           后台启动 mkdocs serve (热重载)
#   ./serve.sh start --dirty   快速启动：跳过 site/ 清理（增量构建）
#   ./serve.sh start --dev     开发模式：禁用 mermaid2，最快启动
#   ./serve.sh stop            停止服务
#   ./serve.sh restart         重启服务
#   ./serve.sh status          查看服务状态
#   ./serve.sh build           生产构建
#   ./serve.sh build --dirty   增量构建（保留已有 site/）
#   ./serve.sh preview         秒开预览（仅 HTTP 服务已构建的 site/）
#

set -euo pipefail

# ------------------------------------------------------------------
# 配置
# ------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
DOCS_DIR="${REPO_ROOT}/Web/mkdocs"
SITE_DIR="${REPO_ROOT}/site"
LOG_DIR="${REPO_ROOT}/logs"
PID_FILE="${LOG_DIR}/mkdocs.pid"
LOG_FILE="${LOG_DIR}/mkdocs.log"
ACCESS_LOG="${LOG_DIR}/access.log"
DEV_CONFIG="${REPO_ROOT}/mkdocs-dev.yml"

VENV_DIR="${REPO_ROOT}/.venv"
HOST="127.0.0.1"
PORT="8000"

# 颜色
C_RESET='\033[0m'
C_GREEN='\033[0;32m'
C_RED='\033[0;31m'
C_YELLOW='\033[0;33m'
C_BLUE='\033[0;34m'
C_DIM='\033[0;90m'

# ------------------------------------------------------------------
# 工具函数
# ------------------------------------------------------------------
log_info()  { echo -e "${C_BLUE}[INFO]${C_RESET}  $*"; }
log_ok()    { echo -e "${C_GREEN}[OK]${C_RESET}    $*"; }
log_warn()  { echo -e "${C_YELLOW}[WARN]${C_RESET}  $*"; }
log_error() { echo -e "${C_RED}[ERROR]${C_RESET} $*"; }
log_dim()   { echo -e "${C_DIM}$*${C_RESET}"; }

die() { log_error "$*"; exit 1; }

ensure_dir() {
    if [[ ! -d "$1" ]]; then
        mkdir -p "$1"
    fi
}

check_port() {
    local port="$1"
    if command -v lsof >/dev/null 2>&1; then
        lsof -Pi ":${port}" -sTCP:LISTEN -t >/dev/null 2>&1
    elif command -v netstat >/dev/null 2>&1; then
        netstat -tlnp 2>/dev/null | grep -q ":${port} "
    elif command -v ss >/dev/null 2>&1; then
        ss -tlnp 2>/dev/null | grep -q ":${port} "
    else
        return 1
    fi
}

activate_venv() {
    if [[ -f "${VENV_DIR}/bin/activate" ]]; then
        # shellcheck source=/dev/null
        source "${VENV_DIR}/bin/activate"
    else
        die "虚拟环境不存在: ${VENV_DIR}"
    fi
}

check_deps() {
    if ! command -v python3 >/dev/null 2>&1; then
        die "未安装 python3"
    fi

    activate_venv

    if ! command -v mkdocs >/dev/null 2>&1; then
        die "mkdocs 未安装，请先运行: pip install -r requirements.txt"
    fi
}

read_pid() {
    if [[ -f "$PID_FILE" ]]; then
        cat "$PID_FILE"
    else
        echo ""
    fi
}

is_running() {
    local pid
    pid="$(read_pid)"
    [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

wait_for_server() {
    local max_wait="${1:-60}"
    local waited=0
    log_info "等待服务就绪 (最多 ${max_wait}s)..."
    while ! curl -sf "http://${HOST}:${PORT}/" >/dev/null 2>&1; do
        sleep 1
        waited=$((waited + 1))
        if [[ $waited -ge $max_wait ]]; then
            log_warn "服务启动超时，请检查日志: ${LOG_FILE}"
            return 1
        fi
    done
    log_ok "服务已就绪"
    return 0
}

generate_dev_config() {
    # 生成简化版配置：禁用 mermaid2 插件，减少构建时间
    if [[ ! -f "$DEV_CONFIG" ]] || [[ "${REPO_ROOT}/mkdocs.yml" -nt "$DEV_CONFIG" ]]; then
        # 去掉 mermaid2 插件行
        sed '/^[[:space:]]*- mermaid2:/,/^[[:space:]]*theme: neutral$/d' \
            "${REPO_ROOT}/mkdocs.yml" > "$DEV_CONFIG"
        log_dim "已生成开发配置: ${DEV_CONFIG} (禁用 mermaid2)"
    fi
}

# ------------------------------------------------------------------
# 命令实现
# ------------------------------------------------------------------

cmd_start() {
    local use_dirty=false
    local use_dev=false

    for arg in "$@"; do
        case "$arg" in
            --dirty|-d) use_dirty=true ;;
            --dev)      use_dev=true ;;
        esac
    done

    if is_running; then
        log_warn "服务已在运行 (PID: $(read_pid))"
        log_info "访问地址: http://${HOST}:${PORT}/"
        return 0
    fi

    if check_port "$PORT"; then
        die "端口 ${PORT} 已被占用，请检查是否有其他 mkdocs serve 在运行"
    fi

    check_deps
    ensure_dir "$LOG_DIR"

    local mkdocs_args=(serve --dev-addr "${HOST}:${PORT}")

    if [[ "$use_dirty" == true ]]; then
        mkdocs_args+=(--dirty)
        log_info "快速启动模式 (--dirty): 跳过 site/ 清理"
    fi

    if [[ "$use_dev" == true ]]; then
        generate_dev_config
        mkdocs_args+=(-f "$DEV_CONFIG")
        log_info "开发模式: 禁用 mermaid2 插件，最快启动"
    fi

    log_info "启动 mkdocs ${mkdocs_args[*]}..."
    log_info "日志文件: ${LOG_FILE}"

    cd "$REPO_ROOT"
    nohup mkdocs "${mkdocs_args[@]}" >> "$LOG_FILE" 2>&1 &

    local pid=$!
    echo "$pid" > "$PID_FILE"

    if ! wait_for_server 120; then
        log_warn "服务可能仍在启动中，稍后请用 './serve.sh status' 检查"
    fi

    log_ok "服务已启动 (PID: $pid)"
    log_info "访问地址: http://${HOST}:${PORT}/"
    log_info "停止命令: ./serve.sh stop"
}

cmd_stop() {
    if ! is_running; then
        log_warn "服务未在运行"
        rm -f "$PID_FILE"
        return 0
    fi

    local pid
    pid="$(read_pid)"
    log_info "停止服务 (PID: $pid)..."

    kill "$pid" 2>/dev/null || true
    local waited=0
    while kill -0 "$pid" 2>/dev/null && [[ $waited -lt 10 ]]; do
        sleep 1
        waited=$((waited + 1))
    done

    if kill -0 "$pid" 2>/dev/null; then
        log_warn "强制终止进程..."
        kill -9 "$pid" 2>/dev/null || true
    fi

    rm -f "$PID_FILE"
    log_ok "服务已停止"
}

cmd_restart() {
    cmd_stop
    sleep 1
    cmd_start "$@"
}

cmd_status() {
    if is_running; then
        local pid
        pid="$(read_pid)"
        log_ok "服务运行中 (PID: $pid)"
        log_info "访问地址: http://${HOST}:${PORT}/"
        log_info "日志文件: ${LOG_FILE}"

        if check_port "$PORT"; then
            log_ok "端口 ${PORT} 监听正常"
        else
            log_warn "端口 ${PORT} 未监听，服务可能正在启动中"
        fi
    else
        log_warn "服务未运行"
        if [[ -f "$PID_FILE" ]]; then
            log_info "发现残留 PID 文件，已清理"
            rm -f "$PID_FILE"
        fi
    fi
}

cmd_build() {
    local use_dirty=false
    for arg in "$@"; do
        case "$arg" in
            --dirty|-d) use_dirty=true ;;
        esac
    done

    check_deps
    ensure_dir "$LOG_DIR"

    local mkdocs_args=(build)
    if [[ "$use_dirty" == true ]]; then
        mkdocs_args+=(--dirty)
        log_info "增量构建模式 (--dirty): 保留已有 site/"
    fi

    log_info "开始构建..."
    log_info "构建日志: ${LOG_FILE}"

    cd "$REPO_ROOT"
    if mkdocs "${mkdocs_args[@]}" >> "$LOG_FILE" 2>&1; then
        log_ok "构建成功: ${SITE_DIR}/"
    else
        die "构建失败，请检查日志: ${LOG_FILE}"
    fi
}

cmd_preview() {
    if [[ ! -f "${SITE_DIR}/index.html" ]]; then
        log_warn "未找到构建产物: ${SITE_DIR}/index.html"
        log_info "建议先运行以下命令之一："
        log_dim "  ./serve.sh build       # 完整构建 (~15min)"
        log_dim "  ./serve.sh build --dirty   # 增量构建 (若已有 site/)"
        log_dim "  ./serve.sh start --dev   # 开发模式启动 (~5-8min)"
        return 1
    fi

    if is_running; then
        log_warn "服务已在运行"
        log_info "访问地址: http://${HOST}:${PORT}/"
        return 0
    fi

    if check_port "$PORT"; then
        die "端口 ${PORT} 已被占用"
    fi

    log_info "启动静态文件预览 (秒开，无热重载)..."
    cd "$SITE_DIR"
    nohup python3 -m http.server "$PORT" --bind "$HOST" >> "$ACCESS_LOG" 2>&1 &
    local pid=$!
    echo "$pid" > "$PID_FILE"

    sleep 1
    if curl -sf "http://${HOST}:${PORT}/" >/dev/null 2>&1; then
        log_ok "预览服务已启动"
        log_info "访问地址: http://${HOST}:${PORT}/"
        log_info "特点: 秒开、无热重载、基于已有 site/ 目录"
    else
        log_warn "预览服务可能正在启动中"
    fi
}

cmd_help() {
    cat <<EOF
Peace Lab Database — MkDocs 服务管理脚本

Usage:
  ./serve.sh start               标准启动 mkdocs serve (热重载)
  ./serve.sh start --dirty       快速启动：跳过 site/ 清理（增量构建）
  ./serve.sh start --dev         开发模式：禁用 mermaid2，最快启动
  ./serve.sh stop                停止服务
  ./serve.sh restart             重启服务
  ./serve.sh status              查看服务状态
  ./serve.sh build               生产构建到 site/
  ./serve.sh build --dirty       增量构建（保留已有 site/）
  ./serve.sh preview             秒开预览（需先 build，无热重载）

效率建议:
  1. 首次: ./serve.sh build --dirty  # 构建一次
     之后: ./serve.sh preview        # 秒开预览
  2. 开发: ./serve.sh start --dev    # 最快热重载 (~5-8min)
  3. 标准: ./serve.sh start --dirty  # 增量启动 (~10-12min)

Environment:
  REPO_ROOT  ${REPO_ROOT}
  LOG_DIR    ${LOG_DIR}
  HOST       ${HOST}
  PORT       ${PORT}
EOF
}

# ------------------------------------------------------------------
# 主入口
# ------------------------------------------------------------------
main() {
    local cmd="${1:-help}"
    shift 2>/dev/null || true

    case "$cmd" in
        start)   cmd_start "$@" ;;
        stop)    cmd_stop ;;
        restart) cmd_restart "$@" ;;
        status)  cmd_status ;;
        build)   cmd_build "$@" ;;
        preview) cmd_preview ;;
        help|--help|-h) cmd_help ;;
        *) die "未知命令: $cmd"; cmd_help; exit 1 ;;
    esac
}

main "$@"
