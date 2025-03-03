#!/usr/bin/env bash

MENU="$(rofi -no-config -no-lazy-grab -sep "|" -dmenu -i -p '' \
-theme ~/.config/polybar/scripts/rofi/powermenu.rasi \
<<< " Bloquear| Cerrar sesión| Reiniciar| Apagar")"
    case "$MENU" in
        *Bloquear) i3lock-fancy ;;
        *Cerrar*sesión) openbox --exit ;;
        *Reiniciar) systemctl reboot ;;
        *Apagar) systemctl poweroff ;;
    esac
