from lib2to3.refactor import MultiprocessRefactoringTool
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import get_frame_rate
from pydub.utils import get_sample_rate
##pacote para manipular audio

class AudioFading:
    def __init__(self, audiofile):
        self._audiofile = audiofile
        self._audio = AudioSegment.from_file(audiofile)
    

    def fade_in(self, duration=5000):
        self._audio = self._audio.fade_in(duration)
        self._audio.export(self._audiofile[:-4] + '_fade_in.mp3', format='mp3')
