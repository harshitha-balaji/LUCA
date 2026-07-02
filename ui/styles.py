from .theme import *

APP_STYLE = f"""
/* ==================================================
   APPLICATION
   ================================================== */

QMainWindow {{
    background-color: {APP_BACKGROUND};
}}

/* ==================================================
   CARD SYSTEM
   ================================================== */

QFrame#card {{
    background-color: {CARD_BACKGROUND};
    border: 1px solid {BORDER};
    border-radius: {CARD_RADIUS}px;
}}

/* ==================================================
   EVENT LOG CONTAINER (FIX)
   ================================================== */

QWidget#eventLog {{
    background-color: {CARD_BACKGROUND};
}}

/* ==================================================
   CARD TITLES
   ================================================== */

QLabel#cardTitle {{
    color: {TEAL_MUTED};
    font-size: {CARD_TITLE_SIZE}px;
    font-weight: 600;
    padding-bottom: 6px;
    letter-spacing: 0.3px;
}}

/* ==================================================
   MAIN HEADER
   ================================================== */

QLabel#mainHeader {{
    color: {TEXT_PRIMARY};
    font-size: {HEADER_SIZE}px;
    font-weight: 600;
    letter-spacing: 0.4px;
}}

/* ==================================================
   GLOBAL TEXT
   ================================================== */

QLabel {{
    color: {TEXT_SECONDARY};
    font-size: {BODY_SIZE}px;
}}

QLabel#supportText {{
    color: {TEXT_SUPPORT};
}}

/* ==================================================
   ROBOT STATUS
   ================================================== */

QLabel#statusReady {{
    color: {SUCCESS};
    font-weight: 600;
}}

QLabel#statusRunning {{
    color: {TEAL};
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
   EVENT LOG TEXT STYLES
   ================================================== */

QLabel#logTimestamp {{
    color: {TEXT_SUPPORT};
    min-width: 42px;
}}

QLabel#logInfo {{
    color: {TEXT_PRIMARY};
}}

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
    background-color: {APP_BACKGROUND};
    border: 1px solid {BORDER};
    color: {TEXT_PRIMARY};
    padding: 6px;
    border-radius: {INPUT_RADIUS}px;
}}

QLineEdit:focus {{
    border: 1px solid {TEAL};
}}

/* ==================================================
   BUTTONS
   ================================================== */

QPushButton {{
    min-height: 34px;
}}

QPushButton#primaryBtn {{
    background-color: {TEAL};
    color: {APP_BACKGROUND};
    border: none;
    border-radius: {BUTTON_RADIUS}px;
    padding: 8px;
    font-weight: 600;
}}

QPushButton#primaryBtn:hover {{
    background-color: {TEAL_HOVER};
}}

QPushButton#primaryBtn:pressed {{
    background-color: {TEAL_MUTED};
}}

QPushButton#primaryBtn:disabled {{
    background-color: {BORDER};
    color: {TEXT_DISABLED};
}}

QPushButton#secondaryBtn {{
    background-color: {SECONDARY_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: {BUTTON_RADIUS}px;
    padding: 8px;
}}

QPushButton#secondaryBtn:hover {{
    background-color: {BORDER};
    border-color: {TEAL_HOVER};
}}

QPushButton#secondaryBtn:disabled {{
    color: {TEXT_DISABLED};
}}

QPushButton#dangerBtn {{
    background-color: {SECONDARY_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: {BUTTON_RADIUS}px;
    padding: 8px;
}}

QPushButton#dangerBtn:hover {{
    border-color: {ERROR};
    color: {ERROR};
}}

QPushButton#dangerBtn:pressed {{
    background-color: {ERROR};
    color: {TEXT_PRIMARY};
}}

QPushButton#dangerBtn:disabled {{
    color: {TEXT_DISABLED};
}}
"""