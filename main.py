# -*- coding: utf-8 -*-
import youtube_dl
from pydub import AudioSegment
import speech_recognition as sr
import subprocess
from pydub.utils import make_chunks
import shutil
import glob, os, os.path

file = "file.mp3"
dst = "file.wav"

print("Start")

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'file.mp3',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['LINK_TO_YT_VIDEO'])

print("Downloaded")

subprocess.call(['ffmpeg', '-i', file,dst])

print("Converted")

myaudio = AudioSegment.from_file("file.wav" , "wav")
chunk_length_ms = 50000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec

# #Export all of the individual chunks as wav files
#
os.mkdir("chunked")
for i, chunk in enumerate(chunks):
    chunk_name = "./chunked/chunk{0}.wav".format(i)
    print("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")
    r = sr.Recognizer()
    with sr.AudioFile(chunk_name) as source:
        audio = r.record(source)
    try:
        print("Text to speeching")
        s = r.recognize_google(audio,language="pl-PL")
        print("Text: "+s)
        with open('result.txt', 'a') as fh:
            fh.write(s.encode('utf-8'))
    except Exception as e:
        print("Exception!!: \n")
        print(e)

filelist = glob.glob(os.path.join('chunked', "*.wav"))
for f in filelist:
    os.remove(f)
os.remove(file)
os.remove(dst)
os.rmdir("chunked")

print("speech to text ready")
print("removed chunked files")
print("done :)")
