# OS
import os
# Threading
import ctypes
import threading
import multiprocessing
# Tkinter
import tkinter as tk
from tkinter import filedialog
# Whisper
from faster_whisper import WhisperModel
# GUI
from gui import GUI

def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    global files_path
    files_path = []

    if folder_path == "":
        return
    
    for file in os.listdir(folder_path):
        if file.endswith(".mp3"):
            files_path.append(f"{folder_path}/{file}")

    GUI.update_label(GUI.folder_info, f'Cartella: {folder_path}')
    GUI.update_label(GUI.files_info, f'File audio (.mp3) trovati: {len(files_path)}')   
    GUI.clear_console_output()
    GUI.update_button(GUI.start_transcribe_button, tk.NORMAL)

def transcribe():
    GUI.update_console_output("Inizializzazione del modello in corso...\n")
    model = WhisperModel('large-v3', device="cpu", compute_type="int8")
    GUI.update_console_output("Inizializzazione completata.\n\n")

    s2t_folder = f"{folder_path}/S2T"
    
    if not os.path.exists(s2t_folder):
        os.mkdir(s2t_folder)
    
    for file_path in files_path:
        file_name = file_path.split("/")[-1].replace(".mp3", ".txt")

        GUI.update_console_output(f"File: {file_path}\n")

        segments, info = model.transcribe(file_path, beam_size=5)
        
        GUI.update_console_output(f"Lingua: {info.language.upper()} ({info.language_probability}%)\n")
            
        with open(f"{s2t_folder}/{file_name}", "w") as f:
            for segment in segments:
                f.write(segment.text.strip() + "\n")
                f.flush()

                GUI.update_console_output(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n")

        GUI.update_console_output("\n")

    GUI.update_label(GUI.folder_info, "Trascrizione completata!")
    GUI.update_label(GUI.files_info, f'File audio trascritti: {len(files_path)}')
    GUI.update_console_output("Trascrizione completata.")
    GUI.update_button(GUI.select_folder_button, tk.NORMAL)
    GUI.update_button(GUI.stop_transcribe_button, tk.DISABLED)

def start_transcribe_thread():
    global transcribe_thread
    transcribe_thread = threading.Thread(target=transcribe, daemon=True)
    transcribe_thread.start()

    GUI.update_console_output("Transcrizione avviata.\n")
    GUI.update_button(GUI.select_folder_button, tk.DISABLED)
    GUI.update_button(GUI.start_transcribe_button, tk.DISABLED)
    GUI.update_button(GUI.stop_transcribe_button, tk.NORMAL)

def end_transcribe_thread():
    ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(transcribe_thread.ident), ctypes.py_object(SystemExit))
    transcribe_thread.join()

    GUI.update_label(GUI.folder_info, '')
    GUI.update_label(GUI.files_info, '')
    GUI.update_console_output("Transcrizione interrotta.\n")
    GUI.update_button(GUI.select_folder_button, tk.NORMAL)
    GUI.update_button(GUI.stop_transcribe_button, tk.DISABLED)

# GUI
def main():
    GUI(select_folder, start_transcribe_thread, end_transcribe_thread)
    
if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()