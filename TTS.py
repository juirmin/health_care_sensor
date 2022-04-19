from gtts import gTTS 
from pydub import AudioSegment
from pydub.playback import play

def playsound(mytext):
    language = 'zh-tw'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("output.mp3") 
    music = AudioSegment.from_mp3('./output.mp3')
    play(music)

if __name__ == '__main__':
    playsound('請開始良測')