#!/usr/bin/env python3

import os
import sys
import subprocess
import site
import importlib.util

# Función para verificar si un módulo está instalado
def is_module_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

# Función para intentar importar PyQt5 de diferentes maneras
def import_pyqt5():
    # Intento 1: Importación directa
    try:
        from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                    QHBoxLayout, QLabel, QPushButton, QRadioButton,
                                    QButtonGroup, QDialog, QMessageBox, QFrame, QInputDialog, QLineEdit)
        from PyQt5.QtGui import QIcon, QPixmap, QFont, QPainter, QColor
        from PyQt5.QtCore import Qt, QProcess
        return True
    except ImportError:
        pass

    # Intento 2: Buscar en rutas adicionales
    try:
        site_packages = site.getsitepackages()
        for path in site_packages:
            if path not in sys.path:
                sys.path.append(path)

        from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                    QHBoxLayout, QLabel, QPushButton, QRadioButton,
                                    QButtonGroup, QDialog, QMessageBox, QFrame, QInputDialog, QLineEdit)
        from PyQt5.QtGui import QIcon, QPixmap, QFont, QPainter, QColor
        from PyQt5.QtCore import Qt, QProcess
        return True
    except ImportError:
        pass

    # Intento 3: Buscar en el entorno virtual si existe
    try:
        venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'myenv')
        if os.path.exists(venv_path):
            venv_site_packages = os.path.join(venv_path, 'lib', 'python3.13', 'site-packages')
            if os.path.exists(venv_site_packages) and venv_site_packages not in sys.path:
                sys.path.append(venv_site_packages)

            from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                        QHBoxLayout, QLabel, QPushButton, QRadioButton,
                                        QButtonGroup, QDialog, QMessageBox, QFrame, QInputDialog, QLineEdit)
            from PyQt5.QtGui import QIcon, QPixmap, QFont, QPainter, QColor
            from PyQt5.QtCore import Qt, QProcess
            return True
    except ImportError:
        pass

    # Si llegamos aquí, no se pudo importar PyQt5
    return False

# Intentar importar PyQt5
if not import_pyqt5():
    print("PyQt5 no está instalado. Intentando instalar...")
    try:
        subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "python-pyqt5"], check=True)
        if not import_pyqt5():
            print("No se pudo instalar PyQt5. Por favor, instálalo manualmente con 'sudo pacman -S python-pyqt5'")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("No se pudo instalar PyQt5. Por favor, instálalo manualmente con 'sudo pacman -S python-pyqt5'")
        sys.exit(1)

# Ahora que PyQt5 está importado, podemos importar los módulos específicos
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QPushButton, QRadioButton,
                            QButtonGroup, QDialog, QMessageBox, QFrame, QInputDialog, QLineEdit)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPainter, QColor
from PyQt5.QtCore import Qt, QProcess

# Determinar las rutas correctas según la instalación
if os.path.exists("/usr/share/mabox-panel-selector"):
    # Instalación del sistema
    BASE_DIR = "/usr/share/mabox-panel-selector"
else:
    # Desarrollo local
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Constantes
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
THEMES_DIR = os.path.join(BASE_DIR, "themes")
TINT2_PREVIEW = os.path.join(RESOURCES_DIR, "tint2_preview.png")
POLYBAR_PREVIEW = os.path.join(RESOURCES_DIR, "polybar_preview.png")
TINT2_CONFIG_PATH = "/usr/bin/tint2conf"
SWITCH_POLYBAR_SCRIPT = os.path.join(BASE_DIR, "switch_to_polybar.sh")
RESTORE_TINT2_SCRIPT = os.path.join(BASE_DIR, "restore_tint2.sh")

