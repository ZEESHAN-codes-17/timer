import tkinter as tk
from tkinter import messagebox
import time
import threading
import math
import winsound

class AttractiveTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Attractive Countdown Timer")
        self.root.geometry("450x650")
        self.root.configure(bg='#2d1b69')
        self.root.resizable(False, False)
        
        # Timer variables
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.running = False
        self.timer_thread = None
        self.flash = False
        
        # Create UI
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="⏰ SET TIMER", 
                              font=('Arial', 24, 'bold'),
                              bg='#2d1b69', fg='#ffeb3b')
        title_label.pack(pady=20)
        
        # Input frame for hours, minutes, seconds
        input_frame = tk.Frame(self.root, bg='#2d1b69')
        input_frame.pack(pady=20)
        
        # Labels
        tk.Label(input_frame, text="Hours", font=('Arial', 12),
                bg='#2d1b69', fg='#ffeb3b').grid(row=0, column=0, padx=10)
        tk.Label(input_frame, text="Minutes", font=('Arial', 12),
                bg='#2d1b69', fg='#ffeb3b').grid(row=0, column=2, padx=10)
        tk.Label(input_frame, text="Seconds", font=('Arial', 12),
                bg='#2d1b69', fg='#ffeb3b').grid(row=0, column=4, padx=10)
        
        # Time input variables
        self.hour_var = tk.StringVar(value="0")
        self.min_var = tk.StringVar(value="0") 
        self.sec_var = tk.StringVar(value="0")
        
        # Entry widgets
        self.hour_entry = tk.Entry(input_frame, width=4, font=('Arial', 16),
                                  textvariable=self.hour_var, justify='center',
                                  bg='#4a148c', fg='#ffeb3b', bd=2,
                                  insertbackground='#ffeb3b')
        self.hour_entry.grid(row=1, column=0, padx=10, pady=5)
        
        tk.Label(input_frame, text=":", font=('Arial', 20, 'bold'),
                bg='#2d1b69', fg='#e91e63').grid(row=1, column=1)
        
        self.min_entry = tk.Entry(input_frame, width=4, font=('Arial', 16),
                                 textvariable=self.min_var, justify='center',
                                 bg='#4a148c', fg='#ffeb3b', bd=2,
                                 insertbackground='#ffeb3b')
        self.min_entry.grid(row=1, column=2, padx=10, pady=5)
        
        tk.Label(input_frame, text=":", font=('Arial', 20, 'bold'),
                bg='#2d1b69', fg='#e91e63').grid(row=1, column=3)
        
        self.sec_entry = tk.Entry(input_frame, width=4, font=('Arial', 16),
                                 textvariable=self.sec_var, justify='center',
                                 bg='#4a148c', fg='#ffeb3b', bd=2,
                                 insertbackground='#ffeb3b')
        self.sec_entry.grid(row=1, column=4, padx=10, pady=5)
        
        # Canvas for circular progress
        self.canvas = tk.Canvas(self.root, width=220, height=220, 
                               bg='#2d1b69', highlightthickness=0)
        self.canvas.pack(pady=30)
        
        # Time display
        self.time_label = tk.Label(self.root, text="00:00:00", 
                                  font=('Courier New', 32, 'bold'),
                                  bg='#2d1b69', fg='#e91e63')
        self.time_label.pack(pady=10)
        
        # MAIN START BUTTON - Large and prominent
        self.start_btn = tk.Button(self.root, text="▶ START TIMER", 
                                  font=('Arial', 18, 'bold'),
                                  bg='#ffeb3b', fg='#2d1b69',
                                  bd=0, relief='flat',
                                  activebackground='#fdd835',
                                  activeforeground='#2d1b69',
                                  cursor='hand2',
                                  width=15, height=2,
                                  command=self.start_timer)
        self.start_btn.pack(pady=25)
        
        # Secondary buttons frame
        button_frame = tk.Frame(self.root, bg='#2d1b69')
        button_frame.pack(pady=15)
        
        self.stop_btn = tk.Button(button_frame, text="⏸ STOP", 
                                 font=('Arial', 12, 'bold'),
                                 bg='#e91e63', fg='#ffffff',
                                 bd=0, relief='flat',
                                 activebackground='#c2185b',
                                 activeforeground='#ffffff',
                                 cursor='hand2',
                                 width=8, height=1,
                                 command=self.stop_timer)
        self.stop_btn.grid(row=0, column=0, padx=20)
        
        self.reset_btn = tk.Button(button_frame, text="🔄 RESET", 
                                  font=('Arial', 12, 'bold'),
                                  bg='#ff9800', fg='#ffffff',
                                  bd=0, relief='flat',
                                  activebackground='#f57c00',
                                  activeforeground='#ffffff',
                                  cursor='hand2',
                                  width=8, height=1,
                                  command=self.reset_timer)
        self.reset_btn.grid(row=0, column=1, padx=20)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready to start", 
                                    font=('Arial', 12),
                                    bg='#2d1b69', fg='#ffeb3b')
        self.status_label.pack(pady=15)
        
        # Draw initial circle
        self.draw_circle(1.0)
    
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.root.winfo_screenheight() // 2) - (650 // 2)
        self.root.geometry(f"450x650+{x}+{y}")
    
    def draw_circle(self, progress):
        self.canvas.delete("all")
        
        # Draw background circle
        self.canvas.create_oval(30, 30, 190, 190, 
                               outline='#4a148c', width=10, fill='')
        
        # Draw progress arc
        if progress > 0:
            start_angle = 90  # Start from top
            extent_angle = -360 * progress  # Negative for clockwise
            
            # Create gradient effect with multiple arcs
            colors = ['#e91e63', '#f06292', '#f8bbd9', '#fce4ec']
            for i, color in enumerate(colors):
                offset = i * 1
                self.canvas.create_arc(30 + offset, 30 + offset, 
                                     190 - offset, 190 - offset,
                                     start=start_angle, extent=extent_angle,
                                     outline=color, width=3, style='arc')
        
        # Add center glow
        if progress > 0:
            for i in range(5):
                alpha_offset = i * 15
                self.canvas.create_oval(90 - alpha_offset, 90 - alpha_offset, 
                                      130 + alpha_offset, 130 + alpha_offset,
                                      outline='#e91e63', width=1, fill='')
    
    def start_timer(self):
        if self.running:
            return
            
        try:
            hours = int(self.hour_var.get() or 0)
            minutes = int(self.min_var.get() or 0) 
            seconds = int(self.sec_var.get() or 0)
            self.total_seconds = hours * 3600 + minutes * 60 + seconds
            
            if self.total_seconds <= 0:
                raise ValueError("Time must be greater than 0")
                
        except ValueError as e:
            messagebox.showerror("Invalid Input", 
                               "Please enter valid numbers for hours, minutes, and seconds.")
            return
        
        self.remaining_seconds = self.total_seconds
        self.running = True
        self.start_btn.config(state="disabled", bg='#9e9e9e')
        self.status_label.config(text="Timer running...")
        
        # Start timer thread
        self.timer_thread = threading.Thread(target=self.countdown, daemon=True)
        self.timer_thread.start()
    
    def stop_timer(self):
        self.running = False
        self.start_btn.config(state="normal", bg='#ffeb3b')
        self.status_label.config(text="Timer stopped")
    
    def reset_timer(self):
        self.running = False
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.start_btn.config(state="normal", bg='#ffeb3b')
        self.time_label.config(text="00:00:00", fg='#e91e63')
        self.status_label.config(text="Ready to start")
        self.draw_circle(1.0)
        self.flash = False
    
    def countdown(self):
        while self.remaining_seconds > 0 and self.running:
            # Update display on main thread
            self.root.after(0, self.update_display)
            time.sleep(1)
            self.remaining_seconds -= 1
            
        if self.running:  # Timer finished normally
            self.root.after(0, self.timer_done)
    
    def update_display(self):
        # Update time display
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.time_label.config(text=time_str)
        
        # Update progress circle
        if self.total_seconds > 0:
            progress = self.remaining_seconds / self.total_seconds
            self.draw_circle(progress)
        
        # Change color when time is running low
        if self.remaining_seconds <= 10:
            self.time_label.config(fg='#ff5722')
        elif self.remaining_seconds <= 60:
            self.time_label.config(fg='#ffeb3b')
        else:
            self.time_label.config(fg='#e91e63')
    
    def timer_done(self):
        self.running = False
        self.start_btn.config(state="normal", bg='#ffeb3b')
        self.time_label.config(text="00:00:00", fg='#ff5722')
        self.status_label.config(text="⏰ Time's up!")
        self.draw_circle(0.0)
        
        # Start flash animation and sound alert
        self.flash = True
        threading.Thread(target=self.flash_animation, daemon=True).start()
        threading.Thread(target=self.sound_alert, daemon=True).start()
        
        messagebox.showinfo("Time's Up!", "Time's up!")
    
    def flash_animation(self):
        original_fg = '#ff5722'
        original_bg = '#2d1b69'
        
        for _ in range(15):
            if not self.flash:
                break
            # Flash to bright colors
            self.root.after(0, lambda: self.time_label.config(fg='#2d1b69', bg='#ffeb3b'))
            time.sleep(0.3)
            # Flash back to normal
            self.root.after(0, lambda: self.time_label.config(fg=original_fg, bg=original_bg))
            time.sleep(0.3)
        
        self.flash = False
    
    def sound_alert(self):
        # "Beep bop beep bop" sound pattern with winsound
        end_time = time.time() + 7
        while time.time() < end_time:
            winsound.Beep(1000, 300)
            winsound.Beep(1200, 300)
            time.sleep(0.1)

def main():
    root = tk.Tk()
    timer_app = AttractiveTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()