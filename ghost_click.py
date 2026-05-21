import tkinter as tk
import threading
import time
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key

class GhostClickApp: 
    def __init__(self,root):
        self.root = root
        self.root.title("GhostClick v1")
        self.root.geometry("300x360") 
        self.root.resizable(False,False)
        
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#1e1e2e")

        # bools
        self.clicking = False
        self.program_running = True 
        

        self.click_delay = 0.05
        self.mouse = Controller()
        
        
        self.status_label = tk.Label(
            root, 
            text="STATUS: INACTIVE", 
            fg="#f38ba8", # Soft red
            bg="#1e1e2e",
            font=("Arial", 14, "bold")
        )
        self.status_label.pack(pady=15)

        self.info_label = tk.Label(
            root, 
            text="Press [ F8 ] to Start / Stop\nPress [ F9 ] to Exit App", 
            fg="#cdd6f4", # Soft white
            bg="#1e1e2e",
            font=("Arial", 10, "bold")
        )
        self.info_label.pack()

        # Handles clicking logic so the GUI doesn't freeze
        self.click_thread = threading.Thread(target=self.clicker_loop)
        self.click_thread.start()

        # Listener for background keyboard events globally
        self.listener_thread = Listener(on_press=self.on_press)
        self.listener_thread.start()

        # Safe close exit protocol
        self.root.protocol("WM_DELETE_WINDOW", self.close_application) 
        
        
    # Methods for Ghost Click 
    
    def clicker_loop(self):
        while self.program_running :
            if self.clicking :
                self.mouse.click(Button.left, 1)
                time.sleep(self.click_delay)
            else:
                time.sleep(0.01)
                
    def on_press(self, key):
        if key == Key.f8:
            self.toggle_clicking()
        elif key == Key.f9:
            self.root.after(0, self.close_application)
            
            
    def toggle_clicking(self):
        self.clicking = not self.clicking
        if self.clicking:
            self.status_label.config(text="Status: Active", fg="#a6e3a1")
        else:
            self.status_label.config(text="Status: Inactive", fg="#f38ba8")
    
    def close_application(self):
        self.clicking = False
        self.program_running = False
        self.listener_thread.stop()
        self.root.destroy()
    
    
if __name__ == "__main__":
    root = tk.Tk()
    app = GhostClickApp(root)
    root.mainloop()
        