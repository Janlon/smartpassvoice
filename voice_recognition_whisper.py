import whisper

def interpretar_whisper(audio_path):
    # Carregar o modelo Whisper
    model = whisper.load_model("base")  # O modelo "base" é uma boa opção para começar, mas você pode escolher outros modelos como "small", "medium", "large"

    # Transcrever o áudio
    result = model.transcribe(audio_path)

    # Retornar o texto reconhecido
    return result['text']