# Crear imágenes de vista previa genéricas si no existen
def create_generic_preview_images():
    if not os.path.exists(RESOURCES_DIR):
        os.makedirs(RESOURCES_DIR, exist_ok=True)

    if not os.path.exists(TINT2_PREVIEW):
        create_generic_image(TINT2_PREVIEW, "Tint2 Panel", (300, 200), (100, 150, 200))

    if not os.path.exists(POLYBAR_PREVIEW):
        create_generic_image(POLYBAR_PREVIEW, "Polybar Panel", (300, 200), (200, 100, 150))

def create_generic_image(path, text, size, color):
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', size, color=color)
        draw = ImageDraw.Draw(img)
        # Usar una fuente predeterminada
        try:
            font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", 20)
        except:
            font = ImageFont.load_default()

        # Dibujar texto en el centro
        try:
            # Para versiones más recientes de PIL
            text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
        except AttributeError:
            # Para versiones antiguas de PIL
            try:
                text_width, text_height = draw.textsize(text, font=font)
            except:
                text_width, text_height = len(text) * 10, 20  # Estimación aproximada

        position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
        draw.text(position, text, fill=(255, 255, 255), font=font)

        # Guardar imagen
        img.save(path)
        print(f"Imagen de vista previa creada: {path}")
    except Exception as e:
        print(f"No se pudo crear la imagen de vista previa: {e}")
        # Crear un archivo vacío para evitar errores futuros
        with open(path, 'w') as f:
            f.write("")

class PanelSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Crear imágenes de vista previa si no existen
        create_generic_preview_images()

        # Configuración de la ventana principal
        self.setWindowTitle("Selector de Paneles - Mabox Linux")
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(500, 350)

        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Título
        title_label = QLabel("Selector de Paneles para Mabox Linux")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Sans", 14, QFont.Bold))
        main_layout.addWidget(title_label)

        # Descripción
        desc_label = QLabel("Selecciona y configura el panel que deseas utilizar en tu sistema.")
        desc_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc_label)

        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)

        # Contenedor para los paneles
        panels_container = QWidget()
        panels_layout = QHBoxLayout(panels_container)

        # Panel Tint2
        tint2_widget = QWidget()
        tint2_layout = QVBoxLayout(tint2_widget)

        # Vista previa de Tint2
        tint2_preview_label = QLabel()
        if os.path.exists(TINT2_PREVIEW) and os.path.getsize(TINT2_PREVIEW) > 0:
            tint2_pixmap = QPixmap(TINT2_PREVIEW)
            tint2_preview_label.setPixmap(tint2_pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            tint2_preview_label.setText("Vista previa no disponible")
        tint2_preview_label.setAlignment(Qt.AlignCenter)
        tint2_layout.addWidget(tint2_preview_label)

        # Radio button para Tint2
        self.tint2_radio = QRadioButton("Tint2")
        self.tint2_radio.setFont(QFont("Sans", 12, QFont.Bold))
        tint2_layout.addWidget(self.tint2_radio, alignment=Qt.AlignCenter)

        # Descripción de Tint2
        tint2_desc = QLabel("Panel ligero y configurable, predeterminado en Mabox Linux.")
        tint2_desc.setWordWrap(True)
        tint2_desc.setAlignment(Qt.AlignCenter)
        tint2_layout.addWidget(tint2_desc)

        # Botón para configurar Tint2
        self.tint2_config_btn = QPushButton("Configurar Tint2")
        self.tint2_config_btn.clicked.connect(self.configure_tint2)
        tint2_layout.addWidget(self.tint2_config_btn)

        panels_layout.addWidget(tint2_widget)

        # Separador vertical
        v_separator = QFrame()
        v_separator.setFrameShape(QFrame.VLine)
        v_separator.setFrameShadow(QFrame.Sunken)
        panels_layout.addWidget(v_separator)

        # Panel Polybar
        polybar_widget = QWidget()
        polybar_layout = QVBoxLayout(polybar_widget)

        # Vista previa de Polybar
        polybar_preview_label = QLabel()
        if os.path.exists(POLYBAR_PREVIEW) and os.path.getsize(POLYBAR_PREVIEW) > 0:
            polybar_pixmap = QPixmap(POLYBAR_PREVIEW)
            polybar_preview_label.setPixmap(polybar_pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            polybar_preview_label.setText("Vista previa no disponible")
        polybar_preview_label.setAlignment(Qt.AlignCenter)
        polybar_layout.addWidget(polybar_preview_label)

        # Radio button para Polybar
        self.polybar_radio = QRadioButton("Polybar")
        self.polybar_radio.setFont(QFont("Sans", 12, QFont.Bold))
        polybar_layout.addWidget(self.polybar_radio, alignment=Qt.AlignCenter)

        # Descripción de Polybar
        polybar_desc = QLabel("Panel moderno y altamente personalizable con soporte para múltiples temas.")
        polybar_desc.setWordWrap(True)
        polybar_desc.setAlignment(Qt.AlignCenter)
        polybar_layout.addWidget(polybar_desc)

        # Botón para configurar Polybar
        self.polybar_config_btn = QPushButton("Configurar Polybar")
        self.polybar_config_btn.clicked.connect(self.configure_polybar)
        polybar_layout.addWidget(self.polybar_config_btn)

        panels_layout.addWidget(polybar_widget)

        # Agregar el contenedor de paneles al layout principal
        main_layout.addWidget(panels_container)

        # Grupo de botones para los radio buttons
        self.panel_group = QButtonGroup()
        self.panel_group.addButton(self.tint2_radio, 1)
        self.panel_group.addButton(self.polybar_radio, 2)

        # Botones de acción
        buttons_layout = QHBoxLayout()

        self.apply_btn = QPushButton("Aplicar")
        self.apply_btn.clicked.connect(self.apply_panel)

        self.close_btn = QPushButton("Cerrar")
        self.close_btn.clicked.connect(self.close)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.apply_btn)
        buttons_layout.addWidget(self.close_btn)

        main_layout.addLayout(buttons_layout)

        # Seleccionar Tint2 por defecto (es el panel predeterminado de Mabox)
        self.tint2_radio.setChecked(True)

        # Mostrar la ventana
        self.show()

    def configure_tint2(self):
        if not os.path.exists(TINT2_CONFIG_PATH):
            QMessageBox.warning(self, "Error", f"No se encontró el configurador de Tint2 en {TINT2_CONFIG_PATH}")
            return

        try:
            process = QProcess()
            process.startDetached(TINT2_CONFIG_PATH)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo iniciar el configurador de Tint2: {str(e)}")

    def configure_polybar(self):
        # Verificar si polybar está instalado
        try:
            result = subprocess.run(["which", "polybar"], capture_output=True, text=True)
            if result.returncode != 0:
                reply = QMessageBox.question(
                    self,
                    "Polybar no encontrado",
                    "Polybar no está instalado. ¿Deseas instalarlo ahora?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )

                if reply == QMessageBox.Yes:
                    self.install_polybar()
                else:
                    return

            # Importar el módulo de configuración de polybar
            try:
                from polybar_config import PolybarConfigDialog
                dialog = PolybarConfigDialog()
                dialog.exec_()
            except ImportError as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el configurador de Polybar: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al verificar Polybar: {str(e)}")

    def install_polybar(self):
        try:
            msg = QMessageBox()
            msg.setWindowTitle("Instalando Polybar")
            msg.setText("Instalando Polybar. Esto puede tardar unos minutos...")
            msg.setStandardButtons(QMessageBox.NoButton)
            msg.show()
            QApplication.processEvents()

            process = subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "polybar"], check=True)

            msg.close()

            QMessageBox.information(self, "Instalación completada", "Polybar se ha instalado correctamente.")

            # Crear configuración inicial si no existe
            self.create_initial_polybar_config()

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error de instalación", f"No se pudo instalar Polybar: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error durante la instalación: {str(e)}")

    def create_initial_polybar_config(self):
        try:
            # Crear directorio de configuración si no existe
            config_dir = os.path.expanduser("~/.config/polybar")
            os.makedirs(config_dir, exist_ok=True)

            # Copiar configuración predeterminada si existe en el paquete
            default_config = os.path.join(THEMES_DIR, "default", "config.ini")
            if os.path.exists(default_config):
                with open(default_config, 'r') as src:
                    with open(os.path.join(config_dir, "config"), 'w') as dst:
                        dst.write(src.read())
                QMessageBox.information(self, "Configuración creada", "Se ha creado una configuración inicial para Polybar.")
        except Exception as e:
            QMessageBox.warning(self, "Advertencia", f"No se pudo crear la configuración inicial: {str(e)}")

    def apply_panel(self):
        if not self.panel_group.checkedButton():
            QMessageBox.warning(self, "Selección requerida", "Por favor, selecciona un panel.")
            return

        selected_id = self.panel_group.checkedId()

        if selected_id == 1:  # Tint2
            self.restore_tint2()
        elif selected_id == 2:  # Polybar
            self.switch_to_polybar()

    def restore_tint2(self):
        reply = QMessageBox.question(
            self,
            "Restaurar Tint2",
            "¿Deseas restaurar Tint2 como el panel predeterminado?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            try:
                if not os.path.exists(RESTORE_TINT2_SCRIPT):
                    QMessageBox.critical(self, "Error", f"No se encontró el script {RESTORE_TINT2_SCRIPT}")
                    return

                # Hacer el script ejecutable si no lo es
                if not os.access(RESTORE_TINT2_SCRIPT, os.X_OK):
                    subprocess.run(["chmod", "+x", RESTORE_TINT2_SCRIPT], check=True)

                # Ejecutar el script directamente (sin sudo)
                process = subprocess.run([RESTORE_TINT2_SCRIPT], capture_output=True, text=True)

                if process.returncode == 0:
                    QMessageBox.information(self, "Éxito", "Tint2 ha sido restaurado como el panel predeterminado.")
                else:
                    QMessageBox.critical(self, "Error", f"No se pudo restaurar Tint2: {process.stderr}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al restaurar Tint2: {str(e)}")

    def switch_to_polybar(self):
        reply = QMessageBox.question(
            self,
            "Cambiar a Polybar",
            "¿Deseas establecer Polybar como el panel predeterminado?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            try:
                # Verificar si polybar está instalado
                result = subprocess.run(["which", "polybar"], capture_output=True, text=True)
                if result.returncode != 0:
                    reply = QMessageBox.question(
                        self,
                        "Polybar no encontrado",
                        "Polybar no está instalado. ¿Deseas instalarlo ahora?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.Yes
                    )

                    if reply == QMessageBox.Yes:
                        self.install_polybar()
                    else:
                        return

                if not os.path.exists(SWITCH_POLYBAR_SCRIPT):
                    QMessageBox.critical(self, "Error", f"No se encontró el script {SWITCH_POLYBAR_SCRIPT}")
                    return

                # Hacer el script ejecutable si no lo es
                if not os.access(SWITCH_POLYBAR_SCRIPT, os.X_OK):
                    subprocess.run(["chmod", "+x", SWITCH_POLYBAR_SCRIPT], check=True)

                # Ejecutar el script directamente (sin sudo)
                process = subprocess.run([SWITCH_POLYBAR_SCRIPT], capture_output=True, text=True)

                if process.returncode == 0:
                    QMessageBox.information(self, "Éxito", "Polybar ha sido establecido como el panel predeterminado.")
                else:
                    QMessageBox.critical(self, "Error", f"No se pudo establecer Polybar: {process.stderr}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cambiar a Polybar: {str(e)}")

if __name__ == "__main__":
    # Verificar si se está ejecutando como root
    if os.geteuid() == 0:
        print("Este programa no debe ejecutarse como root.")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = PanelSelector()
    sys.exit(app.exec_())