import asyncio
from functools import partial
import sys
from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from qasync import QEventLoop
from PySide6.QtGui import QIcon
from task_manager import TaskManager
from tasks.epic_raid import task_epic_raid
from tasks.event_farm import task_event_farm
from core import ASSETS

TASKS = {
    "Epic Raid farm": task_epic_raid,
    "Event Farm": task_event_farm,
}


class MainWindow(QMainWindow):

    def __init__(self, task_manager: TaskManager):
        super().__init__()

        self.manager = task_manager

        self.setWindowTitle("Bleach Brave Souls Bot")
        self.setWindowIcon(QIcon(str(ASSETS / "icone2.ico")))
        self.resize(600, 400)


        self.task_selector = QComboBox()
        self.task_selector.addItems(TASKS.keys())

        self.current_task_label = QLabel("Nenhuma task em execução")
        self.current_task_label.setStyleSheet(
            "font-weight: bold; color: #777;"
        )

        self.start_button = QPushButton("Iniciar")
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setEnabled(False)

        self.log_list = QListWidget()

        self.start_button.clicked.connect(self.start_task)
        self.cancel_button.clicked.connect(self.cancel_task)

        # Layouts
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Escolher task:"))
        selector_layout.addWidget(self.task_selector)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addLayout(selector_layout)
        layout.addWidget(QLabel("Task atual:"))
        layout.addWidget(self.current_task_label)
        layout.addLayout(buttons_layout)
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_log(self, mensagem: str):
        """Thread-safe log addition for PySide6."""
        QTimer.singleShot(0, lambda: self._safe_add_log(mensagem))

    def _safe_add_log(self, mensagem: str):
        self.log_list.addItem(mensagem)
        self.log_list.scrollToBottom()

    @Slot()
    def start_task(self):
        if self.manager.is_running:
            return

        task_name = self.task_selector.currentText()
        task_function = TASKS[task_name]

        task_com_log = partial(task_function, log=self.add_log)

        self.current_task_label.setText(task_name)
        self.current_task_label.setStyleSheet(
            "font-weight: bold; color: green;"
        )
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.task_selector.setEnabled(False)

        asyncio.create_task(self._execute_task(task_name, task_com_log))

    async def _execute_task(self, name: str, task_fn):
        try:
            await self.manager.start(name, task_fn)
            await self.manager.wait()
        except Exception as error:
            self.add_log(f"Erro em {name}: {error}")
            QMessageBox.critical(
                self, "Erro na task", f"A task '{name}' falhou:\n{error}"
            )
        finally:
            self.on_task_finished()

    @Slot()
    def cancel_task(self):
        if not self.manager.is_running:
            return

        self.add_log("[TASK MANAGER] - Solicitando cancelamento...")
        self.cancel_button.setEnabled(False)

        asyncio.create_task(self.manager.cancel())

    def on_task_finished(self):
        self.current_task_label.setText("Nenhuma task em execução")
        self.current_task_label.setStyleSheet(
            "font-weight: bold; color: #777;"
        )
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.task_selector.setEnabled(True)

    def closeEvent(self, event):
        if self.manager.is_running:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.manager.cancel())
        event.accept()
