import Router as router
import MessageThread as message
import random
from Help import *
from RequestTask import RequestTask

def initAndStartRouter():
    '''Cree et demarre le routeur'''
    r=router.router("net_6_rt_1_192.168.0.6")
    r.listen()
        
    return r

def sendTraceroute(r,receiverName,message):
    '''Permet l'envoi au routeur de message pour tracer la route vers un destinataire fournit en parametre
    de la fonction'''
    ttl = 1
    arrived = False
    
    r.sendMessage(receiverName,message)
    while arrived == False:
        
        while len(RequestTask.getResponses()) == 0 : 
            pass
        
        response = RequestTask.getResponses()[0]
        partition1 = response.partition(" ")
        type = partition1.partition(" ")[0]
            
        arrived = (type=="PONG")
        
        if arrived == False:
            message = message.createMessage(r.getName(),receiverName,ttl,"PING")
            r.sendMessage(receiverName,message)
    
        print response
        
def waitResponseOfPing():
    '''Attend la reponse d'un ping'''
    arrived = False
    
    while arrived == False:
        while len(RequestTask.getResponses()) == 0 : 
            pass
        
        list = RequestTask.getResponses()
        
        print list[0]
        
        arrived = True
        
def startConsole(r):
    '''Demarre la console d'administration du routeur'''
    help = Help()
    isFinish = False
    
    while isFinish == False: 
        print help.options()
        nrOption = help.readOption()
    
        if nrOption == 1:
            intervalValue = help.choiceIntervalValue()
            r.getForwardingTable().setInterval(intervalValue)
            
        if nrOption == 2:
            pass
    
        if nrOption == 3:
            receiverName,myMessage = help.sendChatToRouter()
            aMessage = message.createMessage(r.names(),receiverName,255,"CHAT",myMessage)
            r.sendMessage(receiverName, aMessage)
        
        if nrOption == 4:
            receiverName = help.sendPingOrTraceRouteToReceiver()
            rand = random.randint(1,65535)
            aMessage = message.createMessage(r.names(), receiverName,255,"PING", str(rand))
            r.sendMessage(receiverName, aMessage)
            waitResponseOfPing()
        
        if nrOption == 5:
            receiverName = help.sendPingOrTraceRouteToReceiver()
            rand = random.randint(1,65535)
            aMessage = message.createMessage(r.names(),receiverName,1,"PING", str(rand))
            sendTraceroute(r,receiverName,aMessage)
            
        if nrOption == 6:
            print r.getForwardingTable().getLinesOfForwardingTable()
    
        if nrOption == 7:
            distanceVectorList = r.getDistanceVectorList()
            print help.distanceVectorsToString(distanceVectorList)
    
        if nrOption == 8:
            loggingList = r.getLoggingList()
            print help.loggingToString(loggingList)
    
        if nrOption == 9:
            isFinish = True
            r.stop()
        
        print help.getAndClearBuffer()
        
def main():
    r = initAndStartRouter()
    startConsole(r)

main()