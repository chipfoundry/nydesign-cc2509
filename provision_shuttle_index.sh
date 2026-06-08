#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./provision_shuttle_index.sh [--port /dev/cu.usbmodemXXXX] [--source path/to/index.json] [--shuttle shuttle_id]

Defaults:
  --source  ./ttsky25b_for_sdk204.json
  --shuttle ttsky25b
  --port    auto

Examples:
  ./provision_shuttle_index.sh
  ./provision_shuttle_index.sh --port /dev/cu.usbmodem3101
  ./provision_shuttle_index.sh --source ./my_index.json --shuttle ci2511
EOF
}

PORT="auto"
SOURCE="./ttsky25b_for_sdk204.json"
SHUTTLE_ID="ttsky25b"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)
      PORT="${2:-}"
      shift 2
      ;;
    --source)
      SOURCE="${2:-}"
      shift 2
      ;;
    --shuttle)
      SHUTTLE_ID="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ ! -f "$SOURCE" ]]; then
  echo "Source JSON not found: $SOURCE" >&2
  exit 1
fi

if ! command -v mpremote >/dev/null 2>&1; then
  echo "mpremote is not installed. Install with: python3 -m pip install --user mpremote" >&2
  exit 1
fi

TARGET_NAME="${SHUTTLE_ID}.json"
CONNECT_ARGS=(connect "$PORT")

echo "Provisioning shuttle index..."
echo "  port:    $PORT"
echo "  source:  $SOURCE"
echo "  target:  :/shuttles/$TARGET_NAME"

# Ensure shuttles directory exists.
mpremote "${CONNECT_ARGS[@]}" fs mkdir :/shuttles || true

# Copy source file to the board.
mpremote "${CONNECT_ARGS[@]}" fs cp "$SOURCE" ":/shuttles/$TARGET_NAME"

# Verify file exists and print directory listing.
mpremote "${CONNECT_ARGS[@]}" fs ls :/shuttles
mpremote "${CONNECT_ARGS[@]}" exec "import os; print('exists:', '$TARGET_NAME' in os.listdir('/shuttles'))"

# Reset board to apply changes cleanly.
mpremote "${CONNECT_ARGS[@]}" reset

echo "Done."
