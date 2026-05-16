from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import (QApplication, QWidget,
                             QMainWindow, QPushButton,
                             QFileDialog, QRadioButton,
                             QLabel, QMenu)
import sys
import cv2
from obrabotka import zerkalo, BlackWhite
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ✅ Храним изображения в памяти, а не пути
        self.original_img = None  # Оригинал (не меняется)
        self.current_img = None   # Текущее состояние (все фильтры применяются к нему)
        self.setMinimumSize(QSize(800, 600))

        window = QWidget(self)
        self.setCentralWidget(window)

        # Создаём кнопки с указанием родителя
        self.btnChoice = QPushButton("Выбрать изображение", window)
        self.btnChoice.clicked.connect(self.openImage)
        #self.Rad = QRadioButton("Изменить фото", window)
        self.btnClean = QPushButton("Очистить фото", window)
        self.btnClean.clicked.connect(self.cleanImage)
        self.btnDownload = QPushButton("Скачать фото", window)
        self.btnBack = QPushButton("Показать исходную версию", window)

        # Задаём размеры
        self.btnChoice.setFixedSize(200, 50)
        #self.Rad.setFixedSize(200, 30)
        self.btnClean.setFixedSize(200, 50)
        self.btnDownload.setFixedSize(200, 50)
        self.btnBack.setFixedSize(200, 50)

        self.btnChoice.move(100, 50)
        #self.Rad.move(100, 120)
        self.btnClean.move(100, 180)
        self.btnDownload.move(100, 260)
        self.btnBack.move(100, 340)

        self.photo_area = QLabel("Фото", window)
        self.photo_area.setGeometry(350, 50, 400, 400)
        self.photo_area.setStyleSheet("""
                    background-color: #2b2b2b;  /* Темно-серый фон */
                    border: 2px solid #555555;  /* Тонкая рамка */
                    border-radius: 10px;        /* Скругленные углы */
                    color: #aaaaaa;             /* Цвет текста-заглушки */
                """)
        self.photo_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_area.setText("Загрузите изображение")

        self.func_menu = QMenu(self)
        self.func_menu.addAction("Сделать Ч/Б").triggered.connect(self.blackWhite)
        self.func_menu.addAction("Зеркало").triggered.connect(self.FlipPhoto)

        self.btnFunctions = QPushButton("Действия с фото", window)
        self.btnFunctions.setFixedSize(200, 50)
        self.btnFunctions.move(100, 120)  # Поставим ниже остальных кнопок
        self.btnFunctions.setMenu(self.func_menu)  # 🔑 Главная команда

    def openImage(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "", "Images (*.png *.jpg)"
        )
        if file_path:
            # Безопасная загрузка (работает даже с кириллицей в пути)
            self.original_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            self.current_img = self.original_img.copy()
            self.display_image(self.current_img)

    def FlipPhoto(self):
        if self.current_img is None: return
        # 🔄 Переворачиваем ТЕКУЩЕЕ состояние, а не читаем файл заново
        self.current_img = cv2.flip(self.current_img, 1)
        self.display_image(self.current_img)

    def blackWhite(self):
        if self.current_img is None: return

        # 1. Переводим текущее состояние в оттенки серого
        gray = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2GRAY)

        # 2. Применяем жёсткий порог: всё <127 → 0 (чёрный), всё >=127 → 255 (белый)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # 3. 🔑 ВАЖНО: Обновляем self.current_img и возвращаем 3 канала для QLabel
        self.current_img = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

        # 4. Отображаем обновлённую картинку
        self.display_image(self.current_img)

    def cleanImage(self):
        if self.original_img is not None:
            # 🧹 Просто восстанавливаем копию оригинала
            self.current_img = self.original_img.copy()
            self.display_image(self.current_img)

    def display_image(self, img_array):
        """Единый метод: numpy-массив → QPixmap → показ в QLabel"""
        h, w, _ = img_array.shape
        rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        q_img = QImage(rgb.data, w, h, w * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        scaled = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.photo_area.setPixmap(scaled)
        self.photo_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()