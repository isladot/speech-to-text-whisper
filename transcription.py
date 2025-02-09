# OS
import os
# Whisper
from faster_whisper import WhisperModel
# PyDub
from pydub import AudioSegment, utils
# GUI
from gui import GUI

class TranscriptionService:
    def __init__(self, UI, audio_files_path):
        self.UI: GUI = UI
        self.audio_chunks_path = f"{audio_files_path}/chunks"
        self.s2t_files_path = f"{audio_files_path}/S2T"

        if not os.path.exists(self.s2t_files_path):
            os.mkdir(self.s2t_files_path)

        self.model_init()

    def model_init(self):
        self.UI.update_console_output("Inizializzazione del modello in corso...\n")
        self.whisper = WhisperModel('large-v3', device="cpu", compute_type="int8")
        self.UI.update_console_output("Inizializzazione completata.\n\n")

    def transcribe(self, audio_file_path):
        self.UI.update_console_output(f"File: {audio_file_path}\n")

        self.file_name_with_ext = audio_file_path.split("/")[-1]
        self.file_name = self.file_name_with_ext.split(".")[0]

        self.generate_audio_chunks(audio_file_path)
        self.transcribe_audio_from_chunks()

    def generate_audio_chunks(self, file):
        audio = AudioSegment.from_file(file)
        chunks = utils.make_chunks(audio, 5 * 60 * 1000)

        self.chunk_path = f"{self.audio_chunks_path}/{self.file_name}"

        if os.path.exists(self.chunk_path):
            os.system(f"rm -rf {self.chunk_path}")
        
        os.makedirs(self.chunk_path)

        for i, chunk in enumerate(chunks):
            chunk.export(f"{self.chunk_path}/{i}.wav", format="wav")

        self.UI.update_console_output(f"File audio diviso in {len(chunks)} chunks.\n\n")

    def transcribe_audio_from_chunks(self):
        for i, chunk in enumerate(sorted(os.listdir(self.chunk_path), key=lambda x: int(x.split(".")[0]))):
            segments, info = self.whisper.transcribe(f"{self.chunk_path}/{chunk}", beam_size=5)

            self.UI.update_console_output(f"Trascrizione del chunk {chunk} in corso...\n")
            self.UI.update_console_output(f"Lingua: {info.language.upper()} ({info.language_probability}%)\n")

            with open(f"{self.s2t_files_path}/{self.file_name}.txt", i == 0 and "w" or "a") as f:
                for segment in segments:
                    f.write(segment.text.strip() + "\n")
                    f.flush()

                    self.UI.update_console_output(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n")

            self.UI.update_console_output("\n")

        