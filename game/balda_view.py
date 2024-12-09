from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMessageBox, QGraphicsRectItem, QGraphicsTextItem, QGraphicsScene, \
    QGraphicsView, QGraphicsObject


class BaldaCell(QGraphicsObject):
    cellClicked = pyqtSignal(int, int)

    def __init__(self, x, y, rect_x, rect_y, width, height, parent=None):
        super().__init__(parent)
        self.column = x
        self.row = y
        self.rect = QRectF(rect_x, rect_y, width, height)
        self.brush = QBrush(QColor("white"))
        self.pen_color = QColor("black")

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self.pen_color)
        painter.drawRect(self.rect)

    def mousePressEvent(self, event):
        self.cellClicked.emit(self.column, self.row)

class GameView(QGraphicsView):
    def __init__(self, model, score_labels, current_word_label):
        super().__init__()
        self.model = model
        self.score_labels = score_labels
        self.current_word_label = current_word_label
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.init_ui()

        self.selected_cells = []
        self.editing_text_item = None

    def init_ui(self):
        self.setFixedSize(502, 502)
        self.scene.setSceneRect(0, 0, 500, 500)

        self.cells = []
        for y in range(5):
            row = []
            for x in range(5):
                rect = BaldaCell(x, y, x * 100, y * 100, 100, 100)
                rect.cellClicked.connect(self.handle_cell_click)
                self.scene.addItem(rect)

                text_item = QGraphicsTextItem()
                text_item.setDefaultTextColor(Qt.black)
                text_item.setPos(x * 100 + 40, y * 100 + 40)
                text_item.setTextInteractionFlags(Qt.NoTextInteraction)
                self.scene.addItem(text_item)

                if self.model.board[y][x]:
                    text_item.setPlainText(self.model.board[y][x])

                row.append((rect, text_item))
            self.cells.append(row)

    def handle_cell_click(self, x, y):
        if self.model.board[y][x] == "":
            self.start_text_editing(x, y)
        else:
            try:
                self.model.add_letter_to_word(x, y)
                self.update_current_word()
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def start_text_editing(self, x, y):
        rect, text_item = self.cells[y][x]
        if self.editing_text_item:
            self.finish_text_editing()
            return

        text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        text_item.setFocus()
        self.editing_text_item = (x, y, text_item)

    def finish_text_editing(self):
        if not self.editing_text_item:
            return

        x, y, text_item = self.editing_text_item
        letter = text_item.toPlainText().strip().upper()

        if len(letter) != 1 or not letter.isalpha():
            QMessageBox.warning(self, "Ошибка", "Некорректный ввод! Введите одну букву.")
            text_item.setPlainText("")
        else:
            try:
                self.model.add_letter_to_board(x, y, letter)
            except ValueError as e:
                    QMessageBox.warning(self, "Ошибка", str(e))

        text_item.setTextInteractionFlags(Qt.NoTextInteraction)
        self.editing_text_item = None
        self.refresh_board()

    def refresh_board(self):
        self.scene.clear()
        self.init_ui()

    def update_scores(self):
        self.score_labels[0].setText(f"Игрок 1: {self.model.scores[0]} очков")
        self.score_labels[1].setText(f"Игрок 2: {self.model.scores[1]} очков")

    def update_current_word(self):
        self.current_word_label.setText(f"Текущее слово: {self.model.current_word}")

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if isinstance(item, BaldaCell):
            x, y = item.column, item.row
            if self.model.board[y][x] == "":
                self.start_text_editing(x, y)
            else:
                try:
                    self.model.add_letter_to_word(x, y)
                    self.update_current_word()
                except ValueError as e:
                    QMessageBox.warning(self, "Ошибка", str(e))
