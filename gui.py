# Tkinter
import tkinter as tk
from tkinter import scrolledtext

class GUI:
    def __init__(self, select_folder, start_transcribe_thread, end_transcribe_thread):
        self.window = tk.Tk()
        self.window.title("Speech to Text by isladot")
        self.window.geometry("1000x700")
        self.window.resizable(False, False)
        self.window.configure(bg="#ffffff")
        self.window.grid_columnconfigure(0, weight=1)

        # Title
        title = tk.Label(self.window, text="Benvenuto,\nseleziona la cartella con i file audio da trascrivere:", font=("Helvetica", 16), fg="#000000", bg="#ffffff")
        title.grid(row=0, column=0, sticky=tk.N, pady=(15, 0))
        # Subtitle
        subtitle = tk.Label(self.window, text="Formati audio supportati: .mp3, .wav, .m4a", font=("Helvetica", 12), fg="#000000", bg="#ffffff")
        subtitle.grid(row=1, column=0, sticky=tk.N, pady=(0, 15))

        # Select Folder
        self.select_folder_button = tk.Button(self.window, text="Seleziona...", font=("Helvetica", 12), fg="#000000", width=10, height=1, borderwidth=0, command=select_folder)
        self.select_folder_button.grid(row=2, column=0, sticky=tk.N)

        # Folder Info
        self.folder_info = tk.Label(self.window, font=("Helvetica", 12), fg="#000000", bg="#ffffff", height=1, borderwidth=1)
        self.folder_info.grid(row=3, column=0, sticky=tk.N, pady=(15, 0))
        
        # Files Info
        self.files_info = tk.Label(self.window, font=("Helvetica", 12), fg="#000000", bg="#ffffff", height=1, borderwidth=1)
        self.files_info.grid(row=4, column=0, sticky=tk.N, pady=(0, 15))

        # Memory Info
        self.memory_info = tk.Label(self.window, font=("Helvetica", 12), fg="#000000", bg="#ffffff", height=1, borderwidth=1)
        self.memory_info.grid(row=5, column=0, sticky=tk.N, pady=(0, 15))

        # Console Output
        self.console_output = scrolledtext.ScrolledText(self.window, font=("Helvetica", 12), width=100, height=15, state=tk.DISABLED)
        self.console_output.grid(row=6, column=0, sticky=tk.N, pady=15, padx=(15, 0))

        # Start Transcribe Button
        self.start_transcribe_button = tk.Button(self.window, text="Avvia Transcrizione", font=("Helvetica", 12), fg="#000000", width=20, height=1, borderwidth=0, command=start_transcribe_thread, state=tk.DISABLED)
        self.start_transcribe_button.grid(row=7, column=0, sticky=tk.W, padx=(200, 0))

        # Stop Transcribe Button
        self.stop_transcribe_button = tk.Button(self.window, text="Interrompi Transcrizione", font=("Helvetica", 12), fg="#000000", width=20, height=1, borderwidth=0, command=end_transcribe_thread, state=tk.DISABLED)
        self.stop_transcribe_button.grid(row=7, column=0, sticky=tk.E, padx=(0, 200))

    def update_button(self, button, state):
        button.config(state=state)

    def update_label(self, label, text):
        label.config(text=text)

    def update_console_output(self, text):
        self.console_output.config(state=tk.NORMAL)
        self.console_output.insert(tk.END, text)
        self.console_output.update()
        self.console_output.config(state=tk.DISABLED)

        print(text.replace("\n", ""))

    def clear_console_output(self):
        self.console_output.config(state=tk.NORMAL)
        self.console_output.delete('0.0', tk.END)
        self.console_output.update()
        self.console_output.config(state=tk.DISABLED)