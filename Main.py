import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QPlainTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox, QSplitter
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QFont

class ToolManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Tool Manager")
        self.setGeometry(300, 100, 800, 600)

        self.tools_dir = "tools"
        self.tool_list = []
        self.process = None

        # Layout principale con splitter per dividere tool e terminale
        splitter = QSplitter(Qt.Horizontal)

        # Lista dei tool a sinistra
        self.tool_list_widget = QListWidget()
        font = QFont()
        font.setPointSize(12)  # Aumenta la dimensione del carattere
        self.tool_list_widget.setFont(font)
        splitter.addWidget(self.tool_list_widget)

        # Layout per i pulsanti e il terminale a destra
        right_side_layout = QVBoxLayout()

        # Sezione con pulsanti
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run")
        self.run_button.setEnabled(False)  # Abilitato solo quando un tool è selezionato
        self.run_button.clicked.connect(self.run_tool)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)  # Abilitato solo quando il tool è in esecuzione
        self.stop_button.clicked.connect(self.stop_tool)

        self.file_manager_button = QPushButton("Open File Manager")
        self.file_manager_button.setEnabled(False)  # Abilitato solo quando un tool è selezionato
        self.file_manager_button.clicked.connect(self.open_file_manager)

        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.file_manager_button)

        right_side_layout.addLayout(button_layout)

        # Terminale per output nella parte bassa a destra
        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)  # Solo output, no editing
        self.output_text.setFont(QFont("Consolas", 12))  # Font adatto al terminale
        right_side_layout.addWidget(self.output_text)

        # Crea un widget per i pulsanti e il terminale
        right_side_widget = QWidget()
        right_side_widget.setLayout(right_side_layout)
        splitter.addWidget(right_side_widget)

        # Imposta lo splitter come layout principale
        self.setCentralWidget(splitter)

        # Processo per eseguire i tool
        self.qprocess = None

        # Carica i tool
        self.load_tools()

        # Collegamento alla selezione di un tool
        self.tool_list_widget.itemSelectionChanged.connect(self.on_tool_select)

    def load_tools(self):
        """Carica i tool dalla directory specificata."""
        if os.path.exists(self.tools_dir):
            for tool in os.listdir(self.tools_dir):
                tool_path = os.path.join(self.tools_dir, tool)
                if os.path.isdir(tool_path):
                    self.tool_list_widget.addItem(tool)
                    self.tool_list.append(tool)

    def on_tool_select(self):
        """Abilita i pulsanti quando un tool viene selezionato."""
        selected_items = self.tool_list_widget.selectedItems()
        if selected_items:
            self.selected_tool = selected_items[0].text()
            self.run_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.file_manager_button.setEnabled(True)
        else:
            self.run_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.file_manager_button.setEnabled(False)

    def run_tool(self):
        """Esegue il tool selezionato utilizzando subprocess."""
        if hasattr(self, 'selected_tool'):
            tool_path = os.path.join(self.tools_dir, self.selected_tool, "index.py")
            if os.path.exists(tool_path):
                self.output_text.appendPlainText(f"Esecuzione del tool: {self.selected_tool}")

                # Usa subprocess per avviare il processo
                python_executable = "C:/Users/MarcelloMaccagnola/.conda/envs/new1/python.exe"
                command = [python_executable, "-u", tool_path]

                # Avvia il processo e legge l'output in tempo reale
                self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Disabilita il pulsante Run e abilita Stop
                self.run_button.setEnabled(False)
                self.stop_button.setEnabled(True)

                # Legge l'output in un thread separato
                self.read_output()

            else:
                QMessageBox.critical(self, "Errore", "Il file index.py non esiste!")

    def read_output(self):
        """Legge l'output del processo e lo visualizza nel terminale."""
        while True:
            output = self.process.stdout.readline()
            if output == "" and self.process.poll() is not None:
                break
            if output:
                self.output_text.appendPlainText(output.strip())

    def stop_tool(self):
        """Ferma il tool in esecuzione."""
        if self.process:
            self.process.terminate()
            self.output_text.appendPlainText(f"Tool {self.selected_tool} fermato.")
            self.run_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def open_file_manager(self):
        """Apre il file manager nella cartella del tool selezionato."""
        if hasattr(self, 'selected_tool'):
            tool_path = os.path.join(self.tools_dir, self.selected_tool)
            if os.path.exists(tool_path):
                QFileDialog.getExistingDirectory(self, "Open Directory", tool_path)
            else:
                QMessageBox.critical(self, "Errore", "La cartella del tool non esiste!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToolManager()
    window.show()
    sys.exit(app.exec())
