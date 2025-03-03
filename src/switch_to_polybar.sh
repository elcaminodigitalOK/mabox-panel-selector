#!/bin/bash

# Script para cambiar de tint2 a polybar en Mabox Linux
AUTOSTART_FILE="$HOME/.config/openbox/autostart"
BACKUP_FILE="$HOME/.config/openbox/autostart.bak.$(date +%Y%m%d%H%M%S)"

# Verificar si polybar está instalado
if ! command -v polybar &> /dev/null; then
    echo "Polybar no está instalado. Instalando..."
    sudo pacman -S --noconfirm polybar
    
    if [ $? -ne 0 ]; then
        echo "Error al instalar polybar. Abortando."
        exit 1
    fi
fi

# Crear copia de seguridad del archivo autostart
echo "Creando copia de seguridad del archivo autostart..."
cp "$AUTOSTART_FILE" "$BACKUP_FILE"

# Comentar todas las líneas que contengan tint2
echo "Modificando el archivo autostart..."
sed -i 's/^.*tint2.*$/#&/' "$AUTOSTART_FILE"

# Verificar si polybar ya está en el archivo autostart
if grep -q "polybar" "$AUTOSTART_FILE"; then
    echo "Polybar ya está configurado en autostart."
else
    # Agregar polybar al final del archivo
    echo "" >> "$AUTOSTART_FILE"
    echo "# Polybar" >> "$AUTOSTART_FILE"
    echo "[ -x /usr/bin/polybar ] && polybar main &" >> "$AUTOSTART_FILE"
fi

# Detener tint2 inmediatamente
echo "Deteniendo tint2..."
killall tint2 2>/dev/null

# Iniciar polybar inmediatamente
echo "Iniciando polybar..."
mkdir -p "$HOME/.config/polybar"

# Verificar si existe una configuración de polybar
if [ ! -f "$HOME/.config/polybar/config" ]; then
    # Usar configuración por defecto
    echo "Copiando configuración por defecto..."
    cp "/usr/share/mabox-panel-selector/themes/default/config.ini" "$HOME/.config/polybar/config"
fi

# Iniciar polybar
polybar main &

echo "Configuración cambiada correctamente. Polybar ha sido iniciado."

# Opcional: reiniciar Openbox automáticamente
openbox --reconfigure

exit 0