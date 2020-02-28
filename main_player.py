#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import vlc

# vlc configuration
VlcInstance = vlc.Instance('--aout=alsa')
Player = VlcInstance.media_player_new()
Media = VlcInstance.media_new('/home/pi/music.mp3')
PlayerTimePos = 0
PlayerTimePos = Player.get_position()

# Jingle Player configuration
JingleVlcInstance = vlc.Instance('--aout=alsa')
JinglePlayer = JingleVlcInstance.media_player_new()
JingleMedia = JingleVlcInstance.media_new('/home/pi/Jingle.mp3')
#JingleDuration = 0

def MusicPlayerInit():
    Player.set_media(Media)

def MusicPlayer():
    #Player.set_media(Media)
    JinglePlayer.stop()
    Player.play()
    vlc.libvlc_audio_set_volume(Player, 90)


channel=23
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)


def testisr23(channel):
    if GPIO.input(23) == 0:
       print("23 = 0")
    else:
       print("23 != 0")

def isr23(channel):
    if GPIO.input(23) == 0:
       print("23=0")
    else:
       print("ISR23")
       Player.pause()
       JinglePlayer.set_media(JingleMedia)
       vlc.libvlc_audio_set_volume(JinglePlayer, 90)
       JinglePlayer.play()
       JinglePlaying = set([1])
       JingleTimeLeft = True
       while JingleTimeLeft == True:
          print("ISR23 Jingle Player Timepos", JinglePlayer.get_position())
          JingleTime = JinglePlayer.get_state()
          if JingleTime not in JinglePlaying:
             JingleTimeLeft = False
             print(JingleTime)
          time.sleep(1)
       JingleDuration=JinglePlayer.get_length() / 1000
       time.sleep(JingleDuration)
       vlc.libvlc_audio_set_volume(JinglePlayer, 0)
       JinglePlayer.stop()
       MusicPlayer()

ButtonPress23 = GPIO.add_event_detect(23, GPIO.RISING, callback = isr23, bouncetime = 1000)

MusicPlayerInit()
MusicPlayer()

try:
    while True:
       print("Music Player State: ", Player.get_state())
       #print("Music Player Timepos: ", Player.get_position())
       #print("ButtonPress ", ButtonPress23)
       time.sleep(1)

except KeyboardInterrupt:
   GPIO.cleanup()
   print("\n bye")

