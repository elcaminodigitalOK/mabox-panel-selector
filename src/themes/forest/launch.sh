#!/usr/bin/env bash

# Script para lanzar polybar con el tema forest

# Terminar instancias en ejecución
killall -q polybar

# Esperar a que los procesos se cierren
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

# Lanzar la barra
polybar -q main -c "$HOME/.config/polybar/forest/config" &
