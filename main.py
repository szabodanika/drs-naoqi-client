from naoqi import ALBroker
from audo_recorder import SoundProcessingModule
from speech_recognition_client import SpeechRecognitionClient
from conversation_server_client import ConversationServerClient
from speech_synthesis_client import SpeechSynthesisClient
from audio_player import AudioPlayer
import threading
import logging

ROBOT_IP = "daniel.local"
ROBOT_PORT = 9559

CONVERSATION_SERVER_IP = "localhost"
CONVERSATION_SERVER_PORT = 5005

def main():
    pythonBroker = ALBroker("pythonBroker", "0.0.0.0", 9999, ROBOT_IP, ROBOT_PORT)
    
    logging.info("Connected to Pepper Robot")    
    
    # Initialise services from output towards input
    # 1. Start with initialising audio player to play synthesised speech audio
    audio_player = AudioPlayer()
    # 2. Initialise speech synthesiser to synthesise chatbot's text responses
    speech_synthesis_client = SpeechSynthesisClient(
        robot_ip=ROBOT_IP, 
        robot_port=ROBOT_PORT,
        audio_callback=audio_player.playAudio
    )
    
    # 3. Initialise chatbot to respond to the transcribed utterances
    conversation_server_client = ConversationServerClient(
        conversation_server_ip=CONVERSATION_SERVER_IP,
        conversation_server_port=CONVERSATION_SERVER_PORT,
        response_callback=speech_synthesis_client.synthesiseSpeech
    )
    
    conversation_server_client.respondTo("goodbye")
    
    # 4. Initialise speech recogniser to process recorded user audio
    speech_recogniser = SpeechRecognitionClient(
        utterance_callback=conversation_server_client.respondTo
    )
    
    # 6. Initialise and start audio recording service
    sound_recorder = SoundProcessingModule(
        robot_ip=ROBOT_IP, 
        robot_port=ROBOT_PORT,
        name="sound_recorder",
        stop_recognition=threading.Event(), 
        audio_callback=speech_recogniser.transcribeAudio)
    sound_recorder.startProcessing()
    
    pythonBroker.shutdown()
    logging.info("Disconnected from Pepper Robot")

if __name__ == "__main__":
    main()