import pygame
import socket
import requests
import pickle
import check2
s = socket.socket()         
port = 12348
print ("Socket successfully created")


playerid=0
connex=0
pygame.init()
screen = pygame.display.set_mode((700,700))
font = pygame.font.SysFont("comicsansms", 72)
font = pygame.font.Font(None, 75)
done=0
server=0
sendobj=0
while not done:
  
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mosx,mosy=event.pos
            #if()
            if(mosx>0 and mosy>0 and mosx<340 and mosy<400):
                s.bind(('', port))        
                print ("socket binded to %s" %(port))
                s.listen(5)     
                print ("socket is listening")
                connex, addr = s.accept()
                server=1
                sendobj=connex
                playerid=1
                done=1
            if(mosx>370 and mosy>300 and mosx<(370+340) and mosy<400):
                addrs=input("Enter address:")
                s.connect((addrs, port))
                sendobj=s
                playerid=2

                done=1
    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(0,0, 700, 700))        

    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,300, 340, 100))
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(370,300, 340, 100))
    text = font.render("Start Game", True, (255,255,255))
    screen.blit(text,(175 - text.get_width()//2 , +350 - text.get_height() // 2))
    
    text = font.render("Connect", True, (255,255,255))
    screen.blit(text,(350+175 - text.get_width()//2 , 350 - text.get_height() // 2))
    text = font.render("Connect 4", True, (255,0,0))
    screen.blit(text,(350 - text.get_width()//2 , 175 - text.get_height() // 2))
    pygame.display.flip()

#Connect or start game option#

#addrs=input("Enter address:")
#s.connect((addrs, port))










done = False
gamemat=[[0 for i in range(6)] for i in range(7)]
print(gamemat)
red=(255,0,0)
yellow=(255,255,0)
grey=(0,0,0)
playernum=1

font = pygame.font.SysFont("comicsansms", 72)
font = pygame.font.Font(None, 75)
score1=0
score2=0
fill=3
def win(col,row,a,b):
    if(not a==0):
        print("Player "+str(a) + "wins!!!!")
        gamemat=[[0 for i in range(6)] for i in range(7)]
        b.send(pickle.dumps(str(col)+","+str(row)+", won"))

    if(0):
        text = font.render("Player "+str(a) + " wins!!!!", True, (255,255,255))
        screen.blit(text,(350 - text.get_width()//2 , 325 - text.get_height() // 2))
        pygame.display.flip()

        
    
def changeplayer(gamemat,player):
    #senddata(gamemat)
    if(player==1):
        return 2
    if(player==2):
        return 1
    
def flasherror(string1):
    #font = pygame.font.SysFont("comicsansms", 72)
    #font = pygame.font.Font(None, 75)
    #text = font.render(string1, True, (100, 100, 100))

    #screen.blit(text, (400, 400))
    #pygame.time.wait(1000)
    print(string1)
    text = font.render(""+str(string1), True, (255,255,255))
    screen.blit(text,(350 - text.get_width()//2 , 325 - text.get_height() // 2))    
    pygame.display.flip()
    pygame.time.wait(3000)


    #pygame.display.flip()

    
def colorcirc(mat):
    color=grey
    fill=0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if(mat[i][j]==0):
                fill=0
                color=grey
            if(mat[i][j]==1):
                fill=0
                color=red
            if(mat[i][j]==2):
                fill=0
                color=yellow
                
            pygame.draw.circle(screen, color, (100*i+50,100*j+50),30,fill)#10)

text = font.render("Player 1:"+str(score1)+"  Player 2:"+str(score2), True, (0, 0, 0))
winflag=0
while not done:
    
    if (playerid==playernum):
        pass
    else:
        gamematx=pickle.loads(sendobj.recv(1024))
        if(not "won" in gamematx):
            gamemat=gamematx
        if("won" in gamematx):
            lisx2=gamematx.split(",")
            gamemat[int(lisx2[0])][int(lisx2[1])]=playernum
            if(playerid==1):
                score2=score2+1
            else:
                score1=score1+1
            print("You lose! Loser huh")
            winflag=2
            colorcirc(gamemat)
            flasherror("You lose!")
            
            gamemat=[[0 for i in range(6)] for i in range(7)]
        #print("Not your turn")
        #sendobj.flush()
        playernum=changeplayer(gamemat,playernum)
        continue
        #colorcirc()
    '''
    data = (s.recv(1024))
    if(data=="won"):
        if(playernum==1):
            score1=score1+1
        if(playernum==2):
            score2=score2+1
    else
    '''    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            posmouse=event.pos
            if(playerid==playernum):
                if(posmouse[0]<700 and posmouse[1]<600):
                    rownum=int(posmouse[1]/100)
                    colnum=int(posmouse[0]/100)
                    rowiterator=5
                    while(rowiterator>=0):
                        if(gamemat[colnum][rowiterator])==0:
                            gamemat[colnum][rowiterator]=playernum
                            #checkval1=check.func(colnum,rowiterator,gamemat,playernum)
                            checkval1=check2.func(gamemat)
                            win(colnum,rowiterator,checkval1,sendobj)
                            playernum=changeplayer(gamemat,playernum)
                            print("sent")
                            if(checkval1==0):
                                sendobj.send(pickle.dumps(gamemat))
                            else:
                                colorcirc(gamemat)
                                flasherror("You win!!!")
                                winflag=1
                                if(checkval1==1):
                                    score1=score1+1
                                    
                                if(checkval1==2):
                                    score2=score2+1
                                gamemat=[[0 for i in range(6)] for i in range(7)]

                            break
                        rowiterator=rowiterator-1
                    if(rowiterator==-1):
                        flasherror("Column Filled!!!")#"This column is filled")
            else:
                flasherror("Wait for your turn")
                continue
             
                #entire matrix filled exception
                #gamemat[][]=playernum
            
        if event.type == pygame.QUIT:
            done = True
        #print(gamemat)
        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(0,0, 700, 700))
        colorcirc(gamemat)
        pygame.draw.rect(screen, (140, 140,140), pygame.Rect(0,600, 700, 100))
        if(playernum==1):
            text = font.render("Player 1: "+str(score1), True, (255,255,0))#+"  Player 2: "+str(score2), True, (0, 0, 0))
            screen.blit(text,(350//2 - text.get_width()//2 , 600+50 - text.get_height() // 2))
            text = font.render("Player 2: "+str(score2), True, (0, 0, 0))#+"  Player 2: "+str(score2), True, (0, 0, 0))
            screen.blit(text,(350+350//2 - text.get_width()//2 , 600+50 - text.get_height() // 2))
        if(playernum==2):
            text = font.render("Player 1: "+str(score1), True, (0, 0,0))#+"  Player 2: "+str(score2), True, (0, 0, 0))
            screen.blit(text,(350//2 - text.get_width()//2 , 600+50 - text.get_height() // 2))
            text = font.render("Player 2: "+str(score2), True, ( 255,255,0))#+"  Player 2: "+str(score2), True, (0, 0, 0))
            screen.blit(text,(350+350//2 - text.get_width()//2 , 600+50 - text.get_height() // 2))
        
        pygame.display.flip()
'''
        if(winflag!=0):
            
            if(winflag==2):
                flasherror("You lose!")
            if(winflag==1):
                flasherror("You win!!!")
            winflag=0
'''             
s.close()