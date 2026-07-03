#!/usr/bin/env bash
set -euo pipefail

PID_FILE="tmp/server.pid"
PORT_FILE="tmp/server.port"
LOG_FILE="tmp/server.log"
DEFAULT_PORT="8000"

ensure_tmp() {
  mkdir -p tmp
}

is_running() {
  local pid="${1:-}"
  [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null
}

current_pid() {
  if [ -f "$PID_FILE" ]; then
    cat "$PID_FILE"
  fi
}

current_port() {
  if [ -f "$PORT_FILE" ]; then
    cat "$PORT_FILE"
  else
    printf '%s' "$DEFAULT_PORT"
  fi
}

start_server() {
  local port="${1:-$DEFAULT_PORT}"
  ensure_tmp

  local pid
  pid="$(current_pid || true)"
  if is_running "$pid"; then
    printf 'Server already running: http://localhost:%s\n' "$(current_port)"
    return 0
  fi

  rm -f "$PID_FILE" "$PORT_FILE"
  (trap '' HUP; exec nohup python3 -m http.server "$port" --directory docs > "$LOG_FILE" 2>&1) &
  pid="$!"
  disown "$pid" 2>/dev/null || true
  printf '%s' "$pid" > "$PID_FILE"
  printf '%s' "$port" > "$PORT_FILE"

  sleep 1
  if ! is_running "$pid"; then
    printf 'Server failed to start. See %s\n' "$LOG_FILE" >&2
    rm -f "$PID_FILE" "$PORT_FILE"
    return 1
  fi

  printf 'Server running: http://localhost:%s\n' "$port"
}

server_status() {
  ensure_tmp
  local pid
  pid="$(current_pid || true)"
  if is_running "$pid"; then
    printf 'Server running: http://localhost:%s\n' "$(current_port)"
  else
    printf 'Server not running.\n'
    rm -f "$PID_FILE" "$PORT_FILE"
  fi
}

stop_server() {
  ensure_tmp
  local pid
  pid="$(current_pid || true)"
  if ! is_running "$pid"; then
    printf 'Server not running.\n'
    rm -f "$PID_FILE" "$PORT_FILE"
    return 0
  fi

  kill "$pid"
  wait "$pid" 2>/dev/null || true
  rm -f "$PID_FILE" "$PORT_FILE"
  printf 'Server stopped.\n'
}

case "${1:-}" in
  start)
    start_server "${2:-$DEFAULT_PORT}"
    ;;
  status)
    server_status
    ;;
  stop)
    stop_server
    ;;
  *)
    printf 'Usage: ./serve.sh start [port] | status | stop\n' >&2
    exit 1
    ;;
esac
