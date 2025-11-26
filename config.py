import datetime

class Config:
    CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    WATCH_DIRECTORY = r"C:\Test"
    POSITION = 34                     # Column index where the new value will be inserted
    VALUE = "NOMBRE ARTICULO"        # The value to insert into each row
    FILENAME_PREFIX = "Pedidos"      # Files to match (case-insensitive)
    CSV_EXTENSION = ".csv"           # File type to monitor
    EXTENSION_LOG = ".log"           # File type to monitor
    DIRECTORY_BACKUP = "backup"      # Directory name for file backup
    DIRECTORY_LOG = "logs"           # Directory name for file backup
    DELIMITER = ";"
    VALUE_EMPTY = ""
    ENCODING = "utf-8"
    ROW_SPLIT = 45

    UNICODE_TO_ANSI_REPLACEMENTS = {
    # Control characters and C1 controls (U+0080-U+009F)
    # Note: Keep the ordinal indicators ª (U+00AA) and º (U+00BA) - they ARE in CP-1252
    **{chr(i): '' for i in range(0x80, 0xA0) if chr(i) not in ['\x81', '\x8D', '\x8F', '\x90', '\x9D', '\xAA', '\xBA']},
    
    # General Punctuation
    '–': '-',   # U+2013 EN DASH
    '—': '-',   # U+2014 EM DASH
    ' ': ' ',   # U+202F NARROW NO-BREAK SPACE
    '†': '*',   # U+2020 DAGGER
    '‡': '**',  # U+2021 DOUBLE DAGGER
    '•': '*',   # U+2022 BULLET
    '…': '...', # U+2026 HORIZONTAL ELLIPSIS
    '‰': '%',   # U+2030 PER MILLE SIGN
    '‱': '%',   # U+2031 PER TEN THOUSAND SIGN
    '′': "'",   # U+2032 PRIME
    '″': '"',   # U+2033 DOUBLE PRIME
    '‴': "'''", # U+2034 TRIPLE PRIME
    '‵': '`',   # U+2035 REVERSED PRIME
    '‶': '``',  # U+2036 REVERSED DOUBLE PRIME
    '‷': "```", # U+2037 REVERSED TRIPLE PRIME
    '‸': '^',   # U+2038 CARET
    '‹': '<',   # U+2039 SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    '›': '>',   # U+203A SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    '※': '*',   # U+203B REFERENCE MARK
    '‼': '!!',  # U+203C DOUBLE EXCLAMATION MARK
    '‽': '!?',  # U+203D INTERROBANG
    '‾': '_',   # U+203E OVERLINE
    '⁁': '|',   # U+2041 CARET INSERTION POINT
    '⁂': '***', # U+2042 ASTERISM
    '⁃': '-',   # U+2043 HYPHEN BULLET
    '⁄': '/',   # U+2044 FRACTION SLASH
    '⁅': '[',   # U+2045 LEFT SQUARE BRACKET WITH QUILL
    '⁆': ']',   # U+2046 RIGHT SQUARE BRACKET WITH QUILL
    
    # Note: The following characters ARE in CP-1252 and should NOT be replaced:
    # ª (U+00AA) - FEMININE ORDINAL INDICATOR
    # º (U+00BA) - MASCULINE ORDINAL INDICATOR
    # These will be preserved automatically since they're in the ANSI character set
    
}
# Characters that are actually in CP-1252 and should be preserved
    CP1252_VALID_CHARS = {
        'ª',  # U+00AA FEMININE ORDINAL INDICATOR
        'º',  # U+00BA MASCULINE ORDINAL INDICATOR
        '¡',  # U+00A1 INVERTED EXCLAMATION MARK
        '¢',  # U+00A2 CENT SIGN
        '£',  # U+00A3 POUND SIGN
        '¤',  # U+00A4 CURRENCY SIGN
        '¥',  # U+00A5 YEN SIGN
        '¦',  # U+00A6 BROKEN BAR
        '§',  # U+00A7 SECTION SIGN
        '¨',  # U+00A8 DIAERESIS
        '©',  # U+00A9 COPYRIGHT SIGN
        '«',  # U+00AB LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
        '¬',  # U+00AC NOT SIGN
        '®',  # U+00AE REGISTERED SIGN
        '¯',  # U+00AF MACRON
        '°',  # U+00B0 DEGREE SIGN
        '±',  # U+00B1 PLUS-MINUS SIGN
        '²',  # U+00B2 SUPERSCRIPT TWO
        '³',  # U+00B3 SUPERSCRIPT THREE
        '´',  # U+00B4 ACUTE ACCENT
        'µ',  # U+00B5 MICRO SIGN
        '¶',  # U+00B6 PILCROW SIGN
        '·',  # U+00B7 MIDDLE DOT
        '¸',  # U+00B8 CEDILLA
        '¹',  # U+00B9 SUPERSCRIPT ONE
        '»',  # U+00BB RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
        '¼',  # U+00BC VULGAR FRACTION ONE QUARTER
        '½',  # U+00BD VULGAR FRACTION ONE HALF
        '¾',  # U+00BE VULGAR FRACTION THREE QUARTERS
        '¿',  # U+00BF INVERTED QUESTION MARK
        '×',  # U+00D7 MULTIPLICATION SIGN
        '÷',  # U+00F7 DIVISION SIGN
}

