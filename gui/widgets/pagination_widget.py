from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QToolButton, QLineEdit, QLabel


class PaginationWidget(QWidget):

    pageChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.rows_per_page = 1000
        self.page_count = 1
        self.current_page = 1
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)

        self.first_page_btn = QToolButton(self)
        self.first_page_btn.clicked.connect(self._on_first_page_btn_clicked)
        self.first_page_btn.setArrowType(Qt.LeftArrow)
        self.first_page_btn.setToolTip("First page")
        layout.addWidget(self.first_page_btn)

        self.prev_page_btn = QToolButton(self)
        self.prev_page_btn.clicked.connect(self._on_prev_page_btn_clicked)
        self.prev_page_btn.setArrowType(Qt.LeftArrow)
        self.prev_page_btn.setToolTip("Previous page")
        layout.addWidget(self.prev_page_btn)

        self.page_edit = QLineEdit("1")
        self.page_edit.setMaximumSize(45, 24)
        self.page_edit.returnPressed.connect(
            lambda: self.set_current_page(self.page_edit.text())
        )
        layout.addWidget(self.page_edit)

        self.next_page_btn = QToolButton(self)
        self.next_page_btn.clicked.connect(self._on_next_page_btn_clicked)
        self.next_page_btn.setArrowType(Qt.RightArrow)
        self.next_page_btn.setToolTip("Next page")
        layout.addWidget(self.next_page_btn)

        self.last_page_btn = QToolButton(self)
        self.last_page_btn.clicked.connect(self._on_last_page_btn_clicked)
        self.last_page_btn.setArrowType(Qt.RightArrow)
        self.last_page_btn.setToolTip("Last page")
        layout.addWidget(self.last_page_btn)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def set_enabled(self, enabled):
        self.prev_page_btn.setEnabled(enabled)
        self.next_page_btn.setEnabled(enabled)
        self.last_page_btn.setEnabled(enabled)
        self.first_page_btn.setEnabled(enabled)
        self.status_label.setEnabled(enabled)
        self.page_edit.setEnabled(enabled)

    def update_status_text(self):
        status = f"Page: {self.current_page} / {self.page_count}"
        self.status_label.setText(status)

    def set_status_text(self, text):
        self.status_label.setText(text)

    def set_page_count(self, page_count):
        # if self.current_page > page_count:
        #     self.set_current_page(page_count)
        self.page_count = page_count
        self.update_status_text()

    def set_current_page(self, page, block_signals=False):
        try:
            if not isinstance(page, int):
                page = int(page)
        except ValueError:
            print(f"Exception on set_current_page: page must be integer.")
            return

        if page < 1:
            page = 1
        if page > self.page_count:
            page = self.page_count

        self.current_page = page
        self.page_edit.setText(str(page))
        self.update_status_text()
        if not block_signals:
            self.pageChanged.emit(page)

    def _on_prev_page_btn_clicked(self):
        self.set_current_page(self.current_page - 1)

    def _on_next_page_btn_clicked(self):
        self.set_current_page(self.current_page + 1)

    def _on_first_page_btn_clicked(self):
        self.set_current_page(1)

    def _on_last_page_btn_clicked(self):
        self.set_current_page(self.page_count)
