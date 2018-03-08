import time
import pickle
import threading
from threading import Lock,Thread

class tableForwarding(threading.Thread):
    '''Classe jouant le role de table de forwarding et envoyant a intervalle regulier le contenu
    de sa table aux routeurs voisins'''
    def __init__(self,time):
        '''Construit la table de forwarding en specifiant en parametre l'intervalle de temps
        auxquel la table doit envoyer ses infos a ses routeurs voisins'''
        
        threading.Thread.__init__(self)
        self.time=float(time)
        self.forwardTab={}
        self.mutex = Lock()
        self.terminated = False
        
        try:
            f = open('file','rb') 
            self.forwardTab=pickle.load(self.f)
        except:
            pass
        
    def add(self,name,adresse,cost):
        '''Permet l'ajout d'un enregistrement dans la table de forwarding'''
        self.mutex.acquire()
        self.forwardTab[name]=[adresse,cost]
        fo = open('file', "wb")
        pickle.dump(self.forwardTab,fo)
        self.mutex.release()
        
    def existing(self,adresse):
        '''Verifie s'il existe un enregistrement dans la table de forwarding correspondant a une adresse
        fournie en parametre'''
        exist=None
        try:
            return self.forwardTab[adresse]
        except:
            return exist
        return exist
    
    def outputInterfaceTo(self,destAdress):
        '''
        Permet de determiner l'interface de sortie(adresse IP+port) pour une destination
        '''
        value = self.existing(destAdress)
        interface = None
        
        if( value != None ):
            return value

    def getLinesOfForwardingTable(self):
        '''Retourne sous forme textuelle le contenu de la table de forwarding'''
        keys = self.forwardTab.keys()
        
        txt = ""
        i = 0
        while i < len(keys):
            key = keys[i]
            
            value = self.forwardTab[key]
            adress = value[0]
            cost = value[1]
            
            partition = key.partition(".")
            
            if partition[1] != "" :
                adress1 = key[0:len(key)-4]
                port = key[len(key)-4:len(key)]
                
                txt += adress1
                txt += "/"
                txt += port
            else:    
                txt += key
                    
            txt += "   "
            txt += adress[0]
            txt += "/"
            txt += adress[1]
            txt += "   "
            txt += cost
            txt += "\n"
            
            i += 1
        
        return txt
    
    '''
    Modifie l'intervalle d'envoi de mise a jour des vecteurs de distance
    '''
    def setInterval(self,time):
        self.time = time
    
    '''
    Permet d'arreter l'envoi regulier de mise a jour des vecteurs de distance
    '''
    def stop(self):
        self.terminated = True
        
    def run(self):
        '''Envoi a intervalle regulier les vecteurs de distance aux voisins'''
        #permet la mise a jour de la table au routeur voisin
        while(self.terminated == False):
         #utilisation de la classe message pour envoyer les donnes si le cout vaut 1 
            time.sleep(self.time*100.) 
            for i in self.forward:
                #traitement de vecteur-distance
                i