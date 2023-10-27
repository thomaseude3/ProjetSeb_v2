# -*- coding: utf-8 -*-

"""
Created on Mon Feb 28 17:06:13 2022

Le module Camera regroupe toutes les fonctionnalités du banc liées à la caméra Basler, qu'il s'agisse du streaming, de l'acquistion ou de l'enregistrement des images sur le disque dur.

Ce module regroupe :
    - Les fonctions élémentaires de la caméra (connexion et paramétrage, acquisition d'une photo)
    - Les classes (QThread) permettant de réaliser en multithreading les opérations :
        - De streaming du flux vidéo de la caméra vers l'IHM principale
        - D'acquisition à haute vitesse (600 fps) d'images de la caméra
        - D'enregistrement asynchrone des images acquises par le thread d'acquisition
    
En fin de module, des tests unitaires permettent de tester la connexion de la caméra, la prise d'images ainsi que l'acquisition / enregistrement de ces images.
"""

import cv2
import numpy as np
import time
from pypylon import pylon 
import os.path
import os
from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path


def connectCamera(width,height,exposureTime,fps) :
    """
    Fonction réalisant la connexion de la caméra Basler et le réglage de la zone d'acquisition.

    | Crée l'objet camera à partir de la première camera Basler connectée trouvée.
    | Règle la taille de la zone d'acquisition à l'aide des paramètres width et height (ROI centré sur l'image).
    | Règle la vitesse du capteur à "Fast".
    | Règle le temps d'exposition à 1 ms.
    
    | En fonctionnement classique, la fonction renvoie un objet camera de la librairie pypylon
    | En cas de problème de connexion, la fonction renvoie None.
    
    :param int width: largeur en pixel de la zone d'acquisition de la caméra
    :param int height: hauteur en pixel de la zone d'acquisition de la caméra
    
    :return: Objet camera (librairie pypylon)
    :rtype: pylon.InstantCamera
    """
    
    try :
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()  #Need to open camera before can use camera.ExposureTime
        camera.Width = width
        camera.Height = height
        
        camera.CenterX.SetValue(True)
        camera.CenterY.SetValue(True)
        
        # camera.SensorReadoutMode = "Fast"
        camera.AcquisitionFrameRateEnable.SetValue(True)                     
        camera.AcquisitionFrameRate.SetValue(fps)
        camera.ExposureTime.SetValue(exposureTime)  
        
        camera.PixelFormat.SetValue("BGR8")
        
        return camera
    
    except :
        print("ERREUR : Problème de connexion Caméra")
        return None


def oneImage(camera) :
    """
    Fonction réalisant la prise d'une image par un objet caméra Basler (pypylon) 
    
    | Lance l'acquisition de la caméra
    | Récupère une image
    | Arrête l'acquisition de la caméra
    | Renvoie l'image acquise au format numpy.ndarray
    
    :param pylon.InstantCamera camera: Objet camera (librairie pypylon)
    
    :return: l'image prise par la caméra et enregistrée dans la matrice
    :rtype: numpy.ndarray
    """
    
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    grabResult = camera.RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)
    
    if grabResult.GrabSucceeded():
        image = grabResult.GetArray().copy()
    else :
        image = 0
        
    camera.StopGrabbing()
    return image


def setImageSize(camera,width,height):
    camera.Width = width
    camera.Height = height
    
    camera.CenterX.SetValue(True)
    camera.CenterY.SetValue(True)
    
def setExposureFps(camera,exposureTime,fps) :
    
    camera.AcquisitionFrameRate.SetValue(fps)
    camera.ExposureTime.SetValue(exposureTime)     
    

#################################
# THREAD LIVE CAMERA
#################################

