import sys
import asyncio
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

from bot_gui import MainWindow
from task_manager import TaskManager


def main():
    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    manager = TaskManager()

    window = MainWindow(task_manager=manager)
    window.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()