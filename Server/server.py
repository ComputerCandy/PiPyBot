DEBUG = True #Are we Debugging the code?
############################################
#                Import Required Library    #
############################################
if not DEBUG:
    import RPi.GPIO as GPIO 
import socket #Import Socket for later use
import time as timer #Import time as Timer for Timing

############################################
#               Define Variables           #
############################################



true = True #Define true = True for C# like booleans
false = False #Define false = False for C# like booleans



FW = False #Is FW down?
BK = False #Is BK down?
LT = False #Is LT down?
RT = False #Is RT down?
LC = False #Is LC down?
RC = False #Is RC down?
LR = False #Is LR down?
RR = False #Is RR down?
SU = False #Is SU down?
SD = False #Is SD down?
CS = False #Is CS down?
ES = False #Is ES down?

#PI CODE
#Speed for Bot
SS = 0 #Start @ 0 change on SU And SD
# Set to Stop
SSL = 0
SSR = 0
# Encoder Counters
LET = 0                        # Left Encoder Temp
LEC = 0                        # Left Motor Counter
RET = 0                        # RIght Encoder Temp
REC = 0                        # Right Motor Counter
############################################
#               Socket Setup               #
############################################

IP = '127.0.0.1' #What is the HOST/CLIENT IP?
BUFFER_SIZE = 1024  #What is the max size for the packets? (BITS)
s = socket.socket() #Setup the socket
s.bind((IP,45949)) #Bind the Socket to listen on port 45949
s.listen(1) #Listen for a connection
s.settimeout(0.01)#Set Timeout so we dont wait for each packet
print "Time Out:", s.gettimeout() #DEBUG DATA
IPC=0 #How Many Connections have been made?

############################################
#               Code For Pi Only           #
############################################
if not DEBUG:
    GPIO.setmode(GPIO.BCM)    #set up GPIO using BCM numbering
    #ENCODER MAPPING
    GPIO.setup(2, GPIO.IN, GPIO.PUD_UP)
    LEN = 2
    GPIO.setup(3, GPIO.IN, GPIO.PUD_UP)
    REN = 3
    #MOTOR SETUP
    # Left Motor Control
    GPIO.setup(18, GPIO.OUT)        # PWM Speed Control Left
    pi.set_PWM_range(18, 100)          # Percentage On
    pi.hardware_PWM(18, 2000, 0)     # 2000Hz 
    LMP = 18                    # L1                (1) (L1)
    GPIO.setup(24, GPIO.OUT, initial=1)    # Direction
    LMD = 24                    # L2                (2) (L2)
    GPIO.setup(25, GPIO.OUT, initial=0)    # Enable (Break)
    LME = 25                    # EnA                (3) (EnA)
    # Right Motor Control
    GPIO.setup(8, GPIO.OUT, initial=0)        # Enable (Break)
    RME = 8                    # EnB                (4) (EnB)
    GPIO.setup(7, GPIO.OUT, initial=1)        # Direction
    RMD = 7                    # L4                (5) (L4)
    GPIO.setup(12, GPIO.OUT, initial=0)    # PWM Speed Control Right
    pi.set_PWM_range(12, 100)          # Percentage On
    pi.hardware_PWM(12, 2000, 0)     # 2000Hz 
    RMP = 12                    # L3                (6) (L3)
############################################
#               Define Functions           #
############################################
cmt = lambda: int(round(timer.time() * 1000)) #Get Millis for Timing
def setPinStatus(pin,state):
    if not DEBUG:
        GPIO.output(pin,state)
    else:
        print "PIN STATUS- Pin: ",pin," State: ",state
def getPinStatus(pin):
    if not DEBUG:
	    return GPIO.input(LMD)
    return False
#What do we do on Key Press?
def FWF():                        # Staight Forward Movement
    SSL = SS
    setPinStatus(LMD,True)
    SSR = SS
    setPinStatus(RMD,True)
    setPinStatus(LME,True)
    setPinStatus(RME,True)
    
def BKF():                        # Staight Backwards Movement
    SSL = SS
    setPinStatus(LMD,False)
    SSP = SS
    setPinStatus(RMD,False)
    setPinStatus(LME,True)
    setPinStatus(RME,True)

def LCF():                        # Left Curve
    if SS < 51 :
        SSL = SS
        SSR = SS * 2
    if SS > 51 :
        SSL = SS / 2
        SSR = SS
    setPinStatus(LME,True)
    setPinStatus(RME,True)

def RCF():                        # Right Curve
    if SS < 51 :
        SSR = SS
        SSL = SS * 2
    if SS > 51 :
        SSR = SS / 2
        SSL = SS
    setPinStatus(LME,True)
    setPinStatus(RME,True)

