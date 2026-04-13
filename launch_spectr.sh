#!/bin/bash
cd ~/WebstormProjects/SPECTR-Ultimate

# Set app name for GNOME BEFORE launching
export GDK_BACKEND=x11
export FLET_APP_NAME="SPECTR"

# Launch and immediately set icon
python3 gui_flet.py &
PID=$!

# Background icon setter
(
  sleep 1
  for i in {1..20}; do
    WID=$(xdotool search --pid $PID 2>/dev/null | tail -1)
    if [ -n "$WID" ]; then
      /snap/bin/xseticon -id "$WID" ~/WebstormProjects/SPECTR-Ultimate/ui/icon_spectr.png
      
      # Also set window properties
      xprop -id "$WID" -f WM_CLASS 8s -set WM_CLASS "SPECTR"
      xprop -id "$WID" -f _NET_WM_NAME 8u -set _NET_WM_NAME "SPECTR"
      
      break
    fi
    sleep 0.3
  done
) &

wait $PID
