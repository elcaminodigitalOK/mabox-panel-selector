#!/bin/bash

# Script de instalación para el Selector de Paneles Mabox
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
NC="\033[0m" # No Color

echo -e "${GREEN}===== Instalador del Selector de Paneles Mabox =====${NC}"
echo ""

# Verificar dependencias
echo -e "${YELLOW}Verificando dependencias...${NC}"
DEPS=("python" "python-pyqt5" "tint2")
MISSING=()

for dep in "${DEPS[@]}"; do
    if ! pacman -Q "$dep" &> /dev/null; then
        MISSING+=("$dep")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo -e "${RED}Faltan las siguientes dependencias: ${MISSING[*]}${NC}"
    read -p "¿Desea instalarlas ahora? (s/n): " answer
    if [[ "$answer" =~ ^[Ss]$ ]]; then
        sudo pacman -S --noconfirm "${MISSING[@]}"
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error al instalar dependencias. Abortando.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}No se pueden instalar las dependencias. Abortando.${NC}"
        exit 1
    fi
fi

# Crear directorios
echo -e "${YELLOW}Creando directorios de la aplicación...${NC}"
mkdir -p ~/.local/share/mabox-panel-selector/resources
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications

# Copiar archivos de la aplicación
echo -e "${YELLOW}Copiando archivos...${NC}"
INSTALL_DIR=~/.local/share/mabox-panel-selector
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")/src"

# Copiar archivos Python y scripts bash
cp "$SCRIPT_DIR"/*.py "$INSTALL_DIR"/ || exit 1
cp "$SCRIPT_DIR"/*.sh "$INSTALL_DIR"/ || exit 1

# Copiar temas predeterminados
mkdir -p "$INSTALL_DIR/themes"
cp -r "$SCRIPT_DIR/themes"/* "$INSTALL_DIR/themes"/ || echo "No se encontraron temas para copiar"

# Crear o copiar imágenes de vista previa
mkdir -p "$INSTALL_DIR/resources"
if [ -d "$SCRIPT_DIR/resources" ]; then
    cp -r "$SCRIPT_DIR/resources"/* "$INSTALL_DIR/resources"/ || echo "No se encontraron recursos para copiar"
else
    echo -e "${YELLOW}Creando imágenes de vista previa predeterminadas...${NC}"
    # Crear imágenes de vista previa simples si no existen
    convert -size 300x200 xc:lightblue -gravity center -pointsize 20 -annotate 0 "Vista previa de Tint2" "$INSTALL_DIR/resources/tint2_preview.png" 2>/dev/null || \
    echo "No se pudo crear imagen de vista previa para tint2. Se usará un icono genérico."
    
    convert -size 300x200 xc:lightgreen -gravity center -pointsize 20 -annotate 0 "Vista previa de Polybar" "$INSTALL_DIR/resources/polybar_preview.png" 2>/dev/null || \
    echo "No se pudo crear imagen de vista previa para polybar. Se usará un icono genérico."
fi

# Hacer ejecutables los scripts
chmod +x "$INSTALL_DIR"/*.py
chmod +x "$INSTALL_DIR"/*.sh

# Crear enlace simbólico
ln -sf "$INSTALL_DIR/panel_selector.py" ~/.local/bin/mabox-panel-selector

# Crear entrada en el menú
cat > ~/.local/share/applications/mabox-panel-selector.desktop << EOL
[Desktop Entry]
Name=Selector de Paneles
Comment=Selecciona y configura el panel para Mabox Linux
Exec=mabox-panel-selector
Icon=preferences-desktop
Terminal=false
Type=Application
Categories=Settings;DesktopSettings;
StartupNotify=false
EOL

echo -e "${GREEN}¡Instalación completada!${NC}"
echo -e "Puede iniciar el selector de paneles desde el menú o ejecutando 'mabox-panel-selector'"

# Preguntar si desea iniciar ahora
read -p "¿Desea iniciar el selector de paneles ahora? (s/n): " answer
if [[ "$answer" =~ ^[Ss]$ ]]; then
    ~/.local/bin/mabox-panel-selector
fi