import socket
import ConnectionServer
import tableForwarding
from threading import Thread, Lock

def parse(fichier):
    '''
    Methode qui permet de parcourir le fichier de configuration du routeur afin de parametrer
    correctement le routeur
    '''
    f=open(fichier,"r")
    name=f.readline()
    vect=int(f.readline())
    n=int(f.readline())
    res=range(3+n)
    res[0]=name
    res[1]=vect
    res[2]=n
    
    for i in range(3,len(res)):
        res[i]=f.readline()
        
    return res   

class router:
    def __init__(self,fichier):
        '''
        Cree le routeur sur base du fichier de configuration
        '''
        self.config = parse(fichier)
        self.name=self.config[0]
        self.listeInterface=range(self.config[2])
        self.connectionList = []
        self.distanceVectorList = []
        self.loggingList = []
        fw=tableForwarding.tableForwarding(self.config[1])
        self.fw = fw # ligne ajoute par laurent
        
        #mise a jour reguliere de la FIB vers les routeur connu
        fw.start()
        
        #Cree les differentes connexions correspondant aux interfaces du routeur
        for i in range(self.config[2]):
            interface = self.config[i+3].split(' ')
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((interface[0],int(interface[1])))
            s.connect((interface[2],int(interface[3])))
            #contient la connection ouverte UDP,ip+port du router voisin connu,+temps de mise ajour de la FIB 
            self.listeInterface[i]=(s,interface,interface[4],fw)

    def sendMessage(self,destAdress,message):
        '''
        Envoie un message a un destinataire en se basant sur la table de forwarding pour
        acheminer le message vers la bonne interface
        '''
        interface = self.fw.outputInterfaceTo(destAdress)
        
        if interface != None:
            connectionThread = self.getConnectionServer(interface)
            connectionThread.sendMessage(message)
    
    def addLog(self,log):
        self.loggingList.append(log)
    
    def getLoggingList(self):
        return self.loggingList
        
    def addDistanceVector(self,record):
        '''
        Permet d'ajouter un vecteur de distance a la liste existante
        '''
        self.distanceVectorList.append(record)
        
    def stop(self):
        '''Permet l'arret du routeur'''
        
        for interface in self.connectionList:
            interface.stop()
        self.fw.stop()
        
    def getDistanceVectorList(self):
        '''Permet d'obtenir la liste des vecteurs de distance'''
        return self.distanceVectorList
    
    def getConnectionServer(self,interface):
        '''Permet d'obtenir la thread correspondante a une certaine interface'''
        connectionToUsed = None
        
        for connection in self.connectionList:
            inputAdress = connection.getInputAdress()
            
            if interface[0] == inputAdress[0] and interface[1] == inputAdress[1]:
                connectionToUsed = connection
        
        return connectionToUsed
    
    def listen(self):
        '''Permet de creer les differentes threads jouant le role d'interface du routeur, de les demarrer
        et de les enregistrer dans une liste'''
        for con in self.listeInterface:
            connection=ConnectionServer.ConnectionServer(con)
            connection.start()
            self.connectionList.append(connection)
            
    def names(self):
        '''Retourne le nom du routeur'''
        return self.name
    
    def getForwardingTable(self):
        '''Retourne la table de forwarding'''
        return self.fw
