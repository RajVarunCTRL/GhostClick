import tkinter as tk
import threading
import time
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key, Controller as KeyboardController

# THEME CONFIGURATION MODE

"""
        bg              =   MAIN BACKGROUND
        fg              =   MAIN TEXT COLOR
        input_bg        =   Dropdown and entry box background
        hover_bg        =   Dropdown hover color
        status_active   =   Color for STATUS BAR
        status_inactive =   Color for STATUS BAR
        footer_fg       =   Muted text for the footer
    """

THEMES = {
    
    "dark": {
        "bg": "#1e1e2e",             
        "fg": "#cdd6f4",             
        "input_bg": "#313244",       
        "hover_bg": "#45475a",       
        "status_active": "#a6e3a1",  
        "status_inactive": "#f38ba8",
        "footer_fg": "#a6adc8",
        "credits" : "#86ffc8"
    },
    
    "light": {
        "bg": "#eff1f5",
        "fg": "#4c4f69",
        "input_bg": "#e6e9ef",
        "hover_bg": "#ccd0da",
        "status_active": "#40a02b",
        "status_inactive": "#d20f39",
        "footer_fg": "#8c8fa1",
        "credits" : "#000000"
    },
    
    "full_dark": {
        "bg": "#000000",             
        "fg": "#ffffff",             
        "input_bg": "#111111",       
        "hover_bg": "#222222",       
        "status_active": "#00ff00",  
        "status_inactive": "#ff3333",
        "footer_fg": "#888888",       
        "credits" : "#86ffc8"
    }
}

class GhostClickApp: 
    def __init__(self,root):
        self.root = root
        self.root.title("GhostClick v1.3")
        self.root.geometry("460x220") 
        self.root.resizable(False,False)
        
        self.root.attributes("-topmost", True)
        
        # LOAD THEME CONFIG
        self.theme_name = "full_dark" # Swap your theme here.
        
        self.theme = THEMES[self.theme_name]
        
        self.root.configure(bg=self.theme["bg"])

        # bools
        self.clicking = False
        self.program_running = True 
        
        # Controllers
        self.mouse = Controller()
        self.keyboard = KeyboardController()
        
        # setting_vars
        self.current_delay = 0.05
        self.current_action = "Left Click"
        self.current_key = "e"
        
        
        # The LAYOUT
        self.status_label = tk.Label(
            root, 
            text="STATUS: INACTIVE", 
            fg=self.theme["status_inactive"], 
            bg=self.theme["bg"],
            font=("Arial", 14, "bold")
        )
        self.status_label.pack(pady=(15,5))

        # Settings Frame
        settings_frame = tk.Frame(root, bg=self.theme["bg"])
        settings_frame.pack(pady=10, padx=20, fill="x")
        
        # settings_frame.columnconfigure(0, weight=1)
        # settings_frame.columnconfigure(1, weight=1)

        # ROW 0 
        
        # Action Label (COL 0)
        tk.Label(
            settings_frame, 
            text="Action:", 
            fg=self.theme["fg"], 
            bg=self.theme["bg"],
            font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="e", pady=5, padx=(0,5))
        
        # Dropdown Lst COL 1
        self.action_var = tk.StringVar(value="Left Click")
        self.action_menu = tk.OptionMenu(settings_frame, self.action_var, "Left Click", "Right Click", "Middle Click", "Key Press")
        self.action_menu.config(
            bg=self.theme["input_bg"], 
            fg=self.theme["fg"], 
            highlightthickness=0, 
            width=12, 
            activebackground=self.theme["hover_bg"], 
            activeforeground=self.theme["fg"]
        )
        self.action_menu.grid(row=0, column=1,sticky="w",pady=5, padx=(0,25))
        
        # COl 2
        # Key Press ka input
        tk.Label(
            settings_frame,
            text="Key to Tap:",
            fg=self.theme["fg"], 
            bg=self.theme["bg"],
            font=("Arial", 10, "bold")).grid(row=0, column=2, sticky="e", pady=5, padx=(0,5))
        self.key_var  = tk.StringVar(value="e")
        
        # KEY PRESS (COL 3)
        self.key_entry = tk.Entry(
                            settings_frame, 
                            textvariable=self.key_var, 
                            width=10, 
                            fg=self.theme["fg"], 
                            bg=self.theme["bg"], 
                            insertbackground=self.theme["fg"], 
                            state="disabled", justify="center"
                        )
        self.key_entry.grid(row=0, column=3, sticky="w", pady=5)
        
    # ROW 1
        # Delay input by (ms)
        tk.Label(
            settings_frame,
            text="Delay (ms):",
            fg=self.theme["fg"], 
            bg=self.theme["bg"],
            font=("Arial",10, "bold")).grid(row=1,column=2,sticky='e',pady=5, padx=(10,5))

        # Delay Entry (COL 3)
        self.delay_var=tk.StringVar(value="10")
        self.delay_entry = tk.Entry(
                                    settings_frame, 
                                    textvariable=self.delay_var,
                                    width=10,
                                    fg=self.theme["fg"], 
                                    bg=self.theme["bg"],
                                    insertbackground="white",
                                    justify="center")
        self.delay_entry.grid(row=1,column=3,sticky="w",pady=5)
        
        
        # More listeners
        self.action_var.trace_add("write",self.update_settings)
        self.key_var.trace_add("write", self.update_settings)
        self.delay_var.trace_add("write", self.update_settings)
        
        self.credit_label = tk.Label(
            root, 
            text = "Made with care by Raj Varun",
            fg=self.theme["credits"],
            bg=self.theme["bg"],
            font=("Arial", 10, "italic")
        )
        self.credit_label.pack(side="bottom", pady=(0,5))
        
        
        self.info_label = tk.Label(
                            root, 
                            text="Press [ F8 ] to Start / Stop\nPress [ F9 ] to Exit App", 
                            fg=self.theme["fg"], 
                            bg=self.theme["bg"],
                            font=("Arial", 10, "bold")
                        )
        self.info_label.pack(side="bottom",pady=(0,15))

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
            try:
                if self.credit_label.cget("text") != "Made with care by Raj Varun":
                    time.sleep(1)
                    continue
            except Exception:
                break
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
            self.status_label.config(text="Status: Active", fg=self.theme["status_active"])
        else:
            self.status_label.config(text="Status: Inactive", fg=self.theme["status_inactive"])
    
    def close_application(self):
        self.clicking = False
        self.program_running = False
        self.listener_thread.stop()
        self.root.destroy()
    
    
if __name__ == "__main__":
    root = tk.Tk()
    app = GhostClickApp(root)
    root.mainloop()
