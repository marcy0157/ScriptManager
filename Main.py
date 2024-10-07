import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QPlainTextEdit, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QWidget, QFileDialog, QMessageBox, QSplitter
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
        font.setPointSize(12)
        self.tool_list_widget.setFont(font)
        splitter.addWidget(self.tool_list_widget)

        # Layout per i pulsanti e il terminale a destra
        right_side_layout = QVBoxLayout()

        # Sezione con pulsanti
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Tool")
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.run_tool)

        self.stop_button = QPushButton("Stop Tool")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_tool)

        self.file_manager_button = QPushButton("Open File Manager")
        self.file_manager_button.setEnabled(False)
        self.file_manager_button.clicked.connect(self.open_file_manager)

        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.file_manager_button)

        right_side_layout.addLayout(button_layout)

        # Terminale per output (solo lettura)
        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)  # Solo output
        self.output_text.setFont(QFont("Consolas", 12))  # Font adatto al terminale
        right_side_layout.addWidget(self.output_text)

        # Campo di input per inviare comandi
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Inserisci comando...")
        self.input_field.returnPressed.connect(self.send_command)  # Invio con tasto Invio
        right_side_layout.addWidget(self.input_field)

        # Crea un widget per i pulsanti e il terminale
        right_side_widget = QWidget()
        right_side_widget.setLayout(right_side_layout)
        splitter.addWidget(right_side_widget)

        self.setCentralWidget(splitter)

        # Processo per gestire il terminale
        self.process = QProcess()

        # Connessione per l'output del terminale
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)

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
        """Esegue il tool selezionato tramite cmd.exe scrivendo il comando."""
        if hasattr(self, 'selected_tool'):
            tool_path = os.path.join(self.tools_dir, self.selected_tool, "index.py")
            if os.path.exists(tool_path):
                self.output_text.appendPlainText(f"Esecuzione del tool: {self.selected_tool}")

                # Avvia cmd.exe
                self.process.start("cmd.exe")
                if self.process.waitForStarted():
                    self.output_text.appendPlainText("CMD started.")
                    python_executable = "C:/Users/MarcelloMaccagnola/.conda/envs/new1/python.exe"
                    command = f"{python_executable} -u {tool_path}"

                    # Scrive il comando direttamente nel terminale
                    self.process.write(command.encode() + b'\n')

                    # Abilita/Disabilita i pulsanti
                    self.run_button.setEnabled(False)
                    self.stop_button.setEnabled(True)
                else:
                    self.output_text.appendPlainText(f"Errore nell'avvio del tool: {self.process.errorString()}")

            else:
                QMessageBox.critical(self, "Errore", "Il file index.py non esiste!")

    def send_command(self):
        """Invia il comando inserito dall'utente al processo in esecuzione."""
        user_input = self.input_field.text() + '\n'
        self.input_field.clear()

        # Verifica se il processo è attivo e se stdin è disponibile
        if self.process and self.process.state() == QProcess.Running:
            try:
                self.process.write(user_input.encode())  # Invia il comando al processo
            except Exception as e:
                self.output_text.appendPlainText(f"Errore durante l'invio del comando: {e}")
    # def send_command(self):
    #     """Invia il comando inserito dall'utente al processo in esecuzione."""
    #     user_input = self.input_field.text() + '\n'
    #     self.input_field.clear()
    #
    #     # Verifica se il processo è attivo e se stdin è disponibile
    #     if self.process and self.process.state() == QProcess.Running:
    #         try:
    #             self.process.write(user_input.encode())
    #             self.process.flush()  # Assicura l'invio immediato
    #         except Exception as e:
    #             self.output_text.appendPlainText(f"Errore durante l'invio del comando: {e}")

    def stop_tool(self):
        """Ferma il tool in esecuzione."""
        if self.process.state() == QProcess.Running:
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

    def handle_stdout(self):
        """Gestisce l'output del terminale cmd.exe"""
        data = self.process.readAllStandardOutput().data().decode()
        self.output_text.appendPlainText(data)

    def handle_stderr(self):
        """Gestisce gli errori del terminale cmd.exe"""
        data = self.process.readAllStandardError().data().decode()
        self.output_text.appendPlainText(f"Error: {data}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToolManager()
    window.show()
    sys.exit(app.exec())