class Streaming(QThread):
    """
    Mode live de la caméra : retransmission dans l'IHM en temps réel du flux vidéo pris par la caméra.
    
    | Permet la retransmission en multithreading du flux vidéo de la caméra Basler.
    | Cette classe hérite de la classe QThread de la librairie PyQt
    
    :param pylon.InstantCamera camera: Objet camera (librairie pypylon)
    :param PyQt5.QWidget parent: Parent au sens PyQt de l'objet Streaming créé. Ici le parent est l'objet de la classe :class:`IHM_principale.IHMprincipale`
    
    :var bool run_flag: Booléen permettant l'arrêt de la boucle de streaming
    :var int fps: Vitesse d'acquisition de la caméra pour le streaming    
    """
    
    maj_Image = pyqtSignal(np.ndarray)
    """pyqtSignal permettant de transférer le flux d'images depuis l'objet :class:`Streaming` vers l'objet :class:`IHM_principale.IHMPrincipale`"""
    
    def __init__(self,camera,parent):
        QThread.__init__(self, parent = parent)
        self.camera = camera
        self.image = None
        self.run_flag = True
        self.enregistrement_flag = False
        # self.fps = 60
        
    def run(self):
        """
        Fonction threadée de streaming vidéo depuis la caméra Basler
        
        Cette fonction paramètre la vitesse de la caméra, lance l'acquisition et retransmet les images acquises via le pyqtSignal maj_Image
        """
        print("> Streaming : Démarrage Streaming Caméra")
        self.run_flag = True
        self.enregistrement_flag = False
        self.frames = []
        # self.camera.AcquisitionFrameRate.SetValue(self.fps)
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        
        while self.run_flag :
            grabResult = self.camera.RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                self.maj_Image.emit(grabResult.GetArray())
                if self.enregistrement_flag :
                    self.frames.append(grabResult.GetArray().copy())
            grabResult.Release()
            
        self.camera.StopGrabbing()
        print("> Streaming : Arrêt Streaming Caméra")
        
        
    def stop(self) :
        """
        Passe la valeur du flag d'acquisition run_flag à False pour arrêter la boucle d'acquisition
        """
        print("> Streaming : Ordre d'arrêt Streaming Caméra reçu")
        self.run_flag = False
        

#################################
# THREAD ENREGISTREMENT ACQUISITION
#################################

class EnregistrementThread(QThread): #thread chargé d'enregistrer les images du tableau
    """
    Thread d'enregistrement asynchrone des images acquises par la classe :class:`VideoThread`
    
    | Récupère la liste d'images générée par l'objet de la classe :class:`VideoThread`
    | Enregistre au format bmp les images dans le dossier choisi
    | Remplace les images par des 0 dans la liste afin de libérer de la mémoire vive
    | Réitère l'opération pour récupérer les nouvelles images ajoutées à la liste
    
    :param videothread: Thread d'acquisition des images depuis la caméra Basler
    :type videothread: :class:`VideoThread` 
    :param pathlib.Path path: Chemin du dossier d'acquisition (librairie pathlib)
    :param PyQt5.QWidget parent: Parent au sens PyQt de l'objet EnregistrementThread créé. Ici le parent est l'objet de la classe :class:`IHM_principale.IHMprincipale`
    
    :var bool run_flag: Booléen permettant l'arrêt de la boucle d'enregistrement
    :var int numero_de_frame: Indice de la prochaine image à traiter dans la liste d'images
    """
    
    end_enregistrement = pyqtSignal(bool)
    """pyqtSignal permettant d'indiquer à l'IHM principale que l'enregistrement des images est terminé"""
    
    def __init__(self, videothread, path, parent):
        QThread.__init__(self, parent = parent)
        self.videothread = videothread
        self.run_flag = True 
        self.numero_de_frame = 0
        self.path = path
        
    def run(self):
        """
        Fonction threadée d'enregistrement asynchrone des images de la caméra Basler acquises par le Thread d'acquisition :class:`VideoThread`
        
        | Enregistre au fur et à mesure de l'acquisition les images dans le dossier choisi
        | Lorsque aucune nouvelle image n'est trouvée dans la liste d'acquisition, vérifie si le Thread d'acquisition a été arrêté. 
        | Si c'est le cas, le Thread d'enregistrement est stoppé automatiquement et un pyqtSignal est emis
        | Supprime le Thread d'acquisition :class:`VideoThread` et se supprime lui-même
        """
        print("> Enregistrement : Démarrage Enregistrement Images")
        self.j = 0

        while self.run_flag :
  
            n = len(self.videothread.frames[self.numero_de_frame:])
            
            
            if n!= 0 :
                for self.j in range(self.numero_de_frame,self.numero_de_frame+n):
                    chemin_fichier = str(Path(self.path,str(self.numero_de_frame).zfill(5)+".bmp"))
                    cv2.imwrite(chemin_fichier, self.videothread.frames[self.j])
                    self.videothread.frames[self.j]=0
                    self.numero_de_frame+=1

            else:
                if self.videothread.run_flag == False :
                    self.stop()
                time.sleep(0.02)
                
        print("> Enregistrement : Arrêt Enregistrement Images")
        self.end_enregistrement.emit(True)      
   
    
    def stop(self):
        """
        Passe la valeur du flag d'enregistrement run_flag à False pour arrêter la boucle d'enregistrement
        """
        print("> Enregistrement : Ordre d'arrêt Enregistrement Caméra reçu")
        
        self.run_flag = False
        







