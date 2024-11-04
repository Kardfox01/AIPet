import pvporcupine
from pvrecorder import PvRecorder
from speech_recognition import Recognizer, Microphone, UnknownValueError
import sounddevice as sd
import soundfile as sf
from os.path import split, join
from time import sleep


def sit():
    print("сажусь")

def show_face():
    print("подмигиваю")

def move_head():
    print("киваю и машу ушами")

def standup():
    print("встаю")


FILE_DIR = split(__file__)[0]

porcupine = pvporcupine.create(
    access_key    = "F5D+gTgWOZa4x5RRzi2fWSthA0YJWitVObBHWlD+XK5pkJZ4R1L7eg==",
    keyword_paths = [join(FILE_DIR, "hey-mors_en_windows_v3_0_0.ppn")],
)

devices = PvRecorder.get_available_devices()
for i in range(len(devices)):
    print(f"({i}) - {devices[i]}")
device = int(input("Устройство: "))

recorder = PvRecorder(
    device_index = device,
    frame_length = porcupine.frame_length
)

recognizer = Recognizer()

data, fs = sf.read(join(FILE_DIR, "bark.wav"), dtype="float32")

try:
    recorder.start()

    while True:
        keyword_index = porcupine.process(recorder.read())

        if keyword_index == 0:
            print("\nжду команды\n")

            sd.play(data, fs)
            with Microphone(device) as source:
                try:
                    command = recognizer.recognize_google(
                        recognizer.listen(source),
                        language="ru-RU"
                    ).lower()
                except UnknownValueError: continue

            if "сидеть" in command:
                show_face()
                sd.play(data, fs)
                move_head()
                sit()
                sleep(5)
                standup()
            elif "голос" in command:
                sd.play(data, fs)

except KeyboardInterrupt:
    recorder.stop()

finally:
    porcupine.delete()
    recorder.delete()
