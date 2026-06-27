#!/bin/bash
# Waits for cloudflared to spit out the URL, then saves it to a file

URL_FILE="/home/baseer/servo_camera_project/tunnel_url.txt"
LOG_FILE="/home/baseer/servo_camera_project/tunnel.log"

# Clear old file
> "$URL_FILE"

# Run cloudflared, grep for the URL, and save it. Run in background.
cloudflared tunnel --url http://localhost:5000 2>&1 | grep --line-buffered "trycloudflare.com" | sed 's/.*\(https[^ ]*\).*/\1/' > "$URL_FILE" &
TUNNEL_PID=$!

# Keep the script running so systemd doesn't kill it
wait $TUNNEL_PID
