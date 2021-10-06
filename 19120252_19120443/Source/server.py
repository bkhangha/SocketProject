import socket
import threading
#Ham gui file
def SendFile(Client, Namefile):
    f=open(Namefile, 'rb')
    L = f.read()
    header ="""HTTP/1.1 200 OK

"""
    print("-----HTTP respone------- ")
    data=header.encode()+L
    Client.send(data)	
#Ham tao server
def CreateSocketServer(host, port): 
	Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	Server.bind((host,port))
	Server.listen(4)
	return Server

#Ham kiem tra mat khau
def CheckPass(Request): 
	if "Username=admin&Password=admin" in Request: 
		return True
	else: 
		return False
#Ham doc request
def ReadRequest(Client):
	request = ""
	Client.settimeout(1)
	try:
		request = Client.recv(1024).decode()# doc Chunked
	except socket.timeout: 
			print("Timeout!")
	finally:
		return request

# Ham xu li request
def parseRequest(ReqMsg:str):
    #tach dong dau
    firstline=ReqMsg.split("\r\n")[0]
    #tach method
    method=firstline.split(" ")[0]
    #tach url
    url=firstline.split(" ")[1]
    #tach version
    version=firstline.split(" ")[2]
    #phan tich url
    if url[0]=='/':
        protocol="http"
        path=url[1:]
    elif "http" in url:
        protocol="http"
        pos=url.find("/",7)
        path=url[pos+1:]
    else: 
        protocol="https"
        path=""
    #tach host
    pos1=ReqMsg.find("Host: ")
    pos2=ReqMsg.find('\r',pos1)
    host=ReqMsg[pos1+6:pos2]
    #tra ve mot dictonary
    return {"method":method , 
            "protocol":  protocol,
            "host":host ,
            "path":path,
            "version":version  }
# Ham xu li truy cap
def Process(Sock:socket):
    req= ReadRequest(Client)
    httpreq=parseRequest(req)
    if(httpreq["path"]=="info.html"):
        if(CheckPass(req) ):
            SendFile(Sock,"info.html")
        else:
            SendFile(Sock,"404.html")
    else:
        SendFile(Sock,httpreq["path"])
    print(httpreq)
    print("------HTTP requset-------- " )
    print(req)
    Sock.close()
       

if __name__ == "__main__":
    #Tao server
    Server = CreateSocketServer("127.0.0.1",8000)
    while True :
        print("----Truy cap Server 127.0.0.1:8000----")
        Client, address = Server.accept()
        t1=threading.Thread(target=Process,args=(Client,))# xu li da luong
        t1.start()
        t1.join()