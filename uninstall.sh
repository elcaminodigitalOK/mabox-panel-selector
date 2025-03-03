#!/bin/bash

# Script de desinstalación para el Selector de Paneles Mabox
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
NC="\033[0m" # No Color

echo -e "${YELLOW}===== Desinstalador del Selector de Paneles Mabox =====${NC}"
echo ""

# Verificar si está instalado
if [ ! -d ~/.local/share/mabox-panel-selector ]; then
    echo -e "${RED}El Selector de Paneles no parece estar instalado.${NC}"
    exit 1
fi

# Preguntar confirmación
read -p "¿Está seguro de que desea desinstalar el Selector de Paneles? (s/n): " answer
if [[ ! "$answer" =~ ^[Ss]$ ]]; then
    echo "Desinstalación cancelada."
    exit 0
fi

# Eliminar archivos
echo -e "${YELLOW}Eliminando archivos...${NC}"
rm -rf ~/.local/share/mabox-panel-selector
rm -f ~/.local/bin/mabox-panel-selector
rm -f ~/.local/share/applications/mabox-panel-selector.desktop

echo -e "${GREEN}Desinstalación completada.${NC}"
echo -e "Nota: No se han eliminado las configuraciones de polybar en ~/.config/polybar"