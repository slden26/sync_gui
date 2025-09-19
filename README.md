# Sync GUI
Локальный инструмент для синхронизации папок с прогрессбаром, разрешением конфликтов, сохранением настроек и сборкой .exe.

## 🚀 Возможности
- Синхронизация двух папок с отображением прогресса
- Разрешение конфликтов: перезапись, пропуск, сравнение
- Сохранение настроек между сессиями
- Поддержка иконок и тем
- PyInstaller-совместимость

## 🛠️ Установка
git clone https://github.com/slden26/sync_gui.git
cd sync_gui
pip install -r requirements.txt

## 🧱 Сборка .exe
pyinstaller main.py --onefile --noconsole --icon=icon.ico

## 📂 Структура
sync_gui/
├── main.py
├── sync.py
├── settings.json
├── README.md
├── .gitignore
└── icon.ico

## 📜 Лицензия
MIT — свободно используйте и модифицируйте.

