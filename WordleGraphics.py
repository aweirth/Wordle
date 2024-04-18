# File: WordleGraphics.py

"""
This module implements the WordleGWindow class, which manages
the graphical display for the Wordle project.
"""

# Implementation notes
# --------------------
# This WordleGWindow class is implemented as a subclass of
# the GWindow class in the Portable Graphics Library.

from pgl import GWindow, GLabel, GRect, GCompound

N_ROWS = 6			# Number of rows
N_COLS = 5			# Number of columns

GWINDOW_WIDTH = 500		# Width of the graphics window
GWINDOW_HEIGHT = 700		# Height of the graphics window

SQUARE_SIZE = 60		# Size of each square
SQUARE_SEP = 5                  # Separation between squares
TOP_MARGIN = 30    		# Top margin
BOTTOM_MARGIN = 30    		# Bottom margin
MESSAGE_SEP = 20                # Space between board and message center

SQUARE_FONT = "bold 44px 'Helvetica Neue',sans-serif"
MESSAGE_FONT = "bold 20px 'Helvetica Neue',sans-serif"
KEY_FONT = "18px 'Helvetica Neue',sans-serif"
ENTER_FONT = "14px 'Helvetica Neue',sans-serif"

CORRECT_COLOR = "#66BB66"       # A shade of green
PRESENT_COLOR = "#CCBB66"       # A shade of brownish yellow
MISSING_COLOR = "#999999"       # A shade of gray
UNKNOWN_COLOR = "#FFFFFF"       # White
KEY_COLOR = "#DDDDDD"

KEY_WIDTH = 40
KEY_HEIGHT = 60
KEY_CORNER = 9
KEY_XSEP = 5
KEY_YSEP = 7

ASCENT_FRACTION = 0.75           # Used to improve vertical alignment

KEY_LABELS = [
    [ "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P" ],
    [ "A", "S", "D", "F", "G", "H", "J", "K", "L" ],
    [ "ENTER", "Z", "X", "C", "V", "B", "N", "M", "DELETE" ]
]

# Derived constants

SQUARE_DELTA = SQUARE_SIZE + SQUARE_SEP
BOARD_WIDTH = N_COLS * SQUARE_SIZE + (N_COLS - 1) * SQUARE_SEP
BOARD_HEIGHT = N_ROWS * SQUARE_SIZE + (N_ROWS - 1) * SQUARE_SEP
MESSAGE_X = GWINDOW_WIDTH / 2
MESSAGE_Y = TOP_MARGIN + BOARD_HEIGHT + MESSAGE_SEP

class WordleGWindow(GWindow):
    """This class creates the Wordle window."""

    def __init__(self):
        """Creates the Wordle window."""

        def create_grid():
            grid = [ ]
            for row in range(N_ROWS):
                line = [ ]
                for col in range(N_COLS):
                    sq = WordleSquare(self, row, col)
                    self.add(sq)
                    line.append(sq)
                grid.append(line)
            return grid

        def create_keyboard():
            keys = { }
            nk = len(KEY_LABELS[0])
            h = KEY_HEIGHT
            y0 = GWINDOW_HEIGHT - BOTTOM_MARGIN - 3 * KEY_HEIGHT - 2 * KEY_YSEP
            for row in range(len(KEY_LABELS)):
                y = y0 + row * (KEY_HEIGHT + KEY_YSEP)
                x = (GWINDOW_WIDTH - nk * KEY_WIDTH - (nk - 1) * KEY_XSEP) / 2
                if row == 1:
                    x += (KEY_WIDTH + KEY_XSEP) / 2
                for col in range(len(KEY_LABELS[row])):
                    label = KEY_LABELS[row][col]
                    w = KEY_WIDTH
                    if len(label) > 1:
                        w += (KEY_WIDTH + KEY_XSEP) / 2
                    key = WordleKey(w, h, label)
                    self.add(key, x, y)
                    keys[label] = key
                    x += w + KEY_XSEP
            return keys

        def create_message():
            msg = WordleMessage()
            self.add(msg, GWINDOW_WIDTH / 2, MESSAGE_Y)
            return msg

        def key_action(e):
            if isinstance(e, str):
                letter = e.upper()
            else:
                letter = e.get_key().upper()
            if letter == "<BACKSPACE>" or letter == "<DELETE>":
                self.show_message("")
                if self._row < N_ROWS and self._col > 0:
                    self._col -= 1
                    sq = self._grid[self._row][self._col]
                    sq.set_square_label(" ")
            elif letter == "<RETURN>" or letter == "<ENTER>":
                self.show_message("")
                for fn in self._listeners:
                    fn()
            elif letter.isalpha():
                self.show_message("")
                if self._row < N_ROWS and self._col < N_COLS:
                    sq = self._grid[self._row][self._col]
                    sq.set_square_label(letter)
                    self._col += 1

        def click_action(e):
            key = find_key(e.getX(), e.getY())
            if key:
                key_action(key.get_key())

        def find_key(x, y):
            for key in self._keys.values():
                if key.get_frame().contains(x, y):
                    return key
            return None

        def delete_window():
            """Closes the window and exits from the event loop."""
            root.destroy()

        GWindow.__init__(self, GWINDOW_WIDTH, GWINDOW_HEIGHT)
        self._grid = create_grid()
        self._message = create_message()
        self._keys = create_keyboard()
        self._listeners = [ ]
        self.add_event_listener("key", key_action)
        self.add_event_listener("click", click_action)
        self._row = 0
        self._col = 0

    def get_square_label(self, row, col):
        return self._grid[row][col].get_square_label()

    def set_square_label(self, row, col, letter):
        self._grid[row][col].set_square_label(letter)

    def get_square_state(self, row, col):
        return self._grid[row][col].get_state()

    def set_square_state(self, row, col, state):
        self._grid[row][col].set_state(state)

    def get_key_state(self, letter):
        return self._keys[letter].get_state()

    def set_key_state(self, letter, state):
        self._keys[letter].set_state(state)

    def get_current_row(self):
        return self._row

    def set_current_row(self, row):
        self._row = row
        self._col = 0
        for col in range(N_COLS):
            self.set_square_label(row, col, "")
            self.set_square_state(row, col, "UNKNOWN")

    def add_enter_listener(self, fn):
        self._listeners.append(fn)

    def show_message(self, msg, color="Black"):
        self._message.set_text(msg, color)


