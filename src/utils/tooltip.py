"""
Visual feedback utilities for EZLife Tool.
Provides tooltip notifications near the cursor.
"""
import threading
import tkinter as tk


def show_tooltip(text, duration=1200, offset_x=20, offset_y=20):
    """
    Show a tooltip notification near the mouse cursor.
    
    Args:
        text: Text to display in the tooltip
        duration: How long to show the tooltip in milliseconds (default: 1200)
        offset_x: Horizontal offset from cursor (default: 20)
        offset_y: Vertical offset from cursor (default: 20)
    """
    def _run():
        try:
            root = tk.Tk()
            root.overrideredirect(True)
            root.attributes("-topmost", True)
            
            # Estilo simple blanco y negro
            lbl = tk.Label(
                root,
                text=text,
                bg="#ffffff",  # Fondo blanco
                fg="#000000",  # Texto negro
                font=("Segoe UI", 9),  # Fuente normal de Windows
                padx=8,
                pady=4,
                relief="solid",
                borderwidth=1
            )
            lbl.pack()
            
            # Posición near mouse cursor
            x, y = root.winfo_pointerx(), root.winfo_pointery()
            root.geometry(f"+{x + offset_x}+{y + offset_y}")
            
            # Auto-close after duration
            root.after(duration, root.destroy)
            root.mainloop()
        except Exception as e:
            print(f"Error showing tooltip: {e}")
    
    # Run in separate thread to avoid blocking
    threading.Thread(target=_run, daemon=True).start()


def show_success(text):
    """Show a success tooltip with checkmark."""
    show_tooltip(f"✅ {text}")


def show_error(text):
    """Show an error tooltip with X mark."""
    show_tooltip(f"❌ {text}")


def show_info(text):
    """Show an info tooltip with info icon."""
    show_tooltip(f"ℹ️ {text}")
