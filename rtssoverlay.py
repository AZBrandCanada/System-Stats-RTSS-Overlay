import pyglet
import win32con
import win32gui
import win32api
import time

# Create a transparent, borderless window
window = pyglet.window.Window(
    width=500,
    height=500,
    caption="RTSS Overlay Target",
    style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS,
    vsync=False,
    resizable=False
)
window.set_location(window.screen.width - window.width, 0)

# Make background fully transparent
from pyglet.gl import *



@window.event
def on_draw():
    window.clear()
    label = pyglet.text.Label(
        'RTSS Overlay Target',
        font_name='Arial',
        font_size=14,
        x=10, y=window.height - 90,
        anchor_x='left', anchor_y='top',
        color=(255, 255, 255, 255)
    )
    label.draw()

# Force always-on-top and layered window
hwnd = window._hwnd

# Get current extended style
extended_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

# Apply layered, transparent, and topmost styles
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       extended_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST)

# Set transparency (colorkey: black)
win32gui.SetLayeredWindowAttributes(hwnd, 0x000000, 255, win32con.LWA_COLORKEY)

# Ensure window stays topmost every few seconds
def enforce_topmost(dt):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

pyglet.clock.schedule_interval(enforce_topmost, 5)  # Re-assert topmost every 5 seconds

# Limit to 1 FPS
pyglet.clock.schedule_interval(lambda dt: None, 10)

pyglet.app.run()
