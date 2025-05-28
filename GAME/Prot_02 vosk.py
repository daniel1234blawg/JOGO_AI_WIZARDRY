from vosk import Model, KaldiRecognizer
import pyaudio
import json

# Caminho para o modelo em português
MODEL_PATH = "C:\Users\afons\Desktop\model path\vosk-model-pt-fb-v0.1.1-20220516_2113  # Substitua pelo caminho correto do modelo baixado"

# Inicializa o modelo
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Inicializa o microfone
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()

print("Fale algo... (Ctrl+C para sair)")

try:
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            texto = result.get("text", "")
            if texto:
                print(f"Você disse: {texto}")
except KeyboardInterrupt:
    print("\nEncerrando...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()


