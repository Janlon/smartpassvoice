import speech_recognition as sr

def capturar_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🔊 Ouvindo...")
        audio = r.listen(source)

    try:
        texto = r.recognize_google(audio, language="pt-BR")
        print(f"📝 Texto reconhecido: {texto}")
        return texto
    except sr.UnknownValueError:
        print("❌ Não entendi o que foi dito.")
        return None
    except sr.RequestError as e:
        print(f"⚠️ Erro ao solicitar resultados: {e}")
        return None
