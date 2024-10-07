import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QPlainTextEdit, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QWidget, QMessageBox, QSplitter, QComboBox
from PyQt5.QtCore import Qt, QProcess, QFile, QTextStream
from PyQt5.QtGui import QFont, QIcon, QColor

class ToolManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Tool Manager (Unix)")

        # Imposta il logo del programma
        self.setWindowIcon(QIcon('styles/icon/logo.png'))  # Inserisci qui il percorso dell'icona

        self.resize(1400, 900)  # Imposta dimensione iniziale maggiore

        self.tools_dir = "tools"
        self.tool_list = []
        self.process = None
        self.categories = []

        splitter = QSplitter(Qt.Horizontal)

        # Menu a tendina per la selezione delle categorie
        self.category_selector = QComboBox()
        self.category_selector.currentIndexChanged.connect(self.on_category_change)

        # Pulsante di refresh per la lista dei tool
        self.refresh_button = QPushButton("Refresh Tool List")
        self.refresh_button.clicked.connect(self.refresh_tools)

        # Lista dei tool a sinistra
        self.tool_list_widget = QListWidget()
        font = QFont("Segoe UI", 12)
        self.tool_list_widget.setFont(font)

        # Layout a sinistra con il menu a tendina e la lista dei tool
        left_side_layout = QVBoxLayout()
        left_side_layout.addWidget(self.category_selector)
        left_side_layout.addWidget(self.tool_list_widget)
        left_side_layout.addWidget(self.refresh_button)
        left_side_widget = QWidget()
        left_side_widget.setLayout(left_side_layout)
        splitter.addWidget(left_side_widget)

        # Layout per i pulsanti e il terminale a destra
        right_side_layout = QVBoxLayout()

        # Casella per la descrizione del tool
        self.description_text = QPlainTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setPlaceholderText("Descrizione del tool selezionato")
        self.description_text.setFixedHeight(120)  # Altezza della descrizione ridotta

        # Imposta un font personalizzato con dimensione maggiore
        font = QFont("Segoe UI", 12)
        self.description_text.setFont(font)

        right_side_layout.addWidget(self.description_text)

        # Sezione con pulsanti
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Tool")
        self.run_button.setEnabled(False)
        self.run_button.setObjectName("run_button")
        self.run_button.setIcon(QIcon("run_icon.png"))
        self.run_button.clicked.connect(self.run_tool)

        self.stop_button = QPushButton("Stop Tool")
        self.stop_button.setEnabled(False)
        self.stop_button.setObjectName("stop_button")
        self.stop_button.setIcon(QIcon("stop_icon.png"))
        self.stop_button.clicked.connect(self.stop_tool)

        self.file_manager_button = QPushButton("Open File Manager")
        self.file_manager_button.setEnabled(False)
        self.file_manager_button.setObjectName("file_manager_button")
        self.file_manager_button.setIcon(QIcon("file_icon.png"))
        self.file_manager_button.clicked.connect(self.open_file_manager)

        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.file_manager_button)

        right_side_layout.addLayout(button_layout)

        # Terminale per output (solo lettura)
        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 12))
        right_side_layout.addWidget(self.output_text)

        # Campo di input per inviare comandi
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Inserisci comando...")
        self.input_field.returnPressed.connect(self.send_command)
        self.input_field.setFont(QFont("Consolas", 12))
        right_side_layout.addWidget(self.input_field)

        # Crea un widget per i pulsanti e il terminale
        right_side_widget = QWidget()
        right_side_widget.setLayout(right_side_layout)
        splitter.addWidget(right_side_widget)

        self.setCentralWidget(splitter)

        # Processo per gestire il terminale
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)

        self.load_categories_and_tools()
        self.tool_list_widget.itemSelectionChanged.connect(self.on_tool_select)

        # Carica lo stile da un file esterno
        self.load_stylesheet()

    def load_stylesheet(self):
        """Carica il file CSS esterno"""
        file = QFile("styles/style.css")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
        file.close()

    def load_categories_and_tools(self):
        """Carica le categorie e i tool dalla struttura delle directory."""
        if os.path.exists(self.tools_dir):
            self.categories = [d for d in os.listdir(self.tools_dir) if os.path.isdir(os.path.join(self.tools_dir, d))]
            self.category_selector.addItems(self.categories)
            if self.categories:
                self.load_tools(self.categories[0])  # Carica i tool della prima categoria per impostazione predefinita

    def on_category_change(self):
        """Gestisce il cambiamento di categoria e carica i tool per la categoria selezionata."""
        selected_category = self.category_selector.currentText()
        self.load_tools(selected_category)

    def refresh_tools(self):
        """Aggiorna la lista dei tool ricaricando la directory"""
        self.category_selector.clear()
        self.load_categories_and_tools()

    def load_tools(self, category):
        """Carica i tool dalla directory specificata."""
        self.tool_list_widget.clear()
        self.tool_list = []
        category_path = os.path.join(self.tools_dir, category)
        if os.path.exists(category_path):
            for tool in os.listdir(category_path):
                tool_path = os.path.join(category_path, tool)
                if os.path.isdir(tool_path):
                    self.tool_list_widget.addItem(tool)
                    self.tool_list.append(tool)

    def on_tool_select(self):
        selected_items = self.tool_list_widget.selectedItems()
        if selected_items:
            self.selected_tool = selected_items[0].text()
            self.run_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.file_manager_button.setEnabled(True)  # Attiva il pulsante correttamente
            self.load_tool_description()

        else:
            self.run_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.file_manager_button.setEnabled(False)

    def load_tool_description(self):
        selected_category = self.category_selector.currentText()
        description_path = os.path.join(self.tools_dir, selected_category, self.selected_tool, "description.txt")
        if os.path.exists(description_path):
            with open(description_path, 'r', encoding='utf-8') as f:
                description = f.read()
            self.description_text.setPlainText(description)
        else:
            self.description_text.setPlainText("Nessuna descrizione disponibile.")

    def run_tool(self):
        selected_category = self.category_selector.currentText()
        tool_path = os.path.join(self.tools_dir, selected_category, self.selected_tool, "index.py")
        if os.path.exists(tool_path):
            self.output_text.appendPlainText(f"Esecuzione del tool: {self.selected_tool}")

            # Utilizza sys.executable per il percorso dell'interprete Python
            python_executable = sys.executable
            command = f"{python_executable} -u {tool_path}"

            self.process.start(command)
            if self.process.waitForStarted():
                self.run_button.setEnabled(False)
                self.stop_button.setEnabled(True)
            else:
                self.show_error(f"Errore nell'avvio del tool: {self.process.errorString()}")

    def send_command(self):
        user_input = self.input_field.text() + '\n'
        self.input_field.clear()
        if self.process and self.process.state() == QProcess.Running:
            try:
                self.process.write(user_input.encode())
            except Exception as e:
                self.show_error(f"Errore durante l'invio del comando: {e}")

    def stop_tool(self):
        if self.process.state() == QProcess.Running:
            self.process.terminate()
            self.output_text.appendPlainText(f"Tool {self.selected_tool} fermato.")
            self.run_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def handle_stdout(self):
        """Gestisce l'output normale con colore predefinito"""
        data = self.process.readAllStandardOutput().data().decode()
        self.output_text.appendHtml(f'<span style="color: green;">{data}</span>')

    def handle_stderr(self):
        """Gestisce l'output di errore con colore rosso"""
        data = self.process.readAllStandardError().data().decode()
        self.output_text.appendHtml(f'<span style="color: red;">{data}</span>')

    def show_error(self, message):
        """Mostra una finestra modale con il messaggio di errore"""
        QMessageBox.critical(self, "Errore", message)

    def open_file_manager(self):
        selected_category = self.category_selector.currentText()
        tool_path = os.path.join(self.tools_dir, selected_category, self.selected_tool)
        if os.path.exists(tool_path):
            subprocess.Popen(['xdg-open', tool_path])  # Usa xdg-open su Unix/Linux per aprire il file manager


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToolManager()
    window.show()
    sys.exit(app.exec())
