import tkinter as tk
import pyautogui
import threading
import time

TRAIL_LENGTH = 15
UPDATE_INTERVAL = 0.02  # seconds

positions = []
running = True  # flag to stop the thread

def update_trail(canvas):
    while running:
        x, y = pyautogui.position()
        positions.append((x, y))
        if len(positions) > TRAIL_LENGTH:
            positions.pop(0)

        canvas.delete("trail")
        for i, (px, py) in enumerate(positions):
            alpha = int(255 * (i + 1) / TRAIL_LENGTH)
            color = f'#{alpha:02x}00{255 - alpha:02x}'  # Ramping red-blue fade
            canvas.create_oval(px-5, py-5, px+5, py+5, fill=color, outline="", tags="trail")

        time.sleep(UPDATE_INTERVAL)

def start_trail_window():
    def on_escape(event=None):
        global running
        running = False
        root.destroy()

    root = tk.Tk()
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.3)
    root.overrideredirect(True)
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

    root.bind('<Escape>', on_escape)

    canvas = tk.Canvas(root, bg='black', highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    threading.Thread(target=update_trail, args=(canvas,), daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    start_trail_window()
