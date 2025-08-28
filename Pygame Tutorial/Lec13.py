#mixer.music.load
''' loads music file object and prepares it for playback '''

# .unload
''' unloads the currently loaded up music if it is not being used (helps to save on resources)'''

# .play
# .rewind
# .stop
# .pause
# .unpause
# .fadeout
''' takes time argument for which music has to fade out'''
# .set_volume
# .get_volume
# .getbusy 
''' returns True if music is playing'''

# .get_pos
''' returns for how long music has been playing'''

# .queue()
''' to enqueue a song to the current one'''

from pygame import mixer
mixer.init()

mixer.music.load('Pygame Tutorial\Images\piano.wav')
mixer.music.play()
# mixer.music.set_pos(71)

while True:
    inp = input(' ')
    if inp == 'P':
        mixer.music.pause()
        print(mixer.music.get_busy())
    elif inp == 'U':
        mixer.music.unpause()
        print(mixer.music.get_busy())
    elif inp == 'S':
        mixer.music.stop()
        print(mixer.music.get_busy())
        break
    elif inp == 'R':
        mixer.music.rewind()
        print(mixer.music.get_busy())