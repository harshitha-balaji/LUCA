from .theme import *

APP_STYLE = f"""
/* ==================================================
   APPLICATION FOUNDATION
   ================================================== */

QMainWindow {{
    background-color: {CANVAS};
}}

QWidget {{
    color: {TEXT_SECONDARY};
    font-size: {BODY_SIZE}px;
}}

/* ==================================================
   SURFACE SYSTEM
   ================================================== */

QFrame#card {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: {CARD_RADIUS}px;
}}

QWidget#eventLog {{
    background-color: {SURFACE};
}}

/* ==================================================
   TYPOGRAPHY
   ================================================== */

QLabel#mainHeader {{
    color: {TEXT_PRIMARY};
    font-size: {HEADER_SIZE}px;
    font-weight: 600;
}}

QLabel#cardTitle {{
    color: {ACCENT};
    font-size: {CARD_TITLE_SIZE}px;
    font-weight: 600;
    padding-bottom: 6px;
}}

QLabel#secondaryText {{
    color: {TEXT_SECONDARY};
}}

QLabel#disabledText {{
    color: {TEXT_DISABLED};
}}

/* ==================================================
   STATUS SYSTEM
   ================================================== */

QLabel#statusReady {{
    color: {SUCCESS};
    font-weight: 600;
}}

QLabel#statusRunning {{
    color: {ACCENT};
    font-weight: 600;
}}

QLabel#statusWarning {{
    color: {WARNING};
    font-weight: 600;
}}

QLabel#statusError {{
    color: {ERROR};
    font-weight: 600;
}}

/* ==================================================
   EVENT LOG
   ================================================== */

QLabel#logTimestamp {{
    color: {TEXT_DISABLED};
    min-width: 42px;
}}

QLabel#logInfo,
QLabel#logSystem {{
    color: {TEXT_PRIMARY};
}}

QLabel#logSuccess {{
    color: {SUCCESS};
}}

QLabel#logWarning {{
    color: {WARNING};
}}

QLabel#logError {{
    color: {ERROR};
    font-weight: 600;
}}

/* ==================================================
   INPUTS
   ================================================== */

QLineEdit {{
    background-color: {INTERACTIVE};
    border: 1px solid {BORDER};
    border-radius: {INPUT_RADIUS}px;

    color: {TEXT_PRIMARY};
    padding: 6px;

    selection-background-color: {ACCENT};
    selection-color: {CANVAS};
}}

QLineEdit::placeholder {{
    color: {TEXT_DISABLED};
}}

QLineEdit:focus {{
    border: 1px solid {BORDER_FOCUS};
}}

QLineEdit:disabled {{
    color: {TEXT_DISABLED};
}}

/* ==================================================
   BUTTON SYSTEM
   ================================================== */

QPushButton {{
    min-height: 32px;
    border-radius: {BUTTON_RADIUS}px;
    padding: 6px 12px;
    font-weight: 600;
}}

/* ------------------------------
   Primary
   ------------------------------ */

QPushButton#primaryBtn {{
    background-color: {ACCENT};
    color: {CANVAS};
    border: none;
}}

QPushButton#primaryBtn:hover {{
    background-color: {ACCENT_HOVER};
}}

QPushButton#primaryBtn:pressed {{
    background-color: {ACCENT_ACTIVE};
}}

QPushButton#primaryBtn:disabled {{
    background-color: {BORDER};
    color: {TEXT_DISABLED};
}}

/* ------------------------------
   Secondary
   ------------------------------ */

QPushButton#secondaryBtn {{
    background-color: {INTERACTIVE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
}}

QPushButton#secondaryBtn:hover {{
    background-color: {BORDER};
}}

QPushButton#secondaryBtn:pressed {{
    background-color: {INTERACTIVE};
}}

QPushButton#secondaryBtn:disabled {{
    color: {TEXT_DISABLED};
}}

/* ------------------------------
   Danger
   ------------------------------ */

QPushButton#dangerBtn {{
    background-color: {INTERACTIVE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
}}

QPushButton#dangerBtn:hover {{
    border: 1px solid {ERROR};
    color: {ERROR};
}}

QPushButton#dangerBtn:pressed {{
    background-color: {ERROR};
    border: 1px solid {ERROR};
    color: {CANVAS};
}}

QPushButton#dangerBtn:disabled {{
    color: {TEXT_DISABLED};
}}

/* ==================================================
   SCROLLBAR SYSTEM
   ================================================== */

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
}}

QScrollBar::groove:vertical {{
    background: transparent;
    border: none;
}}

QScrollBar::handle:vertical {{
    background-color: {BORDER};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {ACCENT};
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: transparent;
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    background: transparent;
    border: none;
    height: 0px;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
}}

QScrollBar::groove:horizontal {{
    background: transparent;
    border: none;
}}

QScrollBar::handle:horizontal {{
    background-color: {BORDER};
    border-radius: 5px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {ACCENT};
}}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {{
    background: transparent;
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    background: transparent;
    border: none;
    width: 0px;
}}
"""