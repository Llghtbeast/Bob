import wave
import sys
import pyaudio
import argparse

def play_audio(file, is_ww):
    # TODO: write code to play the audio file

    path = f'data/1/{file}' if is_ww else f'data/0/{file}'

    with wave.open(path, mode='wb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
        )

def record_audio(file, length, is_ww, device_id=8, chunk=4096, sample_format=pyaudio.paInt16, fs=16000):
    """
    Save wake word data and non wake word data.
    """
    # TODO: modify code to use USB Microphone device (do not use hard coded id)
    p = pyaudio.PyAudio()

    info = p.get_host_api_info_by_index(0)
    numdevices = int(info.get('deviceCount') or 0)
    for i in range(0, numdevices):
        if int(p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') or 0) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    
    channels = int(p.get_device_info_by_index(device_id).get('maxInputChannels', 1))

    stream = p.open(
        input_device_index=device_id,
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True,
    )

    print(f'Recording audio for {length} seconds')
    frames = []
    for _ in range(0, int(fs/chunk * length)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    path = f'data/1/{file}' if is_ww else f'data/0/{file}'
    print(f'Saving audio recording to {path}')
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))

    p.terminate()



if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(
        prog='Play or Record audio',
        description='The program allows the user to play or record audio',
    )

    parser.add_argument('process')
    parser.add_argument('file')
    parser.add_argument('-l', '--length', default=5)    # Length of recording in seconds
    parser.add_argument('--ww', action='store_true')    # Is the recording that of a wake word

    args = parser.parse_args()
    
    if args.process == 'record':
        record_audio(args.file, int(args.length), args.ww)
    elif args.process == 'play':
        play_audio(args.file, args.ww)

    # TODO: train a ML model (openwakeword maybe) to detect this wake word
