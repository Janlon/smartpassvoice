import speech_recognition as sr

def interpretar_speech_recognition(audio_path):
    # Inicializa o reconhecedor de fala
    recognizer = sr.Recognizer()

    # Carrega o arquivo de áudio
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)  # Lê o áudio do arquivo

    try:
        # Reconhece o áudio utilizando o Google Web Speech API
        texto = recognizer.recognize_google(audio, language="pt-BR")
        return texto
    except sr.UnknownValueError:
        print("Google Speech Recognition não conseguiu entender o áudio")
        return None
    except sr.RequestError as e:
        print(f"Erro na requisição ao serviço de reconhecimento de fala: {e}")
        return None
