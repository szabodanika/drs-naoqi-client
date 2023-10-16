from naoqi import qi
import logging

class SpeechSynthesisClient:
    
    def __init__(self, robot_ip, robot_port, audio_callback):
        self.robot_ip = robot_ip
        self.robot_port = str(robot_port)
        self.audio_callback = audio_callback
        
    def synthesiseSpeech(self, text):
        session = qi.Session()
        try:
            session.connect("tcp://{}:{}".format(self.robot_ip, self.robot_port))
            tts = session.service("ALTextToSpeech")
            tts.say(text)
        except:
            logging.error("session.connect failed.")
        finally:
            session.close()
        
        # no need for this now since we are using built in audio synthesiser
        # self.audio_callback("add_audio_file_here")