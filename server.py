import socket
import threading
import random
import time

Question_list = [
["Which African nation is famous for chocolate?","Ghana",1],
["What is the name of the biggest rain forest in the world?","Amazon",1],
["How many strings does a violin have?","Four",1],
["Which is the continent with the most number of countries?","Africa",1],
["Which gas is most abundant in the earth’s atmosphere?","Nitrogen",1],
["Which place is known as the roof of the world?","Tibet",1],
["Which festival is called the festival of light?","Diwali",1],
["The largest ‘Democracy’ in the world?","India",1],
["Which is the most spoken language in the world?[options:English,Chinese,French,Urdu]","Chinese",1],
["Which is the most sensitive organ in our body?","Skin",1],
["Which planet is known as the Red Planet?","Mars",1],
["How many months of the year have 31 days?","Seven",1],
["Which is the largest flower in the world?","Rafflesia",1],
["Which continent is known as ‘Dark’ continent?","Africa",1],
["Who is the inventor of electricity?","Benjamin Franklin",1],
["Which is the tallest animal on the earth?","Giraffe",1],
["How many millimetres are there in 1cm?","10",1],
["Which two parts of the body continue to grow for your entire life?[in format X and Y]","Nose and Ears",1],
["Which country is called the land of rising sun?","Japan",1],
["What is the standard taste of the water?","Tasteless",1],
["Which is the largest ocean in the world?","Pacific Ocean",1],
["Which is the largest plateau in the world?","Tibetan Plateau",1],
["Which day is observed as World Environment Day?[format:[eg] may 20]","June 5",1],
["During which year did World War I begin?[numbers]","1914",1],
["How many Cricket world cups[odi] does India have?[numbers]","2",1],
["True or false: Chameleon’s have extremely long tongues, sometimes as long as their bodies?","True",1],
["What makes up [approx.] 80% of our brain’s volume?","Water",1],
["An ostrich’s eye is bigger than its brain. True or False?","True",1],
["How many planets are there in our solar system?[numbers]","8",1],
["Which is the hottest continent on Earth?","Africa",1],
["Which is the smallest continent in the world?","Australia",1],
["What is the top colour in a rainbow?","Red",1],
["How many years are there in a millennium?[numbers]","1000",1],
["Which country is home to the kangaroo?","Australia",1],
["‘Stars and Stripes’ is the nickname of the flag of which country?[full name]","United States of America",1],
["Which language is used by the computer to process data?","Binary language",1],
["What type of bird lays the largest eggs?","Ostrich",1],
["What covers approximately 71% of the Earth’s surface: Land or Water?","Water",1],
["Which is the hardest substance available on earth?","Diamond",1],
["Which is the biggest desert in the world?","Sahara desert",1],
["Which country gifted The Statue of Liberty to the United States?","France",1],
["Who painted the Mona Lisa?","Leonardo da Vinci",1],
["Who invented the telephone?","Alexander Graham Bell",1],
["What is the name of the Greek God of music?","Apollo",1],
["What does the “SIM” in the SIM card stand for?","Subscriber Identity Module",1],
["Which is the first element on the periodic table of elements?","Hydrogen",1],
["Which is the longest written Constitution in the world?","India",1],
["What is the largest joint in the human body?","Knee",1],
["What does the Internet prefix WWW stand for?","World Wide Web",1],
["How many stars are there in the American flag?[numbers]","50",1],
["Which instrument is used to measure Atmospheric Pressure?","Barometer",1],
["Who is the inventor of the electric Bulb?","Thomas Alva Edison",1],
["How many primary colours are there?","Three",1],
["How many bones does an adult human have?[numbers]","206",1],
["What do you call a house made of ice?","Igloo",1],
]



#creating sockets
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = socket.gethostname()
port = 1233
HEADER_LENGTH = 10
start_=True
try:
    #binding sockets
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))
    start_=False

print('Waitiing for a Connection..')
ServerSocket.listen(5)

k=0

#to store connection of players
all_connections=[]
#to store names of players
user_list={}
#to store score of players
score_list={}
#to store sequence of buzzer of players in order
buzzer_list=[]

#to store threads
thread_list=[]
thread_list_send=[]

global no_of_player
#to take total no of players to play
def take_palyer():
    no_of_player=input("enter no of players (max=5) --> ")
    #if no of player is empty ask again
    if(no_of_player==''):
        print('\nplease enter valid no')
        return take_palyer()

    #if no of player valid
    if (int(no_of_player) <5 and int(no_of_player)>0):
        return no_of_player

    #if no of player is more then 5 ask again
    if(int(no_of_player)>5 or int(no_of_player)<0):
        print('\nmax 5 player are allowed' )
        return take_palyer()

