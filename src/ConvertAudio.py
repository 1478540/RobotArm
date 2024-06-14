# 音频格式转换程序
# 利用ffmpeg库，将目标音频转化为设定格式

import ffmpeg


Audio_Format=[48000,1,'s16']


#音频格式转化函数（目前只测试过.wav）
# input_file 是输入音频路径
# output_file 是输出音频路径
# audio_format 是要求的音频格式，以列表的形式存储，依次是：采样率、声道、字节位数格式（默认是48000采样率、单声道、16位字节小端序）
def convert_audio(input_file, output_file,audio_format=Audio_Format):
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, ar=audio_format[0], ac=audio_format[1], sample_fmt=audio_format[2])
            .run(overwrite_output=True)
        )
        print(f"Conversion successful: {input_file} -> {output_file}")
    except ffmpeg.Error as e:
        print(f"Error occurred: {e}")