class WordleSquare(GCompound):

    def __init__(self, gw, row, col):
        GCompound.__init__(self)
        x = (GWINDOW_WIDTH - BOARD_WIDTH) / 2 + col * SQUARE_DELTA
        y = TOP_MARGIN + row * SQUARE_DELTA
        self._letter = " "
        self._state = "UNKNOWN"
        self._frame = GRect(SQUARE_SIZE, SQUARE_SIZE)
        self._frame.set_filled(True)
        self._frame.set_fill_color("White")
        self._label = GLabel("")
        self._label.set_font(SQUARE_FONT)
        self.add(self._frame)
        self.add(self._label)
        self.set_location(x, y)

    def get_square_label(self):
        return self._letter

    def set_square_label(self, letter):
        self._letter = letter
        self._label.set_label(letter)
        x = (SQUARE_SIZE - self._label.get_width()) / 2
        y = (SQUARE_SIZE + ASCENT_FRACTION * self._label.get_ascent()) / 2
        self._label.set_location(x, y)

    def get_state(self):
        return self._state

    def set_state(self, state):
        state = state.upper()
        self._state = state
        fg = "White"
        if state == "UNKNOWN":
            fg = "Black"
            bg = "White"
        elif state == "CORRECT":
            bg = CORRECT_COLOR
        elif state == "PRESENT":
            bg = PRESENT_COLOR
        elif state == "MISSING":
            bg = MISSING_COLOR
        else:
            raise ValueError("Illegal letter state " + str(state))
        self._frame.set_fill_color(bg)
        self._label.set_color(fg)


class WordleKey(GCompound):

    def __init__(self, width, height, key):
        GCompound.__init__(self)
        if len(key) == 1:
            self._key = key
        else:
            self._key = "<" + key + ">"
        self._state = "UNKNOWN"
        font = KEY_FONT
        if key == "ENTER":
            font = ENTER_FONT
        if key == "DELETE":
            key = "\u232B"
        self._frame = GRect(width, height)
        self._frame.set_filled(True)
        self._frame.set_fill_color("White")
        self._label = GLabel(key)
        self._label.set_font(font)
        x = (width - self._label.get_width()) / 2
        y = (height + ASCENT_FRACTION * self._label.get_ascent()) / 2
        self.add(self._frame)
        self.add(self._label, x, y)

    def get_key(self):
        return self._key

    def get_frame(self):
        return self._frame
        
    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state
        fg = "White"
        if state == "UNKNOWN":
            fg = "Black"
            bg = "White"
        elif state == "CORRECT":
            bg = CORRECT_COLOR
        elif state == "PRESENT":
            bg = PRESENT_COLOR
        elif state == "MISSING":
            bg = MISSING_COLOR
        else:
            raise ValueError("Illegal letter state " + str(state))
        self._frame.set_fill_color(bg)
        self._label.set_color(fg)


class WordleMessage(GCompound):

    def __init__(self):
        GCompound.__init__(self)
        self._msg = GLabel("")
        self._msg.set_font(MESSAGE_FONT)
        self.add(self._msg)

    def get_text(self):
        return self._text

    def set_text(self, text, color="Black"):
        self._text = text
        self._msg.setLabel(text)
        self._msg.setColor(color)
        self._msg.setLocation(-self._msg.get_width() / 2,
                              ASCENT_FRACTION * self._msg.get_ascent() / 2)