###################################################
# PAS UTILISE
###################################################

#################################
# THREAD ACQUISITION
#################################
        
class VideoThread(QThread):
    """
    Thread d'acquisition des images à haute vitesse depuis la caméra Basler
    
    | Permet l'enregistrement dans une liste des images acquises par la caméra
    | Cette classe hérite de la classe QThread de la librairie PyQt
    
    :param pylon.InstantCamera camera: Objet camera (librairie pypylon)
    :param PyQt5.QWidget parent: Parent au sens PyQt de l'objet VideoThread créé. Ici le parent est l'objet de la classe :class:`IHM_principale.IHMprincipale`
    
    :var bool run_flag: Booléen permettant l'arrêt de la boucle d'acquisition
    :var list frames: Liste des images acquises par la caméra Basler
    :var int fps: Vitesse d'acquisition de la caméra pour l'acquisition
    """
    
    float_frameRate = pyqtSignal(float)
    """pyqtSignal permettant de retransmettre à l'IHM principale la cadence d'aquisition réelle de la caméra"""
    
    def __init__(self, camera, parent):
        QThread.__init__(self, parent = parent)
        self.camera = camera
        self.frames = [] # liste de stockage de la donnée des images
        self.fps = 600
        self.run_flag = True
        
    
    def run(self): 
        """
        Fonction threadée d'acquisition des images de la caméra Basler
        
        Cette fonction : 
        
            - Paramètre la vitesse de la caméra
            - Renvoie à l'IHM Principale la cadence d'acquisition réelle de la caméra
            - Lance l'acquisition
            - Sauvegarde les images dans la liste frames
        """
        print("> Acquisition : Démarrage Acquisition Caméra")
        self.run_flag = True #flag pour arreter le widget video 
        self.frames = [] # liste de stockage de la donnée des images 
        
        try :         
            # self.camera.SensorReadoutMode = "Fast"
            self.camera.AcquisitionFrameRateEnable.SetValue(True)                     
            self.camera.AcquisitionFrameRate.SetValue(self.fps) # fps du flux video réglés à 600 fps 
            self.camera.ExposureTime.SetValue(1000)
            self.frameRate = self.camera.AcquisitionFrameRate.GetValue()
            self.float_frameRate.emit(self.frameRate)
           
            
            #Grabing Continusely (video) with minimal delay
            self.camera.StartGrabbing() 
            self.t0 = -time.time()
        
            while self.run_flag : #boucle flux video 
                
                grabResult = self.camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
            
                if grabResult.GrabSucceeded():
                    
                    self.frames.append(grabResult.GetArray().copy())
    
                else :
                    print("> Acquisition : Erreur Grabbing, frame",len(self.frames)) 
                grabResult.Release()
                    
                    
            self.camera.StopGrabbing()
            print("> Acquisition : Arrêt Acquisition Caméra")           

        except: # si camera non connéctée 
            if self.run_flag == True :
                print("> Acquisition : Erreur Caméra")
            else :
                print("> Acquisition : Arrêt Acquisition Caméra")
            
            
    def stop(self): #arret definitif du thread
        """
        Passe la valeur du flag d'acquisition run_flag à False pour arrêter la boucle d'acquisition
        """
        print("> Acquisition : Ordre d'arrêt Acquisition Caméra reçu")
        self.run_flag = False  

        




__all__ = [
'connectCamera',
'oneImage',
'Streaming',
'VideoThread',
'EnregistrementThread',
]	

# Tests Unitaires :
# 
if __name__ == '__main__':

    print("\nTEST UNITAIRE : Camera_Acquisition")
    camera = connectCamera(640,480)
    image = oneImage(camera)
    # print(image)
    # image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    cv2.imshow("Acquisition camera", image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    print("> Fin du test unitaire d'acquisition")
    
    
    testName = "Camera_Enregistrement"
   
    print("\nTEST UNITAIRE :",testName)
   
    import shutil
    from pathlib import Path
   
    testPath = Path(Path(__file__).parents[0],"Ressources","TestsUnitaires",testName)
    
    if os.path.isdir(testPath) :
        shutil.rmtree(testPath)
    os.mkdir(testPath)
    os.mkdir(Path(testPath,"Acquisition"))
    os.mkdir(Path(testPath,"Acquisition","Images_brutes"))
    
    videoThread = VideoThread(camera,None)
    enregistrementThread = EnregistrementThread(videoThread, testPath, None)
    
    videoThread.start()
    enregistrementThread.start()
    
    time.sleep(3)
    
    videoThread.stop()    
    
    camera.Close()