def LTF():                        # Left Turn
    if SSR >= 51:
        SSR = SSR / 2
        SSL = 0
        
    if SSR <= 50:
        SSL = 0
    setPinStatus(LME,True)
    setPinStatus(RME,True)

def RTF():                        # Right Turn
    if SSL >= 51:
        SSL = SSL / 2
        SSR = 0
        
    if SSL <= 50:
        SSR = 0    
    setPinStatus(LME,True)
    setPinStatus(RME,True)
        
def LRF():                        # Left Rotate
    SSL = 0
    SSR = 0
    setPinStatus(LMD,not getPinStatus(LMD))
    SSL = SS / 2
    SSR = SSL
    setPinStatus(LME,True)
    setPinStatus(RME,True)
    
def RRF():                        # Right Rotate    
    SSL = 0
    SSR = 0
    setPinStatus(RMD,not getPinStatus(RMD))
    SSR = SS / 2
    SSL = SSR
    setPinStatus(LME,True)
    setPinStatus(RME,True)
        
def CSF():                        # Coast Stop
    SSL = 0
    SSR = 0
    setPinStatus(LME,False)
    setPinStatus(RME,False)
        
def SUF():                        # Speed Up
    SSL = SSL + 2
    SSR = SSR + 2
    SS = SS + 2
    setPinStatus(LME,True)
    setPinStatus(RME,True)
        
def SDF():                        # Speed Down
    SSL = SSL - 2
    SSR = SSR - 2
    SS = SS - 2
    setPinStatus(LME,True)
    setPinStatus(RME,True)


def motorRun(dta): #Socket Data Handler
     global FW #Prepare FW for writing to
     global BK #Prepare BK for writing to
     global LT #Prepare LT for writing to
     global LC #Prepare LC for writing to
     global LR #Prepare LR for writing to
     global RT #Prepare RT for writing to
     global RC #Prepare RC for writing to
     global RR #Prepare RR for writing to
     global SU #Prepare SU for writing to
     global SD #Prepare SD for writing to
     global ES #Prepare ES for writing to
     global CS #Prepare CS for writing to
     if dta == "FW": #IF the key is FW
         FW = True #Set FW to True
     if dta == "BK": #IF the key is BK
         BK = True #Set BK to True
     if dta == "LT": #IF the key is LT
         LT = True #Set LT to True
     if dta == "LC": #IF the key is LC
         LC = True #Set LC to True
     if dta == "LR": #IF the key is LR
         LR = True #Set LR to True
     if dta == "RT": #IF the key is RT
         RT = True #Set RT to True 
     if dta == "RC": #IF the key is RC
         RC = True #Set RC to True
     if dta == "RR": #IF the key is RR
         RR = True #Set RR to True
     if dta == "SU": #IF the key is SU
         SU = True #Set SU to True
     if dta == "SD": #IF the key is SD
         SD = True #Set SD to True
     if dta == "ES": #IF the key is ES
        ES = True #Set ES to True
     if dta == "CS": #IF the key is CS
        CS = True #Set CS to True
     if dta == "KEYUP": #Has a key been let go?
         FW = False #If so set all values to False
         BK = False
         LT = False
         RT = False
         LC = False
         RC = False
         LR = False
         RR = False
         SU = False
         SD = False
         CS = False
         ES = False
def motorUpdate():
      
    if FW == True:
        FWF()
    if BK == True:
         BKF()
    if LT == True:
        LTF()
    if LC == True:
        LCF()
    if LR == True:
        LRF()
    if RT == True:
        RTF()
    if RC == True:
        RCF()
    if RR == True:
        RRF()
    if SU == True:
        SUF()
    if SD == True:
        SDF()
    if CS == True:
        CSF()
    if ES == True:
        ESF()

def applySpeeds():
        if LEC > SSL:
            LMP = LMP - 2
        if LEC < SSL:
            LMP = LMP + 2
        if REC > SSR:
            RMP = RMP - 2
        if REC < SSR:
            RMP = RMP + 2            

TimerA = cmt()
while 1:
    applySpeeds()
    data = None
    if TimerA + 100 < cmt():
        motorUpdate()
        TimerA = cmt()
       # print "TimerA Trigger"
    #print TimerA,"|",TimerA+100,"|",cmt()
    try:
        conn, addr = s.accept()
        data = conn.recv(BUFFER_SIZE)
    except socket.error:
        #print "socket error"
        cmt()

    if data:
        if (data == "STOP"): break
        if(data == "RUPi"):
            conn.send("Yes")
            IPC = IPC + 1
        if(data == "IPC"):
            conn.send(str(IPC))
        if data: 
            print data
            print 'Packet sent from:', addr[0]
            motorRun(data)
GPIO.cleanup()