if start_:
    no_of_player=take_palyer()
    print("----Waiting for connection----")

#send message to client that game has started
def send_start():
    for i in all_connections:
        start="start"
        start=start.encode('utf-8')
        start_header = f"{len(start):<{HEADER_LENGTH}}".encode('utf-8')
        try:
            i.send(start_header+start)
        except:
            pass

#send wait to client when all players have not connected
def send_wait():
    global all_connections
    for i in all_connections:
        wait="wait"
        wait=wait.encode('utf-8')
        wait_header = f"{len(wait):<{HEADER_LENGTH}}".encode('utf-8')
        try:
            i.send(wait_header+wait)
        except:
            pass
#to get user name of all players
def get_username(i,):
    global user_list
    global score_list
    try:
        username_header = i.recv(HEADER_LENGTH)
        if len(username_header)>0:
            username_length = int(username_header.decode('utf-8').strip())
            username = i.recv(username_length).decode('utf-8')
        print('user: ' + username + ' connected')
        #storing username of every client
        user_list[i]=username
        #initializing every players score to 0
        score_list[i]=0
    except :
        pass

#to get question and answer from question list
def getQuestion(Question_list,k):
    a=random.choice(Question_list)
    if k>54:
        #total question asked > no of question in list
        return
    #a[2]==1 means que is not asked
    if a[2]==1:
        #marking question as aksed
        a[2]=0
        k+=1
        print('\nQue->'+a[0])
        return(["Que) "+a[0],a[1]])
    else:
        return getQuestion(Question_list,k)

#to send question to all clinets
def send_question(que):
    global all_connections

    for i in all_connections:
        que_ask=que.encode('utf-8')
        que_header = f"{len(que_ask):<{HEADER_LENGTH}}".encode('utf-8')
        try:
            i.send(que_header+que_ask)
        except:
            pass
#to get buzzers form Clients
def get_buzzer(i,):
    try:
        answer_header = i.recv(HEADER_LENGTH)
        if len(answer_header):
            answer_length = int(answer_header.decode('utf-8').strip())
            answer = i.recv(answer_length).decode('utf-8')
            #buzzer 0 means buzzer wasnt pressed by client
            if not (answer=='0'):
                buzzer_list.append(i)
                print('buzzer pressed by->'+user_list[buzzer_list[0]])
    except :
        pass
#check if someone pressed buzzer
def if_buzzer_pressed(i,):
    timeS=0
    while(True):
        time.sleep(0.1)
        if(timeS>=10):
            try:
                i.send(("nopress").encode('utf-8'))
            except:
                pass
            break
        if(len(buzzer_list)>0):
            try:
                i.send(("pressed").encode('utf-8'))
            except :
                pass
            break
        timeS = timeS+0.1

#to check which player has pressed buzzer and
#letting him answer where tell others to wait
def send_buzzer():
    if(len(buzzer_list)>0):
        #first in buzzer_list will represt first client ot prss buzzer
        #sending him s-> answer
        try:
            buzzer_list[0].send("s".encode('utf-8'))
        except :
            pass
        for i in all_connections:
            #sending others n->to wait
            if not i == buzzer_list[0]:
                try:
                    i.send("n".encode('utf-8'))
                except :
                    pass
    else:
        #if length of buzzer_list=0 then no one pressed buzzer
        print('no one pressed buzzer')
        for i in all_connections:
            try:
                i.send('p'.encode('utf-8'))
            except :
                pass
#to check answer given by the clinet
def check_answer(ans):
    try:
        answer_header = buzzer_list[0].recv(HEADER_LENGTH)
        if len(answer_header):
            answer_length = int(answer_header.decode('utf-8').strip())

            answer = buzzer_list[0].recv(answer_length).decode('utf-8')
        print('answer given->'+answer)
        print('correct answer->'+ans)
        #checing if the answer is correct
        #if answer is correct 1 point is rewared
        if ans.lower() == answer:
            score_list[buzzer_list[0]]+=1
        #else 0.5 point is deducted
        else:
            score_list[buzzer_list[0]]-=0.5
    except :
        pass

#to send client that someone has answer the que now move on
def send_answer_checked():
        for i in all_connections:
            #sending others n->to wait
            if not i == buzzer_list[0]:
                try:
                    i.send("go".encode('utf-8'))
                except :
                    pass
