import os
import wave
import json
from vosk import Model, KaldiRecognizer

def interpretar_vosk(audio_path):
    # Carregar o modelo do Vosk
    model_path = "C:/smartpassvoice/vosk-model-small-pt-0.3/"  # Altere para o caminho do modelo
    model = Model(model_path)

    # Abrir o arquivo de áudio
    with wave.open(audio_path, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("Arquivo de áudio precisa ser mono, com 16kHz e 16 bits de profundidade.")

        recognizer = KaldiRecognizer(model, wf.getframerate())

        # Iniciar o reconhecimento de fala
        texto = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                texto += json.loads(result)["text"] + " "

        # Retornar o texto reconhecido
        result = recognizer.FinalResult()
        texto += json.loads(result)["text"]
        return texto.strip()
