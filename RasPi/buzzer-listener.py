__author__ = 'r3cursive'
import serial
import os
import random
import mp3play
import time

debugMode = False
numBuzzers = 10
players = dict()
# you have to set timeout to none otherwise reading is a non-blocking operation
s = serial.Serial(port=4,timeout=None)
buzzerSoundDir = 'buzzer-sounds/'
#the arduino module sends 3 characters, ex 3\r\n
bufSize = 3


def getSerialInput():
    return int(s.read(bufSize).rstrip('\r\n'))


def fakeBuzzerSetup():
    global debugMode
    print "Debug /// Fake buzzer setup in place"
    for i in range(0,numBuzzers):
        players[i] = i
    debugMode = True

def addPlayer(buzzer):
    # if a player buzzes in again, alert, and make sure we want to overwrite
    if buzzer in players.keys():
        print '%s is already registered to buzzer %d!' % (players[buzzer], buzzer)

        # there's actually input here
        readIn = raw_input('Press Enter to ignore, or type a new player name!: ')
        if readIn == '':
            return
    else:
        print 'Registration for buzzer %d' % buzzer
        readIn = raw_input('Type a player name: ')
    if readIn != '':
        players[buzzer] = readIn
        print 'OK! Player %s is now registered to buzzer %d' % (players[buzzer], buzzer)


def buzzerSetup():
    print '*'*20
    print '*'*20
    print 'Beginning buzzer setup'
    print '*'*20
    print '*'*20
    activatedBuzzers = len(players.keys())
    #flush the readbuffer before we start
    s.flushInput()
    while numBuzzers > activatedBuzzers:
        s.flushInput()
        readBuf = getSerialInput()
        addPlayer(readBuf)
        activatedBuzzers = len(players.keys())
        #import ipdb; ipdb.set_trace()

def playRandomBuzzserSound():
    mp3file = random.choice(os.listdir(buzzerSoundDir))
    mp3file = buzzerSoundDir + '/' + mp3file
    mp3 = mp3play.load(mp3file)
    #import ipdb; ipdb.set_trace()
    mp3.play(3)
    time.sleep(3)

def gameTime():
    # main game buzzer fucntion, the timeout is handled on the arduino side, so this should only be playing
    # sounds and displaying who buzzed in.
    while True:
        print "*"*random.randint(1, 40)
        print
        s.flushInput()
        contestant = getSerialInput()
        print "Player %s has buzzed in on %d" % (players[contestant], contestant)
        print
        print "*"*random.randint(1, 40)
        playRandomBuzzserSound()



if __name__ == "__main__":
    fakeBuzzerSetup()
    if not debugMode:
        buzzerSetup()
        print '*'*20
        print '*'*20
        print 'Buzzer setup complete. Game ready in 30 seconds'
        time.sleep(30)
    os.system('cls')
    gameTime()