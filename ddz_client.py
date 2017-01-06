# telnet program example
import socket, select, string, sys
from cardcolor import UseStyle
import json

username = ''
color = 0
def pack_data(data,data_type):
    return json.dumps([data_type,data])

def is_json(myjson):  
    try:  
        json.loads(myjson)  
    except ValueError:  
        return False  
    return True  

def prompt() :
    print UseStyle(('['+username+']'),fore='white',disable = color)
    sys.stdout.flush()

def server_come(msg):
    cards = ''
    print 'SERVER:',
    if is_json(msg):
        data_json = json.loads(msg)
        data_type = data_json[0]
        if data_type == 'cards':
            cards = data_json[1]
            for c in cards:
                print UseStyle(c[0],fore=c[1],disable = color),
            print
    else:
        print UseStyle(msg,fore='cyan',disable = color)
        sys.stdout.flush()
    
if __name__ == "__main__":
    
    print UseStyle('Please input your username',fore='green',disable = color)
    username = raw_input('>>')

    if(len(sys.argv) < 3) :
        print 'Usage : python ddz_client.py hostname port'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Start Enjoy DDZ'

    prompt()
    while 1:
        
        rlist = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_list, write_list, error_list = select.select(rlist , [], [])
         
        for sock in read_list:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    #sys.stdout.write(data)
                    server_come(data)
                    prompt()
             
            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(pack_data(msg,'robs'))
                prompt()

