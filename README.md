# To-Do List 

This application helps users manage their daily tasks efficiently using a modern graphical interface.  
Each task can have its own **note**, **date**, and **alarm reminder**, all stored locally in a SQLite database.
The project is designed with a **multi-window structure**, making it easy to extend, maintain, and understand.

---

## Features

-  Add tasks with custom titles  
-  Attach notes to each task  
-  Assign calendar dates  
-  Set alarm reminders  
-  Automatic alarm popups with sound  
-  Persistent storage using SQLite  
-  Database-driven state management  
-  Smart checkbox (text click vs check click)  
-  Multi-window architecture (Qt Designer UI files)

---

##  Project Structure

```
todolist/
├── assets/
│   ├── icons/
│   ├── alarm.wav
│   └── style.qss
│
├── Python_Files/
│   ├── main_window.py
│   ├── second_window.py
│   ├── alarm_window.py
│   ├── calendar_window.py
│   ├── note_window.py
│   └── base_widgets.py
│
├── Ui_Files/
│   ├── todolist.ui
│   ├── secondwindow.ui
│   ├── alarmwindow.ui
│   ├── calendarwindow.ui
│   └── notewindow.ui
│
├── main.py
└── README.md
```

---

##  Application Demo



https://github.com/user-attachments/assets/6cf7cb3c-8346-4a6b-ba44-fde1edc69419




---

###  Installation

```bash
pip install PyQt5
```

###  Run

```bash
python main.py
```

---

##  Technologies

- **Python 3** – Core application logic and data processing  
- **PyQt5** – Graphical user interface, event handling, and window management  
- **Qt Designer** – Visual design of user interfaces using `.ui` files  
- **SQLite** – Lightweight local database for storing tasks, notes, dates, and alarms  
- **Qt Multimedia (QSound)** – Playing alarm sounds for task reminders  
- **QSS (Qt Style Sheets)** – Custom styling and theming of UI components  
- **QTimer** – Background alarm checking without blocking the UI  
- **Custom PyQt Widgets** – Enhanced user interaction (e.g. clickable task text)  
- **Signal & Slot Mechanism** – Communication between windows and components  
- **Modular Project Structure** – Clean separation of features across multiple files  

---

If you enjoyed this project, don’t forget to give it a star ⭐ and follow for more projects ✌️😊


