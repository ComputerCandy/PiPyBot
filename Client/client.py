import pygame
import time as timer
import socket
import sys
#INITILIZE WINDOW AND CONSOLE
pygame.init()

for x in range(0, 20):
    print " "

print(" ____                      _          ____           \n|  _ \ ___ _ __ ___   ___ | |_ ___   / ___|__ _ _ __ \n| |_) / _ \ '_ ` _ \ / _ \| __/ _ \ | |   / _` | '__|\n|  _ <  __/ | | | | | (_) | ||  __/ | |__| (_| | |   \n|_| \_\___|_| |_| |_|\___/ \__\___|  \____\__,_|_|   \n")
IMGDIR = "CarIMG/"

bootstrapArgs = sys.argv
#Define Keys for Input	
FW = pygame.K_w
BK = pygame.K_s
LT = pygame.K_a
LC = pygame.K_c
LR = pygame.K_b
RT = pygame.K_d
RC = pygame.K_v
RR = pygame.K_n
SU = pygame.K_UP
SD = pygame.K_DOWN
ES = pygame.K_m
CS = pygame.K_RETURN
#DEFINE VARIABLES FOR WINDOW	

display_width = 400
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height), pygame.HWSURFACE)
true = True
false = False




black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
IPC = 0
IP = bootstrapArgs[1]
#IP = "127.0.0.1"
#IP = raw_input('What is the Raspberry Pi IP you are trying to connect to?')
#DEFINE FUNCTIONS
def isIPv4(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

def start():
    
    
    print "Logging into Pi, At IP: " + IP
    if (isIPv4(IP)):
        BUFFER_SIZE = 1024
        MESSAGE = "RUPi"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IP, 45949))
            s.send(MESSAGE)
            
            data = s.recv(BUFFER_SIZE)
        except socket.error:
            print "Failed Connecting to Pi. Please restart this script and launch the script on your Pi"
            pygame.quit()
            quit()
        if(data != "Yes"):
            print "Failed Connecting to Pi. Please restart this script and enter a valid IP address"
            s.close()
            pygame.quit()
            quit()

    else:
        print "Failed. Please restart this script and enter a valid IP address"
        pygame.quit()
        quit()
    pygame.display.set_caption('Raspberry Pi Controler - Listening - IP: '+IP)
    s.close()



def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def showText(text,size,line,x,y,useFormula):
    largeText = pygame.font.SysFont('Arial',size)
    TextSurf, TextRect = text_objects(text, largeText)
    if (useFormula == 1):
        TextRect.center = ((display_width-(display_width-50)+x),(display_height-(display_height-50)+(line*size*2))+y)
    else:
        TextRect.center = (x,y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def updateScreen():
    gameDisplay.fill(white)
    showText("Key Mapping",25,0,10,10,true)
    showText("Forward : W",14,1,10,10,true)
    showText("Back : S",14,2,10,10,true)
    showText("Turn Left : A",14,3,10,10,true)
    showText("Curve Left : C",14,4,10,10,true)
    showText("Rotate Left : B",14,5,10,10,true)
    showText("Turn Right : D",14,6,10,10,true)
    showText("Curve Right : V",14,7,10,10,true)
    showText("Rotate Right : N",14,8,10,10,true)
    showText("EStop : M",14,9,10,10,true)
    showText("Slow Stop : RETURN",14,10,10,10,true)
    showText("Speed Up : UP",14,11,10,10,true)
    showText("Speed Down : DOWN",14,12,10,10,true)    
    pygame.display.update() 
def sendInstruction(ltrsSend):
    doImage = true
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, 45949))
    s.send(ltrsSend)
    s.close()
	
    #if(ltrsSend == "KEYUP"):
	#   doImage = false
    #elif(ltrsSend == "STOP"):
	#   doImage = false
    #elif(ltrsSend == "SU"):
	#   doImage = false
    #elif(ltrsSend == "SD"):
	#   doImage = false
    #elif(ltrsSend == "IPC"):
	#    doImage = false
    #if(doImage == true):
    #    gameDisplay.blit(images[ltrsSend],(0,0))
		
def testIPCNew():
    sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sa.connect((IP, 45949))
    sendInstruction("IPC")
    IPC = int(sa.recv(1045))
start()
updateScreen()
while not crashed:
	# render text
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        ############################
        if event.type == pygame.KEYDOWN:
            if event.key == FW:
                print "Forward"
                sendInstruction("FW")
                
            elif event.key == BK:
                print "Back"
                sendInstruction("BK")
                
            elif event.key == LT:
                print "Left Turn"
                sendInstruction("LT")
                
            elif event.key == RT:
                print "Right Turn"
                sendInstruction("RT")
                
            elif event.key == SU:
                print "Speed Up"
                sendInstruction("SU")
            elif event.key == SD:
                print "Speed Down"
                sendInstruction("SD")
            elif event.key == ES:
                print "EStop"
                sendInstruction("ES")
            elif event.key == CS:
                print "Slow Stop"
                sendInstruction("CS")
                
            elif event.key == LC:
                print "Left Curve"
                sendInstruction("LC")
                
            elif event.key == LR:
                print "Left Rotate"
                sendInstruction("LR")
                
            elif event.key == RC:
                print "Right Curve"
                sendInstruction("RC")
                
            elif event.key == RR:
                print "Right Rotate"
                sendInstruction("RR")
            #testIPCNew()
            updateScreen()	
        if event.type == pygame.KEYUP:
            #testIPCNew()
            updateScreen()	
            sendInstruction("KEYUP")
    ######################
    ##
    
   ##         
    
    clock.tick(120)
    
sendInstruction("STOP")
pygame.quit()
quit()
