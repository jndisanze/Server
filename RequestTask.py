from threading import Lock

class RequestTask(object):
    '''Classe faisant office d'intermediaire pour la reception de message lors d'envoi de PING'''
    responseList = []
    lock = Lock()
    
    def __init__(self):
        '''Cree une RequestTask'''
        pass
    
    @staticmethod
    def addResponse(response):
        '''Ajoute un message dans la liste'''
        RequestTask.lock.acquire()
        RequestTask.responseList.append(response)
        RequestTask.lock.release()
    
    @staticmethod
    def getResponses():
        '''Permet d'obtenir la liste des reponses de la liste'''
        newList = []
        
        RequestTask.lock.acquire()
        
        for i in range(len(RequestTask.responseList)):
            newList.append(RequestTask.responseList[i])
        
        for i in range(len(RequestTask.responseList)):
            RequestTask.responseList.remove(RequestTask.responseList[0])
        
        RequestTask.lock.release()
        
        return newList