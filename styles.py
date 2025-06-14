__all__ = ['STYLESHEET']

PRIMARY_COLOR = '#4A4A4A'
SECONDARY_COLOR = '#282828'
HIGHLIGHT_COLOR = '#606C71'
DISABLED_COLOR = '#393939'
FONT_COLOR = '#FFFFFF'

STYLESHEET = f'''

    #primary {{
        background-color: {PRIMARY_COLOR};
    }}
    
    #secondary {{
        background-color: {SECONDARY_COLOR};
    }}
    
    QLabel {{
        color: {FONT_COLOR};
    }}
    
    QPushButton {{
        color: {FONT_COLOR};
        padding: 5px;
    }}
    
    #primary QPushButton {{
        background-color: {SECONDARY_COLOR};
    }}
    
    #secondary QPushButton {{
        background-color: {PRIMARY_COLOR};
    }}
    
    QComboBox {{
        background-color: {SECONDARY_COLOR};
        selection-background-color: {SECONDARY_COLOR};
        color: {FONT_COLOR};
    }}
    
    QComboBox QAbstractItemView {{
        color: {FONT_COLOR};
        border: 1px solid gray;
        selection-background-color: {HIGHLIGHT_COLOR};
        selection-color: white;
        background-color: {SECONDARY_COLOR};
    }}
    
'''