import socket
import sys,select
import threading
from termios import tcflush, TCIFLUSH

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 1233
HEADER_LENGTH = 10

#printing rules of the quiz
print('\n---------------RULES---------------')
print('>for giving answer press buzzer')
print('>you have 10 SECONDS to press buzzer')
print('>>----press ENTER for buzzer----<<')
print('> for correct answer 1 point will be rewared')
print('> for wrong answer 0.5 point will be deducted')
print('>if you dont press buzzer no scores will be rewared or deducted')
print('> SCORE 5 POINTS TO WIN \n')
print('Waiting for connection\n')

print('\n---------------NOTE---------------')
print('>>----press ENTER for buzzer----<<\n')
#connecting to the host
try:
    client.connect((host, port))
except socket.error as e:
    print(str(e))

# used to stop taking buzzer if some other client have pressed it
stopIT=False

#send user name to server
def send_username():
    #taking user name
    tcflush(sys.stdin, TCIFLUSH)
    my_username=input('username->')
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    try:
        client.send(username_header + username)
    except:
        print('some problem with server')
        sys.exit()

#function for pressing buzzer
def if_buzzer_pressed():
    global stopIT
    try:
        pressed=client.recv(7).decode('utf-8')
        if(pressed == 'pressed'):
            stopIT=True
    except:
        print('some problem with server')
        sys.exit()

def press_buzzer():
    # removing input buffers
    tcflush(sys.stdin, TCIFLUSH)
    global stopIT
    stopIT = False
    time=0
    #10 seconds for pressing buzzer
    while(time<10):
        i,o,e = select.select([sys.stdin],[],[],0.1)
        #if pressed before 10 sec take input
        if i:
            buzzer=sys.stdin.readline().strip()
        else:
            buzzer ='0'

        #if client pressed buzzer go out of the loop
        if(buzzer != '0'):
            break
        #if times up
        if(time>=10):
            break
        # if other client pressed buzzer go out of the loop
        if(stopIT):
            break

        time=time+0.1

    #else times up
    if(time==10):
        print("---times up!---")
        buzzer="0"

    # if user just pressed enter making it random char so easy to send
    if buzzer== "":
        buzzer='a'

    #send buzzer
    try:
        ans = buzzer.encode('utf-8')
        ans_header = f"{len(ans):<{HEADER_LENGTH}}".encode('utf-8')
        client.send(ans_header + ans)
    except:
        print('some problem with server')
        sys.exit()
    # flushing output screen
    sys.stdout.flush()

#function for geting and printing question
def get_question():
    print('-'*60)
    try:
        que_header = client.recv(HEADER_LENGTH)
        if len(que_header):
            que_length = int(que_header.decode('utf-8').strip())
            que = client.recv(que_length).decode('utf-8')
            print(que)
    except:
        print('some problem with server')
        sys.exit()
#function for sending answer
def send_answer():
    print('----type answer----')
    # removing input buffers
    tcflush(sys.stdin, TCIFLUSH)
    #10 seconds to type answer
    i,o,e = select.select([sys.stdin],[],[],10)
    if i:
        my_ans=sys.stdin.readline().strip()
    else:
        print("----times up!----")
        my_ans=""

    try:
        ans = my_ans.encode('utf-8')
        ans_header = f"{len(ans):<{HEADER_LENGTH}}".encode('utf-8')
        client.send (ans_header + ans)
    except:
        print('some problem with server')
        sys.exit()
    # flushing output screen
    sys.stdout.flush()

#function for getting and printing score
def get_score():
    print('\n----CURRENT SCORES ARE----')

    try:
        score_header = client.recv(HEADER_LENGTH)
        if len(score_header):
            score_length = int(score_header.decode('utf-8').strip())
            score = client.recv(score_length).decode('utf-8')
            print(score)
    except:
        print('some problem with server')
        sys.exit()

#function for getting and printing winner name
def get_winner():
    try:
        winner_header = client.recv(HEADER_LENGTH)
        if len(winner_header):
            winner_length = int(winner_header.decode('utf-8').strip())
            winner = client.recv(winner_length).decode('utf-8')
            print(winner)
    except:
        print('some problem with server')
        sys.exit()

#function to start game
def start_game():
    print("\n----PLEASE WAIT ----\n")
    while True:
        try:
            #recive signal to take question
            next=client.recv(1).decode('utf-8')
            if(next=='q'):
                #to get and print question
                get_question()
        except:
            print('some problem with server')
            sys.exit()

        try:
            #recive signal to send buzzer
            next=client.recv(1).decode('utf-8')
            #to press buzzer and check if buzer is already pressed
            if(next=='b'):
                t1 = threading.Thread(target=press_buzzer)
                t2 = threading.Thread(target=if_buzzer_pressed)

                # starting thread 1
                t1.start()
                # starting thread 2
                t2.start()

                # wait until thread 1 is completely executed
                t1.join()
                # wait until thread 2 is completely executed
                t2.join()
        except:
            print('some problem with server')
            sys.exit()
        try:
           # recive response of buzzer
            buffer_first = client.recv(1)
            #if response is s then client have pressed buzzer first
            if(buffer_first.decode('utf-8')=='s'):
                send_answer()

            #if response is n then other client have pressed buzzer first
            elif(buffer_first.decode('utf-8')=='n'):
                print('\nwait other player is giving answer')
                #waitng untill other client is answering
                answerGiven = client.recv(2)
                if(answerGiven.decode('utf-8')=='go'):
                    pass

            #if response is p then no one have pressed buzzer
            elif(buffer_first.decode('utf-8')=='p'):
                pass
        except:
            print('some problem with server')
            sys.exit()

        try:
            #recive signal to take scores
            next=client.recv(1).decode('utf-8')
            if(next=='z'):
                #to get and print score
                get_score()
        except:
            print('some problem with server')
            sys.exit()

        try:
            #recive signal to check winner
            next=client.recv(1).decode('utf-8')
            #if signal is w then game is over
            if(next=='w'):
                print('----GAME OVER----')
                get_winner()
                break
            #else continue the game
            else:
                pass
        except:
            print('some problem with server')
            sys.exit()

while True:
    #reciving message for starting the game
    try:
        start_header = client.recv(HEADER_LENGTH)
    except:
        print('some problem with server')
        sys.exit()

    if len(start_header):
        start_length = int(start_header.decode('utf-8').strip())
        try:
            start = client.recv(start_length)
        except:
            print('some problem with server')
            sys.exit()

    if not type(start) == str:
        start=start.decode('utf-8')

    #if message is start then start the game
    if start=="start":
        print('----ENTER your GAMENAME---')
        send_username()
        start_game()
        break
    #else wait for the start message
    else:
        continue

client.close()
