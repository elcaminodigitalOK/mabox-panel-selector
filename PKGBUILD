# Maintainer: Nitro <cd.galeano.ec@gmail.com>
pkgname=mabox-panel-selector
pkgver=0.1.0
pkgrel=1
pkgdesc="Selector de paneles para Mabox Linux"
arch=('any')
# url="https://github.com/tuusuario/mabox-panel-selector" (repo aun no creado)
license=('GPL')
depends=('python' 'python-pyqt5' 'tint2' 'openbox')
optdepends=('polybar: soporte para polybar')

package() {
  # Verificar la ubicación actual
  echo "Directorio actual: $(pwd)"
  
  # Crear directorios con verificación de errores
  echo "Creando directorios de instalación..."
  mkdir -p "$pkgdir/usr/bin" || { echo "Error al crear $pkgdir/usr/bin"; exit 1; }
  mkdir -p "$pkgdir/usr/share/$pkgname" || { echo "Error al crear $pkgdir/usr/share/$pkgname"; exit 1; }
  mkdir -p "$pkgdir/usr/share/applications" || { echo "Error al crear $pkgdir/usr/share/applications"; exit 1; }
  
  # Verificar archivos esenciales
  if [ ! -f "panel_selector.py" ]; then
    echo "Error: No se encuentra el archivo 'panel_selector.py'. Abortando."
    exit 1
  fi
  
  # Copiar todos los archivos al directorio de instalación
  echo "Copiando archivos de la aplicación..."
  cp -r * "$pkgdir/usr/share/$pkgname/" || { echo "Error al copiar archivos"; exit 1; }
  
  # Hacer ejecutables los scripts con verificación
  echo "Configurando permisos de ejecución..."
  if ls "$pkgdir/usr/share/$pkgname/"*.py >/dev/null 2>&1; then
    chmod +x "$pkgdir/usr/share/$pkgname/"*.py || { echo "Error al configurar permisos de scripts Python"; exit 1; }
  else
    echo "Advertencia: No se encontraron archivos Python para hacer ejecutables."
  fi
  
  if ls "$pkgdir/usr/share/$pkgname/"*.sh >/dev/null 2>&1; then
    chmod +x "$pkgdir/usr/share/$pkgname/"*.sh || { echo "Error al configurar permisos de scripts Bash"; exit 1; }
  else
    echo "Advertencia: No se encontraron scripts Bash para hacer ejecutables."
  fi
  
  # Crear script wrapper para manejar la importación de PyQt5
  echo "Creando script wrapper..."
  cat > "$pkgdir/usr/bin/$pkgname" << EOL || { echo "Error al crear script wrapper"; exit 1; }
#!/bin/bash
# Script wrapper para mabox-panel-selector

# Configurar PYTHONPATH para incluir las ubicaciones del sistema
export PYTHONPATH="/usr/lib/python3.13/site-packages:\$PYTHONPATH"

# Ejecutar la aplicación
python /usr/share/$pkgname/panel_selector.py "\$@"
EOL

  # Hacer ejecutable el script wrapper
  chmod +x "$pkgdir/usr/bin/$pkgname" || { echo "Error al configurar permisos del script wrapper"; exit 1; }
  
  # Instalar archivo de escritorio
  echo "Creando entrada en el menú de aplicaciones..."
  cat > "$pkgdir/usr/share/applications/$pkgname.desktop" << EOL || { echo "Error al crear archivo .desktop"; exit 1; }
[Desktop Entry]
Name=Selector de Paneles
Comment=Selecciona y configura el panel para Mabox Linux
Exec=$pkgname
Icon=preferences-desktop
Terminal=false
Type=Application
Categories=Settings;DesktopSettings;
StartupNotify=false
EOL

  echo "Instalación completada con éxito."
}