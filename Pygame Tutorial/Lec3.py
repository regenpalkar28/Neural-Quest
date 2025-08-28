# MOUSEMOTION events are issued whenever we move mouse over pygame window
# the event object has:
#   - 3 numbers corresponding to the buttons on mouse (Lclick, MClick, Rclick) 
#   - Position: tuple containing x and y coords of the mouse when event was generated
#   - rel: tuple containing the distance the mouse has moved since last mouse motion

# mouse also generated MOUSEBUTTONDOWN (click) followed by MOUSEBUTTONUP (release) events
# it contains 2 values:
#   - button: number of the button that was pressed
#   - pos: tuple containing position of the mouse when the event was generated