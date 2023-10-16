from threading import Thread
from naoqi import ALModule, ALProxy
from io import StringIO
import time
import logging
import uuid
import traceback
import wave
import numpy
from Queue import Queue

LISTEN_RETRIES = 10

class SoundProcessingModule(ALModule):
    
    init_success = True
    
    def __init__( self, name, robot_ip, robot_port, stop_recognition, audio_callback):
        
        try:
            ALModule.__init__( self, name )
        except Exception as e:
            logging.error(str(e))
            pass
        
        logging.info("SoundProcessingModule connected")
        self.robot_ip = robot_ip
        self.robot_port = robot_port
        self.BIND_PYTHON( name , "processRemote")
        try:
            self.ALAudioDevice = ALProxy("ALAudioDevice", self.robot_ip, self.robot_port)
        except RuntimeError:
            logging.error("Can't find service: ALAudioDevice. Are you connected to a physical robot?")
            self.init_success = False
        self.framesCount=0
        self.audio_callback = audio_callback
        self.count = LISTEN_RETRIES
        self.recordingInProgress = False
        self.stopRecognition = stop_recognition
        self.uuid = uuid.uuid4()
        self.previous_sound_data = None
        
    def startProcessing(self):
        # Don't start if not initialised, just gonna get a bunch of errors. But act like everything is cool and hip
        if(not self.init_success): return
        
        """init sound processing, set microphone and stream rate"""
        print("startProcessing")
        self.ALAudioDevice.setClientPreferences(self.getName(), 16000, 3, 0)
        self.ALAudioDevice.subscribe(self.getName())
        while not self.stopRecognition.is_set():
            time.sleep(1)
        self.ALAudioDevice.unsubscribe(self.getName())
        
    def processRemote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer):
        self.framesCount = self.framesCount + 1
        sound_data_interlaced = numpy.fromstring(str(inputBuffer), dtype=numpy.int16)
        sound_data = numpy.reshape(sound_data_interlaced, (nbOfChannels, nbOfSamplesByChannel), 'F')
        peak_value = numpy.max(sound_data)    # detect sound
        if peak_value > 14000:
            print("Peak:", peak_value)
            self.count = LISTEN_RETRIES
            if not self.recordingInProgress:
                self.startRecording(self.previous_sound_data)# if there is no sound for a few seconds we end the current recording and start audio processing    if self.count <= 0 and self.recordingInProgress:
            self.stopRecording()# if recording is in progress we save the sound to an in-memory file    if self.recordingInProgress:
            self.count -= 1
            self.previous_data = sound_data
            self.procssingQueue.put(sound_data[0].tostring())
            self.outfile.write(sound_data[0].tostring())
            
    def startRecording(self, previous_sound_data):
        """init an in memory file object and save the last raw sound buffer to it."""
        self.outfile = StringIO.StringIO()
        self.procssingQueue = Queue()
        self.recordingInProgress = True
        if not previous_sound_data is None:
            self.procssingQueue.put(previous_sound_data[0].tostring())
            self.outfile.write(previous_sound_data[0].tostring())

        print("start recording")
        
    def stopRecording(self):
        """saves the recording to memory"""
        print("stopped recording")
        self.previous_sound_data = None
        self.outfile.seek(0)
        try:
            self.audio_callback(self.outfile)
        except:
            traceback.print_exc()    
            self.recordingInProgress = False