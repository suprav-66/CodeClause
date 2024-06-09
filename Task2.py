import tkinter as tk
from tkinter import messagebox
import time

class TypingSpeedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Calculator")
        self.root.geometry("500x300")

        # Set background color
        self.root.configure(bg="#808080")

        # Center the window
        self.root.eval('tk::PlaceWindow . center')

        # Add heading
        self.heading_label = tk.Label(root, text="Typing Speed Calculator", bg="#FFD700", font=("Arial", 24, "bold"))
        self.heading_label.pack(pady=10)

        self.label_instruction = tk.Label(root, text="Type the text below as fast as you can and press Enter when done:", bg="#e0e0e0", font=("Arial", 16, "bold"))
        self.label_instruction.pack()

        self.text_to_type = "The quick brown fox jumps over the lazy dog"
        self.label_text_to_type = tk.Label(root, text=self.text_to_type, wraplength=480, bg="#d0d0d0", font=("Arial", 16, "bold"))
        self.label_text_to_type.pack()

        self.entry = tk.Entry(root, width=50, font=("Arial", 10))
        self.entry.pack(pady=20)

        self.start_button = tk.Button(root, text="Start Typing", command=self.start_typing, bg="#f0f0f0", font=("Arial", 14, "bold"))
        self.start_button.pack(pady=10)

        self.show_speed_button = tk.Button(root, text="Show Speed", command=self.calculate_speed, bg="#f0f0f0", font=("Arial", 14, "bold"))
        self.show_speed_button.pack(pady=10)

        self.start_time = None

        self.entry.bind("<Return>", self.calculate_speed)

    def calculate_speed(self, event=None):
        if not self.start_time:
            messagebox.showwarning("Warning", "Please start typing first.")
            return

        end_time = time.time()
        total_time = end_time - self.start_time

        typed_text = self.entry.get()
        typed_words = typed_text.split()
        typed_word_count = len(typed_words)

        wpm = (typed_word_count / total_time) * 60

        messagebox.showinfo("Typing Speed", f"Your typing speed is: {round(wpm)} WPM")

        self.start_time = None
        self.entry.delete(0, tk.END)

    def start_typing(self):
        self.start_time = time.time()

if __name__ == "__main__":
    root = tk.Tk()
    typing_speed_calculator = TypingSpeedCalculator(root)
    root.mainloop()