#to send scores of all clinets
def send_scores():
    msg=""
    for user, score in score_list.items():
        msg = str(msg)+ str(user_list[user]) + '-->' +str(score)+'\n'
    print(msg)

    for i in all_connections:
        msg_send=msg.encode('utf-8')
        msg_header = f"{len(msg_send):<{HEADER_LENGTH}}".encode('utf-8')
        try:
            i.send(msg_header+msg_send)
        except :
            pass
#clearing buzzer list so again first element will represt first client to press buzzer
def delete_buffer():
    global buzzer_list
    buzzer_list.clear()

#to check if game is over
def check_gameover():
    for user , score in score_list.items():
        #if score is >=5 then game is over
        if score>=5:
            return (True,user)
    return (False,'')

#return winning messages
def send_winner(winner):
    msg=str(user_list[winner]) + ' wins the game'
    print(msg)
    for i in all_connections:
        msg_send=msg.encode('utf-8')
        msg_header = f"{len(msg_send):<{HEADER_LENGTH}}".encode('utf-8')
        try:
            i.send(msg_header+msg_send)
        except :
            pass
# if game is tied
def tsaTie():
    msg="--No one wins the game--\n-----final scores are-----\n"
    for user, score in score_list.items():
        msg = str(msg)+ str(user_list[user]) + '-->' +str(score)+'\n'
    print(msg)

    for i in all_connections:
        msg_send=msg.encode('utf-8')
        msg_header = f"{len(msg_send):<{HEADER_LENGTH}}".encode('utf-8')
        try:
            i.send(msg_header+msg_send)
        except :
            pass
#for every step server will send a code which says which function
#on client side to run maintaing a proper flow
def send_check(next):
    global all_connections
    t=0
    for i in all_connections:
        try:
            i.send(next.encode('utf-8'))
        except:
            #count no of disconnected clients
            t+=1
            pass

    # if all user disconnected then stop the game
    if(int(no_of_player) == t):
        return True
    else:
        return False

#function to start game
def start_game():
    #to clear all previous threads
    thread_list.clear()
    for i in all_connections:
        #storing threads
        thread_list.append(threading.Thread(target=get_username,args=(i,)))

    for i in thread_list:
        #starting all threads
        i.start()

    for i in thread_list:
	    # wait until other threads are completely executed
        i.join()

    #k indicates no of question asked
    k=0
    while True:
        #get pair of question and answer
        pair = getQuestion(Question_list,k)
        if pair:
            k+=1
            que=pair[0]
            ans=pair[1]

            #send q indicating run function to get question
            send_check('q')
            #sending question to all Clients
            send_question(que)
            #to clear all previous threads
            thread_list.clear()
            thread_list_send.clear()

            #send b indicating run function to press buzzer to client
            send_check('b')
            for i in all_connections:
                #storing threads
                thread_list.append(threading.Thread(target=get_buzzer,args=(i,)))
                thread_list_send.append(threading.Thread(target=if_buzzer_pressed,args=(i,)))

            for i in range(len(thread_list)):
                #starting all threads
                thread_list[i].start()
                thread_list_send[i].start()

            for i in range(len(thread_list)):
        	    # wait until other threads are completely executed
                thread_list[i].join()
                thread_list_send[i].join()

            #send results of buzzer pressed
            send_buzzer()

            #if someone pressed buzzer ask him anser
            if(len(buzzer_list)>0):
                #to get answer from the client who have pressed buzzers
                #and evaluate the answer
                check_answer(ans)
                send_answer_checked()
            #send z indicating run function to get scores of every client
            send_check('z')
            #to send score to Clients
            send_scores()

            #to clear buzzer_list
            delete_buffer()

            #checking if game is over
            check=check_gameover()
            #check if question bank is empty
            if(k>=54):
                send_check('w')
                itsaTie()
                break
            #if over
            if check[0]:
                #send w indicating run function to get winner name
                send_check('w')
                send_winner(check[1])
                break
            #if not over
            else:
                #send 0 indicating continue the game
                stop=send_check('0')

        # if all users disconnected then stop the game
        if(stop):
            print('all players disconnected')
            break
        #if all questions are asked repeat the question


while True:
    #accepting the connection
    Client, address = ServerSocket.accept()

    #if client is not in list add him
    if Client not in all_connections:
        all_connections.append(Client)
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    print('user connected =  :' + str(len(all_connections)))

    #if total players connected == total players required for the game
    #start the game
    if len(all_connections)==int(no_of_player):
        print("game started\n")
        #send message to client to start game
        send_start()
        #starting the game from server side
        start_game()

        break
    else:
        #send message to client to wait for game to start
        send_wait()
ServerSocket.close()
