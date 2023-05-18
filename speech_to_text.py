from pydub import AudioSegment
from os import path
import speech_recognition as sr
import os
import time


def speech_to_text(input_file = "video.mp3"):
    output_file = "video.wav"

    # convert mp3 file to wav file
    sound = AudioSegment.from_mp3(input_file)
    sound.export(output_file, format="wav")
    audio_file = "video.wav"

    r = sr.Recognizer()
    # 打开语音文件
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    # print('文本内容: ',r.recognize_sphinx(audio,language='zh_CN'))  #汉语
    print('文本内容: ', r.recognize_sphinx(audio))

if __name__ == "__main__" :
    speech_to_text()
