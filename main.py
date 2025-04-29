import datetime
import os
import pyaudio
import wave
import speech_recognition as sr
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

def interpretar_audio_com_speech_recognition(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        print("Reconhecendo áudio...")
        audio_data = recognizer.record(source)
        
        try:
            # Usando o Google Speech Recognition API
            texto = recognizer.recognize_google(audio_data, language="pt-BR")
            print("Texto reconhecido: " + texto)
            return texto
        except sr.UnknownValueError:
            print("Google Speech Recognition não conseguiu entender o áudio")
            return None
        except sr.RequestError as e:
            print(f"Não foi possível conectar ao serviço Google Speech Recognition; {e}")
            return None

def main():
    while True:
        # Gera o nome do arquivo
        nome_arquivo = f"audio_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        # Grava o áudio do microfone
        audio_path = gravar_audio(nome_arquivo)

        # Interpreta o áudio usando o speech_recognition
        texto = interpretar_audio_com_speech_recognition(audio_path)

        # Se o texto foi reconhecido, salva no banco
        if texto:
            salvar_evento(texto, "speech_recognition")
            salvar_audio_no_banco(nome_arquivo)

        print(f"Áudio '{nome_arquivo}' interpretado e salvo com sucesso.")

if __name__ == "__main__":
    main()
