# OS
import os
import time
# Threading
import ctypes
import threading
import multiprocessing
# Tkinter
import tkinter as tk
from tkinter import filedialog
# PSUtil
import psutil
# GUI
from gui import GUI
# Transcription
from transcription import TranscriptionService

def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    global files_path
    files_path = []

    if folder_path == "":
        return
    
    for file in os.listdir(folder_path):
        if file.endswith(".mp3") or file.endswith(".wav") or file.endswith(".m4a"):
            files_path.append(f"{folder_path}/{file}")

    UI.update_label(UI.folder_info, f'Cartella: {folder_path}')
    UI.update_label(UI.files_info, f'File audio trovati: {len(files_path)}')   
    UI.clear_console_output()

    if len(files_path) > 0:
        UI.update_button(UI.start_transcribe_button, tk.NORMAL)


def transcribe():
    service = TranscriptionService(UI, folder_path)
    
    for file_path in files_path:
        service.transcribe(file_path)

    os.system(f"rm -rf {folder_path}/chunks")    
    os.system(f"open {folder_path}/S2T")

    UI.update_label(UI.folder_info, "Trascrizione completata!")
    UI.update_label(UI.files_info, f'File audio trascritti: {len(files_path)}')
    UI.update_console_output("Trascrizione completata.")
    UI.update_button(UI.select_folder_button, tk.NORMAL)
    UI.update_button(UI.stop_transcribe_button, tk.DISABLED)

def start_transcribe_thread():
    global transcribe_thread
    transcribe_thread = threading.Thread(target=transcribe, daemon=True)
    transcribe_thread.start()

    UI.update_console_output("Transcrizione avviata.\n")
    UI.update_button(UI.select_folder_button, tk.DISABLED)
    UI.update_button(UI.start_transcribe_button, tk.DISABLED)
    UI.update_button(UI.stop_transcribe_button, tk.NORMAL)

def end_transcribe_thread():
    ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(transcribe_thread.ident), ctypes.py_object(SystemExit))
    transcribe_thread.join()

    UI.update_label(UI.folder_info, '')
    UI.update_label(UI.files_info, '')
    UI.update_console_output("Transcrizione interrotta.\n")
    UI.update_button(UI.select_folder_button, tk.NORMAL)
    UI.update_button(UI.stop_transcribe_button, tk.DISABLED)

def check_memory_usage():
    while True:
        memory = psutil.virtual_memory()
        memory_usage = memory.used / (1024 ** 3)
        memory_usage_percent = memory.percent
        memory_available = memory.available / (1024 ** 3)
        memory_total = memory.total / (1024 ** 3)

        UI.update_label(UI.memory_info, f'Memoria Utilizzata: {memory_usage:.2f} GB ({memory_usage_percent}%), Disponibile: {memory_available:.2f} GB, Totale: {memory_total:.2f} GB')

        time.sleep(1)

def start_memory_thread():
    global memory_thread
    memory_thread = threading.Thread(target=check_memory_usage, daemon=True)
    memory_thread.start()

# GUI
def main():
    global UI
    UI = GUI(select_folder, start_transcribe_thread, end_transcribe_thread)

    start_memory_thread()

    UI.window.mainloop()
    
if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()