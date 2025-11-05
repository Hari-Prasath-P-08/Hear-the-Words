import whisper

model = whisper.load_model("base") #you can use "small", "medium", "large" for specific needs.
result = model.transcribe("separated_vocals/Vengamavan_vocals.wav", language = "en")
print(result["text"])