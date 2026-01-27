import wave
import sys
import pyaudio

if __name__ == '__main__':
    p = pyaudio.PyAudio()

    # TODO: create a script to gather wake word data and non wake word data.
    # Then train a ML model (openwakeword maybe) to detect this wake word