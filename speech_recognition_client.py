
class SpeechRecognitionClient:
    
    def __init__(self, utterance_callback):
        
        self.utterance_callback = utterance_callback
        
    def transcribeAudio(self, audioFile):
        
        self.utterance_callback("str")