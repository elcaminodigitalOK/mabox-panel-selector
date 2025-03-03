ESTA APLICACION TODABIA ESTA EN CONSTRUCCION, USESE BAJO SU PROPIA RESPONSABILIDAD.

# Selector de Paneles para Mabox Linux

Una herramienta para elegir y configurar el panel de Mabox Linux entre tint2 (predeterminado) y polybar.

## Características

- Cambio fácil entre tint2 y polybar
- Configuración de temas para polybar
- Edición de configuraciones
- Importación de nuevos temas
- Integración con Mabox Linux

## Instalación

 + clonar repositorio 
 + git clone https://github.com/elcaminodigitalOK/mabox-panel-selector.git
 + cd mabox-panel-selector
 + chmod +x src/*.py src/*.sh
 + makepkg -f
 + ejecutar la aplicacion con el comando "mabox-panel-selector"
   

## Desinstalacion

  + sudo pacman -R mabox-panel-selector
  + borrar archivos residuales :
    + sudo rm -rf /usr/share/mabox-panel-selector
sudo rm -f /usr/bin/mabox-panel-selector
sudo rm -f /usr/share/applications/mabox-panel-selector.desktop





## Créditos

Desarrollado para la comunidad de Mabox Linux.

## Licencia

Este proyecto está licenciado bajo GPL v3.
