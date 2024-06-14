# 音频播放程序

import pygame


# 播放音频文件
# audio_path是音频路径（目前只测试过播放.wav）
# volume是音量
def AudioPlay(audio_path,volume=0.9):

	# 初始化pygame
	pygame.mixer.init()
	

	sound = pygame.mixer.Sound(audio_path)
	# 设置第一个文件的音量为100%
	sound.set_volume(volume)

	sound.play()
	
    # 等待音频文件播放完成
	while pygame.mixer.get_busy():
	    pygame.time.delay(100)
	