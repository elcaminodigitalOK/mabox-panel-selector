#!/usr/bin/env python3

import os
import sys
import json
import shutil
import subprocess

try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                QHBoxLayout, QLabel, QPushButton, QListWidget,
                                QListWidgetItem, QSplitter, QTextEdit, QFileDialog,
                                QMessageBox, QTabWidget, QScrollArea, QFrame,
                                QDialog, QLineEdit, QFormLayout, QComboBox)
    from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QTextCursor
    from PyQt5.QtCore import Qt, QSize, QProcess, QTimer
except ImportError:
    print("PyQt5 no está instalado. Intentando instalar...")
    os.system("sudo pacman -S --noconfirm python-pyqt5")
    try:
        from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                    QHBoxLayout, QLabel, QPushButton, QListWidget,
                                    QListWidgetItem, QSplitter, QTextEdit, QFileDialog,
                                    QMessageBox, QTabWidget, QScrollArea, QFrame,
                                    QDialog, QLineEdit, QFormLayout, QComboBox)
        from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QTextCursor
        from PyQt5.QtCore import Qt, QSize, QProcess, QTimer
    except ImportError:
        print("No se pudo instalar PyQt5. Por favor, instálalo manualmente con 'sudo pacman -S python-pyqt5'")
        sys.exit(1)

# Rutas
HOME = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME, ".config", "polybar")
THEMES_DIR = "/usr/share/mabox-panel-selector/themes"
USER_THEMES_DIR = os.path.join(CONFIG_DIR, "themes")

