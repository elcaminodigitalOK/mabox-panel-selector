#!/bin/bash

# Script para restaurar tint2 como panel por defecto en Mabox Linux
AUTOSTART_FILE="$HOME/.config/openbox/autostart"
BACKUP_FILE="$HOME/.config/openbox/autostart.bak.$(date +%Y%m%d%H%M%S)"

# Crear copia de seguridad del archivo autostart
echo "Creando copia de seguridad del archivo autostart..."
cp "$AUTOSTART_FILE" "$BACKUP_FILE"

# Descomentar todas las líneas que contengan tint2
echo "Modificando el archivo autostart..."
sed -i 's/^#\(.*tint2.*\)$/\1/' "$AUTOSTART_FILE"

# Comentar todas las líneas que contengan polybar
sed -i 's/^.*polybar.*$/#&/' "$AUTOSTART_FILE"

# Detener polybar inmediatamente
echo "Deteniendo polybar..."
killall polybar 2>/dev/null

# Iniciar tint2 inmediatamente
echo "Iniciando tint2..."
tint2 &

echo "Configuración cambiada correctamente. Tint2 ha sido restaurado."

# Opcional: reiniciar Openbox automáticamente
openbox --reconfigure

exit 0