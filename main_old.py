import datetime
import os
import pyaudio
import wave
from voice_recognition import interpretar_speech_recognition
from voice_recognition_vosk import interpretar_vosk
from voice_recognition_whisper import interpretar_whisper
from db import salvar_evento, salvar_audio_no_banco

# Configurações de gravação
AUDIO_DIR = "audios"
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5

def gravar_audio(nome_arquivo):
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    audio_path = os.path.join(AUDIO_DIR, nome_arquivo)

    p = pyaudio.PyAudio()

    print("Gravando áudio...")
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Gravação finalizada.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(audio_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return audio_path

def main():
    while True:
        # Gera o nome do arquivo
        nome_arquivo = f"audio_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        # Grava o áudio do microfone
        audio_path = gravar_audio(nome_arquivo)

        # Faz a interpretação usando todos os interpretadores
        texto_speech_recognition = interpretar_speech_recognition(audio_path)
        texto_vosk = interpretar_vosk(audio_path)
        texto_whisper = interpretar_whisper(audio_path)

        # Salva os resultados no banco, caso algum texto tenha sido reconhecido
        if texto_speech_recognition:
            salvar_evento(texto_speech_recognition, "speech_recognition")

        if texto_vosk:
            salvar_evento(texto_vosk, "vosk")

        if texto_whisper:
            salvar_evento(texto_whisper, "whisper")

        # Salva o áudio no banco
        salvar_audio_no_banco(nome_arquivo)

        print(f"Áudio '{nome_arquivo}' interpretado e salvo com sucesso.")

if __name__ == "__main__":
    main()