class ThemePreviewDialog(QDialog):
    def __init__(self, theme_path, parent=None):
        super().__init__(parent)
        self.theme_path = theme_path
        self.setWindowTitle("Vista previa del tema")
        self.setMinimumSize(800, 400)

        layout = QVBoxLayout()

        # Imagen de vista previa
        preview_label = QLabel()
        preview_path = os.path.join(theme_path, "preview.png")

        if os.path.exists(preview_path):
            pixmap = QPixmap(preview_path)
            preview_label.setPixmap(pixmap.scaled(780, 300, Qt.KeepAspectRatio))
        else:
            preview_label.setText("Vista previa no disponible")

        preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(preview_label)

        # Descripción
        readme_path = os.path.join(theme_path, "README.md")
        description = QTextEdit()
        description.setReadOnly(True)

        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                description.setText(f.read())
        else:
            description.setText("No hay descripción disponible para este tema.")

        layout.addWidget(description)

        # Botones
        button_layout = QHBoxLayout()

        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        apply_button = QPushButton("Aplicar este tema")
        apply_button.clicked.connect(self.apply_theme)
        button_layout.addWidget(apply_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def apply_theme(self):
        """Aplica el tema seleccionado"""
        theme_name = os.path.basename(self.theme_path)

        # Asegurarse de que el directorio de configuración existe
        os.makedirs(CONFIG_DIR, exist_ok=True)

        # Crear enlace simbólico al tema actual
        current_link = os.path.join(CONFIG_DIR, "current")
        config_file = os.path.join(CONFIG_DIR, "config")

        # Buscar el archivo de configuración en el tema
        theme_config = os.path.join(self.theme_path, "config")
        if not os.path.exists(theme_config):
            theme_config = os.path.join(self.theme_path, "config.ini")
            if not os.path.exists(theme_config):
                QMessageBox.warning(self, "Error", f"No se encontró un archivo de configuración en el tema {theme_name}")
                return

        # Copiar la configuración al directorio principal
        try:
            shutil.copy(theme_config, config_file)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo copiar la configuración: {str(e)}")
            return

        # Preguntar si se desea aplicar ahora
        reply = QMessageBox.question(self, "Aplicar tema",
                                    f"El tema {theme_name} ha sido seleccionado.\n"
                                    "¿Desea aplicarlo ahora?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            # Matar instancias existentes de polybar
            subprocess.run(["killall", "-q", "polybar"])

            # Esperar a que se cierren y lanzar polybar
            QTimer.singleShot(500, lambda: subprocess.Popen(["polybar", "main"]))

        self.accept()

class EditThemeDialog(QDialog):
    def __init__(self, theme_path, parent=None):
        super().__init__(parent)
        self.theme_path = theme_path
        self.theme_name = os.path.basename(theme_path)
        self.setWindowTitle(f"Editar tema: {self.theme_name}")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()

        # Pestañas para diferentes archivos de configuración
        self.tabs = QTabWidget()

        # Añadir pestañas para cada archivo de configuración
        config_files = ["config", "colors.ini", "modules.ini"]
        self.editors = {}

        for file in config_files:
            file_path = os.path.join(theme_path, file)
            if os.path.exists(file_path):
                editor = QTextEdit()
                editor.setFont(QFont("Monospace", 10))

                with open(file_path, 'r') as f:
                    editor.setText(f.read())

                self.editors[file] = editor
                self.tabs.addTab(editor, file)

        layout.addWidget(self.tabs)

        # Botones
        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(save_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_changes(self):
        """Guarda los cambios en los archivos de configuración"""
        try:
            for file, editor in self.editors.items():
                file_path = os.path.join(self.theme_path, file)
                with open(file_path, 'w') as f:
                    f.write(editor.toPlainText())

            QMessageBox.information(self, "Cambios guardados",
                                   f"Los cambios en el tema {self.theme_name} han sido guardados.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron guardar los cambios: {str(e)}")

class ImportThemeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Importar tema")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        # Formulario
        form_layout = QFormLayout()

        self.name_edit = QLineEdit()
        form_layout.addRow("Nombre del tema:", self.name_edit)

        self.config_path = QLineEdit()
        self.config_path.setReadOnly(True)
        browse_button = QPushButton("Examinar...")
        browse_button.clicked.connect(self.browse_config)

        config_layout = QHBoxLayout()
        config_layout.addWidget(self.config_path)
        config_layout.addWidget(browse_button)
        form_layout.addRow("Archivo de configuración:", config_layout)

        layout.addLayout(form_layout)

        # Botones
        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        import_button = QPushButton("Importar")
        import_button.clicked.connect(self.import_theme)
        button_layout.addWidget(import_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def browse_config(self):
        """Abre un diálogo para seleccionar el archivo de configuración"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de configuración",
                                                 HOME, "Archivos de configuración (*.ini *.conf config)")
        if file_path:
            self.config_path.setText(file_path)

    def import_theme(self):
        """Importa el tema seleccionado"""
        name = self.name_edit.text().strip()
        config_path = self.config_path.text()

        if not name:
            QMessageBox.warning(self, "Error", "Debe proporcionar un nombre para el tema.")
            return

        if not config_path or not os.path.exists(config_path):
            QMessageBox.warning(self, "Error", "Debe seleccionar un archivo de configuración válido.")
            return

        # Asegurarse de que el directorio de temas de usuario existe
        os.makedirs(USER_THEMES_DIR, exist_ok=True)

        # Crear directorio para el tema
        theme_dir = os.path.join(USER_THEMES_DIR, name)

        if os.path.exists(theme_dir):
            reply = QMessageBox.question(self, "Tema existente",
                                        f"El tema {name} ya existe. ¿Desea sobrescribirlo?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
            else:
                shutil.rmtree(theme_dir)

        try:
            # Crear directorio
            os.makedirs(theme_dir, exist_ok=True)

            # Copiar archivo de configuración
            shutil.copy(config_path, os.path.join(theme_dir, "config"))

            # Crear README.md
            with open(os.path.join(theme_dir, "README.md"), 'w') as f:
                f.write(f"# {name}\n\nTema personalizado para Polybar.\n")

            QMessageBox.information(self, "Tema importado",
                                   f"El tema {name} ha sido importado correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo importar el tema: {str(e)}")

class PolybarConfigDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Configuración de Polybar")
        self.setMinimumSize(900, 600)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)

        # Título
        title = QLabel("Configuración de Polybar")
        title.setFont(QFont("Sans", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Descripción
        desc = QLabel("Seleccione un tema para Polybar o importe uno nuevo:")
        desc.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc)

        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # Splitter para dividir la lista de temas y la vista previa
        splitter = QSplitter(Qt.Horizontal)

        # Panel izquierdo: Lista de temas
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Lista de temas
        self.theme_list = QListWidget()
        self.theme_list.setIconSize(QSize(64, 64))
        self.theme_list.itemDoubleClicked.connect(self.preview_theme)
        left_layout.addWidget(self.theme_list)

        # Botones para la lista de temas
        theme_buttons = QHBoxLayout()

        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.clicked.connect(self.load_themes)
        theme_buttons.addWidget(self.refresh_btn)

        self.import_btn = QPushButton("Importar")
        self.import_btn.clicked.connect(self.import_theme)
        theme_buttons.addWidget(self.import_btn)

        left_layout.addLayout(theme_buttons)

        # Panel derecho: Vista previa y acciones
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Vista previa
        self.preview_label = QLabel("Seleccione un tema para ver la vista previa")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        self.preview_label.setFrameShape(QFrame.StyledPanel)
        right_layout.addWidget(self.preview_label)

        # Descripción del tema
        self.theme_desc = QTextEdit()
        self.theme_desc.setReadOnly(True)
        self.theme_desc.setMinimumHeight(150)
        right_layout.addWidget(self.theme_desc)

        # Botones de acción
        action_buttons = QHBoxLayout()

        self.preview_btn = QPushButton("Vista previa")
        self.preview_btn.clicked.connect(self.preview_selected_theme)
        self.preview_btn.setEnabled(False)
        action_buttons.addWidget(self.preview_btn)

        self.edit_btn = QPushButton("Editar")
        self.edit_btn.clicked.connect(self.edit_selected_theme)
        self.edit_btn.setEnabled(False)
        action_buttons.addWidget(self.edit_btn)

        self.apply_btn = QPushButton("Aplicar")
        self.apply_btn.clicked.connect(self.apply_selected_theme)
        self.apply_btn.setEnabled(False)
        action_buttons.addWidget(self.apply_btn)

        right_layout.addLayout(action_buttons)

        # Añadir paneles al splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 600])

        main_layout.addWidget(splitter)

        # Botones inferiores
        bottom_buttons = QHBoxLayout()

        self.close_btn = QPushButton("Cerrar")
        self.close_btn.clicked.connect(self.close)
        bottom_buttons.addWidget(self.close_btn)

        main_layout.addLayout(bottom_buttons)

        # Cargar temas
        self.load_themes()

        # Mostrar ventana
        self.center()
        self.show()

    def center(self):
        """Centra la ventana en la pantalla"""
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.desktop().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def load_themes(self):
        """Carga los temas disponibles"""
        self.theme_list.clear()
        self.themes = []

        # Asegurarse de que los directorios existen
        os.makedirs(CONFIG_DIR, exist_ok=True)
        os.makedirs(USER_THEMES_DIR, exist_ok=True)

        # Cargar temas del sistema
        if os.path.exists(THEMES_DIR):
            for item in os.listdir(THEMES_DIR):
                theme_dir = os.path.join(THEMES_DIR, item)
                if os.path.isdir(theme_dir):
                    config_file = os.path.join(theme_dir, "config")
                    if not os.path.exists(config_file):
                        config_file = os.path.join(theme_dir, "config.ini")

                    if os.path.exists(config_file):
                        self.themes.append({
                            "name": item,
                            "path": theme_dir,
                            "type": "system"
                        })

        # Cargar temas del usuario
        if os.path.exists(USER_THEMES_DIR):
            for item in os.listdir(USER_THEMES_DIR):
                theme_dir = os.path.join(USER_THEMES_DIR, item)
                if os.path.isdir(theme_dir):
                    config_file = os.path.join(theme_dir, "config")
                    if not os.path.exists(config_file):
                        config_file = os.path.join(theme_dir, "config.ini")

                    if os.path.exists(config_file):
                        self.themes.append({
                            "name": item + " (usuario)",
                            "path": theme_dir,
                            "type": "user"
                        })

        # Añadir temas a la lista
        for theme in sorted(self.themes, key=lambda x: x["name"]):
            item = QListWidgetItem(theme["name"])

            # Añadir icono si hay una vista previa
            preview_path = os.path.join(theme["path"], "preview.png")
            if os.path.exists(preview_path):
                item.setIcon(QIcon(preview_path))

            # Guardar la ruta del tema como dato
            item.setData(Qt.UserRole, theme["path"])

            self.theme_list.addItem(item)

        # Deshabilitar botones si no hay temas
        has_themes = len(self.themes) > 0
        self.preview_btn.setEnabled(False)
        self.edit_btn.setEnabled(False)
        self.apply_btn.setEnabled(False)

        # Conectar selección
        self.theme_list.itemSelectionChanged.connect(self.theme_selected)

    def theme_selected(self):
        """Maneja la selección de un tema"""
        selected_items = self.theme_list.selectedItems()

        if selected_items:
            theme_path = selected_items[0].data(Qt.UserRole)
            theme_name = selected_items[0].text()

            # Mostrar vista previa
            preview_path = os.path.join(theme_path, "preview.png")
            if os.path.exists(preview_path):
                pixmap = QPixmap(preview_path)
                self.preview_label.setPixmap(pixmap.scaled(580, 180, Qt.KeepAspectRatio))
            else:
                self.preview_label.setText("Vista previa no disponible")

            # Mostrar descripción
            readme_path = os.path.join(theme_path, "README.md")
            if os.path.exists(readme_path):
                with open(readme_path, 'r') as f:
                    self.theme_desc.setText(f.read())
            else:
                self.theme_desc.setText(f"Tema: {theme_name}\n\nNo hay descripción disponible para este tema.")

            # Habilitar botones
            self.preview_btn.setEnabled(True)
            self.edit_btn.setEnabled(True)
            self.apply_btn.setEnabled(True)
        else:
            self.preview_label.setText("Seleccione un tema para ver la vista previa")
            self.theme_desc.clear()

            # Deshabilitar botones
            self.preview_btn.setEnabled(False)
            self.edit_btn.setEnabled(False)
            self.apply_btn.setEnabled(False)

    def preview_theme(self, item):
        """Muestra una vista previa del tema seleccionado"""
        theme_path = item.data(Qt.UserRole)
        dialog = ThemePreviewDialog(theme_path, self)
        dialog.exec_()

    def preview_selected_theme(self):
        """Muestra una vista previa del tema seleccionado"""
        selected_items = self.theme_list.selectedItems()

        if selected_items:
            theme_path = selected_items[0].data(Qt.UserRole)
            dialog = ThemePreviewDialog(theme_path, self)
            dialog.exec_()

    def edit_selected_theme(self):
        """Edita el tema seleccionado"""
        selected_items = self.theme_list.selectedItems()

        if selected_items:
            theme_path = selected_items[0].data(Qt.UserRole)

            # Verificar si es un tema del sistema
            if theme_path.startswith("/usr/"):
                reply = QMessageBox.question(self, "Tema del sistema",
                                           "Este es un tema del sistema. ¿Desea crear una copia en su directorio personal para editarlo?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

                if reply == QMessageBox.Yes:
                    # Crear copia en el directorio del usuario
                    theme_name = os.path.basename(theme_path)
                    user_theme_path = os.path.join(USER_THEMES_DIR, theme_name)

                    if os.path.exists(user_theme_path):
                        overwrite = QMessageBox.question(self, "Tema existente",
                                                      f"Ya existe un tema con el nombre '{theme_name}' en su directorio personal. ¿Desea sobrescribirlo?",
                                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                        if overwrite == QMessageBox.No:
                            return

                        # Eliminar tema existente
                        shutil.rmtree(user_theme_path)

                    # Copiar tema
                    shutil.copytree(theme_path, user_theme_path)

                    # Abrir editor con la copia
                    dialog = EditThemeDialog(user_theme_path, self)
                    if dialog.exec_() == QDialog.Accepted:
                        self.load_themes()
                else:
                    return
            else:
                # Editar tema del usuario directamente
                dialog = EditThemeDialog(theme_path, self)
                if dialog.exec_() == QDialog.Accepted:
                    self.load_themes()

    def apply_selected_theme(self):
        """Aplica el tema seleccionado"""
        selected_items = self.theme_list.selectedItems()

        if selected_items:
            theme_path = selected_items[0].data(Qt.UserRole)
            theme_name = selected_items[0].text()

            # Asegurarse de que el directorio de configuración existe
            os.makedirs(CONFIG_DIR, exist_ok=True)

            # Buscar el archivo de configuración en el tema
            config_file = os.path.join(theme_path, "config")
            if not os.path.exists(config_file):
                config_file = os.path.join(theme_path, "config.ini")
                if not os.path.exists(config_file):
                    QMessageBox.warning(self, "Error", f"No se encontró un archivo de configuración en el tema {theme_name}")
                    return

            # Copiar la configuración al directorio principal
            try:
                shutil.copy(config_file, os.path.join(CONFIG_DIR, "config"))
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo copiar la configuración: {str(e)}")
                return

            # Preguntar si se desea aplicar ahora
            reply = QMessageBox.question(self, "Aplicar tema",
                                        f"El tema {theme_name} ha sido seleccionado.\n"
                                        "¿Desea aplicarlo ahora?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                # Matar instancias existentes de polybar
                subprocess.run(["killall", "-q", "polybar"])

                # Esperar a que se cierren y lanzar polybar
                QTimer.singleShot(500, lambda: subprocess.Popen(["polybar", "main"]))

    def import_theme(self):
        """Importa un nuevo tema"""
        dialog = ImportThemeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_themes()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Estilo consistente en todas las plataformas
    config = PolybarConfigDialog()
    sys.exit(app.exec_())