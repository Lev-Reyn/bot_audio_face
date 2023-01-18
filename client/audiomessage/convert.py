import os


def audio2wav(audio_path, output_name):
    """
    Convert any audio format to wav format, need to install ffmpeeg
    """
    output_name = output_name + '.wav'
    os.system("ffmpeg -i " + audio_path + " -ac 1 -ar 16000" + " " + output_name)


if __name__ == '__main__':
    output_file_name = 'testim'
    video_path = '../../voices/AwACAgIAAxkBAAIZPGPF5Ndzo2f98yW4rtpwRPJ4-kCCAAK0JQACtmMwSoQJFVXObmciLQQ.ogg'
    audio2wav(video_path, output_file_name)
    print('ok')

