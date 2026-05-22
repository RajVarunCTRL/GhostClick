import tkinter as tk
import threading
import time
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key, Controller as KeyboardController

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
        
        # Controllers
        self.mouse = Controller()
        self.keyboard = KeyboardController()
        
        # setting_vars
        self.click_delay = 0.05
        self.current_action = "Left Click"
        self.current_key = "e"
        
        
        # The LAYOUT
        self.status_label = tk.Label(
            root, 
            text="STATUS: INACTIVE", 
            fg="#f38ba8", 
            bg="#1e1e2e",
            font=("Arial", 14, "bold")
        )
        self.status_label.pack(pady=10)

        # Settings Frame
        settings_frame = tk.Frame(root, bg="#1e1e2e")
        settings_frame.pack(pady=5)

        # Dropdown Lst
        tk.Label(
            settings_frame, 
            text="Action", 
            fg="#cdd6f4", 
            bg="#1e1e2e",
            font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
        
        self.action_var = tk.StringVar("LeftClick")
        self.action_menu = tk.OptionMenu(settings_frame, self.action_var, "Left Click", "Right Click", "Middle Click", "Key Press")
        self.action_menu.config(bg="#313244", fg="#cdd6f4", highlightthickness=0)
        self.action_menu.grid(row=0, column=0,sticky="w",pady=5)
        
        # Key Press ka input
        tk.Label(
            settings_frame,
            text="Key to Tap:",
            fg="#cdd6f4",
            bg="#1e1e2e",
            font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5, padx=5)

        self.key_entry = tk.Entry(settings_frame, textvariable=self.key_var, width=5, bg="#313244", fg="#cdd6f4", insertbackground="white", state="disabled")
        self.key_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        
        # Delay input by (ms)
        tk.Label(
            settings_frame,
            text="Delay (ms):",
            fg="#cdd6f4",
            bg="#1e1e2e",
            font=("Arial",10)).grid(row=1,column=0,sticky='e',padx=5,pady=5)

        self.delay_var=tk.StringVar(value="50")
        self.delay_entry = tk.Entry(
                                    settings_frame, 
                                    textvariable=self.delay_var,
                                    width=8,
                                    bg="#313244",
                                    fg="#cdd6f4",
                                    insertbackground="white")
        self.delay_entry.grid(row=2,column=1,sticky="w",pady=5)
        
        
        # More listeners
        self.action_var.trace_add("write",self.update_settings)
        self.key_var.trace_add("write", self.update_settings)
        self.delay_var.trace_add("write", self.update_settings)
        
        
        
        self.info_label = tk.Label(
                            root, 
                            text="Press [ F8 ] to Start / Stop\nPress [ F9 ] to Exit App", 
                            fg="#cdd6f4", 
                            bg="#1e1e2e",
                            font=("Arial", 10, "bold")
                        )
        self.info_label.pack(pady=15)

        # Handles clicking logic so the GUI doesn't freeze
        self.click_thread = threading.Thread(target=self.clicker_loop)
        self.click_thread.start()

        # Listener for background keyboard events globally
        self.listener_thread = Listener(on_press=self.on_press)
        self.listener_thread.start()

        # Safe close exit protocol
        self.root.protocol("WM_DELETE_WINDOW", self.close_application) 
        
        
    # Methods for Ghost Click 
    
    def update_settings(self, *args):
        """Update internal variables safely."""
        self.current_action = self.action_var.get()
        self.current_key = self.key_var.get()
        
        if self.current_action == "Key Press":
            self.key_entry.config(state="normal")
        else:
            self.key_entry.config(state= "disabled")
            
        # ms to secs for sleep func
        try:
            ms = int(self.delay_var.get())
            self.current_delay = max(0.001,ms/1000.0)
        except ValueError:
            pass # Uses the old value in case of character set by the user.       
        
    def clicker_loop(self):
        while self.program_running :
            if self.clicking :
                if self.current_action == "Left Click":
                    self.mouse.click(Button.left, 1)
                elif self.current_action == "Right Click":
                    self.mouse.click(Button.right, 1)
                elif self.current_action == "Middle Click":
                    self.mouse.click(Button.middle, 1)
                elif self.current_action == "Key Press" and len(self.current_key) > 0:
                    char = self.current_key[0]
                    self.keyboard.press(char)
                    self.keyboard.release(char)
                time.sleep(self.current_delay)
            else:
                time.sleep(0.01)
            #     self.mouse.click(Button.left, 1)
            #     time.sleep(self.click_delay)
            # else:
            #     time.sleep(0.01)
                
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
        