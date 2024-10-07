import subprocess
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QPlainTextEdit, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QWidget, QMessageBox, QSplitter
from PyQt5.QtCore import Qt, QProcess, QFile, QTextStream
from PyQt5.QtGui import QFont, QIcon


class ToolManagerUnix(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Tool Manager")

        # Imposta il logo del programma
        self.setWindowIcon(QIcon('styles/icon/logo.png'))  # Inserisci qui il percorso dell'icona

        self.resize(1400, 900)  # Imposta dimensione iniziale maggiore

        self.tools_dir = "tools"
        self.tool_list = []
        self.process = None
        # Imposta la finestra
        self.setWindowTitle("Python Tool Manager (Unix)")
        self.resize(1400, 900)  # Imposta dimensione iniziale maggiore

        self.tools_dir = "tools"
        self.tool_list = []
        self.process = None

        splitter = QSplitter(Qt.Horizontal)

        # Lista dei tool a sinistra
        self.tool_list_widget = QListWidget()
        font = QFont("Segoe UI", 12)
        self.tool_list_widget.setFont(font)
        splitter.addWidget(self.tool_list_widget)

        # Layout per i pulsanti e il terminale a destra
        right_side_layout = QVBoxLayout()

        # Casella per la descrizione del tool
        self.description_text = QPlainTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setPlaceholderText("Descrizione del tool selezionato")
        self.description_text.setFixedHeight(120)  # Altezza della descrizione ridotta

        # Imposta un font personalizzato con dimensione maggiore
        font = QFont("Segoe UI", 12)  # Cambia la dimensione secondo le tue esigenze
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

        self.load_tools()
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

    def load_tools(self):
        if os.path.exists(self.tools_dir):
            for tool in os.listdir(self.tools_dir):
                tool_path = os.path.join(self.tools_dir, tool)
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

            # Debug per verificare se il pulsante è abilitato
            print("File Manager Button is enabled:", self.file_manager_button.isEnabled())
        else:
            self.run_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.file_manager_button.setEnabled(False)

    def load_tool_description(self):
        description_path = os.path.join(self.tools_dir, self.selected_tool, "description.txt")
        if os.path.exists(description_path):
            with open(description_path, 'r', encoding='utf-8') as f:
                description = f.read()
            self.description_text.setPlainText(description)
        else:
            self.description_text.setPlainText("Nessuna descrizione disponibile.")

    def run_tool(self):
        if hasattr(self, 'selected_tool'):
            tool_path = os.path.join(self.tools_dir, self.selected_tool, "index.py")
            if os.path.exists(tool_path):
                self.output_text.appendPlainText(f"Esecuzione del tool: {self.selected_tool}")

                # Avvia il processo su Unix
                python_executable = "python3"
                command = f"{python_executable} -u {tool_path}"
                self.process.start(command)

                if self.process.waitForStarted():
                    self.run_button.setEnabled(False)
                    self.stop_button.setEnabled(True)
                else:
                    self.output_text.appendPlainText(f"Errore nell'avvio del tool: {self.process.errorString()}")

    def send_command(self):
        user_input = self.input_field.text() + '\n'
        self.input_field.clear()
        if self.process and self.process.state() == QProcess.Running:
            try:
                self.process.write(user_input.encode())
            except Exception as e:
                self.output_text.appendPlainText(f"Errore durante l'invio del comando: {e}")

    def stop_tool(self):
        if self.process.state() == QProcess.Running:
            self.process.terminate()
            self.output_text.appendPlainText(f"Tool {self.selected_tool} fermato.")
            self.run_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output_text.appendPlainText(data)

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output_text.appendPlainText(f"Error: {data}")

    def open_file_manager(self):
        print("Open File Manager Clicked")  # Aggiungi questa riga di debug per confermare l'azione
        if hasattr(self, 'selected_tool'):
            tool_path = os.path.join(self.tools_dir, self.selected_tool)
            if os.path.exists(tool_path):
                subprocess.Popen(['xdg-open', tool_path])  # Usa xdg-open per Linux


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToolManagerUnix()
    window.show()
    sys.exit(app.exec())
