"""
Contains all main styles for the application
"""

# Standard Colors
PRIMARY_COLOR = '#4A4A4A'
SECONDARY_COLOR = '#282828'
HIGHLIGHT_COLOR = '#606C71'
FONT_COLOR = '#FFFFFF'

# Unpack no margins using *NO_MARGINS
NO_MARGINS = tuple([0, 0, 0, 0])

# Contains the main stylesheets for standard QWidgets in the application
MAIN_STYLES = f'''
    QLabel {{
        color: {FONT_COLOR};
        font-size: 18px;
    }}
    
    QPushButton {{
        color: {FONT_COLOR};
        font-size: 18px;
    }}
    
    QWidget {{
        background-color: {PRIMARY_COLOR};
    }}
'''

BUTTON_HEIGHT = 60