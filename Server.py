import socket, select
from DDZ import DDZ
import json

def is_json(myjson):  
    try:  
        json.loads(myjson)  
    except ValueError:  
        return False  
    return True  
'''
PROTOCOL
[type,data]
'''

def process_data(data):
    if not is_json(data):
        return 
    data_json = json.loads(data)
    print data_json
    if len(data_json) < 2:
        print 'DATA BROKEN'
    data_type =data_json[0]
    data =data_json[1]
    
    if data_type == 'rob':
        user_id = data['id']
        score = data['score']
        
        broadcast_data(sockfd, '\r'+str(d.play_sequence %3+1)+'ROB!')
        if d.play_sequence %3 +1 == user_id:
            d.rob_the_landlord(d.play_sequence %3 +1,int(score))
            d.play_sequence +=1
        else:
            CONNECTION_LIST[user_id].send('It is not your turn')
            
        if d.score ==3:
            print d.landlord_id,'is Landlord'


def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket:
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)
 
if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(30)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "DDZ server started on port " + str(PORT)
    d = DDZ()

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Player (%s, %s) connected" % addr
                broadcast_data(sockfd, "[%s:%s] entered room,"% addr+str(len(CONNECTION_LIST)-1)+" user(s) online \n" )
                if len(CONNECTION_LIST)-1 == 3:
                    print 'GAME START'
                    broadcast_data(sockfd, 'GAME START')
                    print CONNECTION_LIST
                    print 'Deal Cards'
                    d.generate_cards()
                    d.shuffle()
                    d.deal()
                    d.sort()
                    print len(CONNECTION_LIST),CONNECTION_LIST[1],CONNECTION_LIST[2],CONNECTION_LIST[3]
                    CONNECTION_LIST[1].send(json.dumps(['cards',d.get_colorful_card_name(1)]))
                    CONNECTION_LIST[2].send(json.dumps(['cards',d.get_colorful_card_name(2)]))
                    CONNECTION_LIST[3].send(json.dumps(['cards',d.get_colorful_card_name(3)]))
                    broadcast_data(sockfd, json.dumps(['cards',d.get_colorful_card_name(-1)]))
                    broadcast_data(sockfd, '\rRob Landlord')
                    broadcast_data(sockfd, '\r'+str(d.play_sequence %3+1)+'ROB!')

            else:   
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)

                    if data:
                        process_data(data)

#                         broadcast_data(sock, "\r" + '<' + data + '> enter ddz room\n')
#                         broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)                

                except Exception as e:
                    print e
                    broadcast_data(sock, "Player (%s, %s) is offline" % addr)
                    print "Player (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
    
