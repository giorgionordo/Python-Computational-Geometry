from pygc.punto import gcPunto
from pygc.segmento import gcSegmento
from pygc.listapunti import gcListaPunti
from pygc.poligono import gcPoligono
from pygc.triangolo import gcTriangolo
# import matplotlib.pyplot as plt
# import seaborn   # pacchetto che aggiunge uno stile più moderno nella resa grafica
# seaborn.set()    # avvia l'interfaccia grafica di seaborn


class gcBoundingBox:
    """ classe di geometria computazionale in Python
        che definisce i bounding box nel piano ed i relativi metodi primitivi
        autore: Giorgio Nordo - Dipartimento MIFT Università di Messina
        www.nordo.it   |  giorgio.nordo@unime.it """

    # costruttore del bounding box di un oggetto di tipo punto, segmento
    # lista di punti, poligono, oggetto bounding box
    # o direttamente come tupla (quadrupla) delle coordinate estremali
    # memorizzando le coordinate estremali
    def __init__(self, lv=None):
        """ crea il bounding box di un oggetto di tipo punto, segmento, triangolo
            lista di punti o poligono o anche come oggetto bounding box
            o direttamente come tupla (quadrupla) delle coordinate estremali
        """
        if type(lv) == gcPunto:               # se il parametro ricevuto è un punto
           xmin = xmax = lv.getx()
           ymin = ymax = lv.gety()
        #------------------------------------------------------------------------
        elif type(lv) == gcSegmento:          # se il parametro ricevuto è un segmento
            xmin = min(lv.getInizio().getx(), lv.getFine().getx())
            xmax = max(lv.getInizio().getx(), lv.getFine().getx())
            ymin = min(lv.getInizio().gety(), lv.getFine().gety())
            ymax = max(lv.getInizio().gety(), lv.getFine().gety())
        #------------------------------------------------------------------------
        elif type(lv) == gcTriangolo:         # se il parametro ricevuto è un triangolo
            xmin = min(lv[1].getx(), lv[2].getx(), lv[3].getx())
            xmax = max(lv[1].getx(), lv[2].getx(), lv[3].getx())
            ymin = min(lv[1].gety(), lv[2].gety(), lv[3].gety())
            ymax = max(lv[1].gety(), lv[2].gety(), lv[3].gety())
        #------------------------------------------------------------------------
        elif type(lv) == gcListaPunti:        # se il parametro ricevuto è una lista di punti
            xmin = min([p.getx() for p in lv])
            xmax = max([p.getx() for p in lv])
            ymin = min([p.gety() for p in lv])
            ymax = max([p.gety() for p in lv])
        #------------------------------------------------------------------------
        elif type(lv) == gcPoligono:          # se il parametro ricevuto è un poligono
            xmin = lv.xMin()
            xmax = lv.xMax()
            ymin = lv.yMin()
            ymax = lv.yMax()
        #------------------------------------------------------------------------
        elif type(lv) == gcBoundingBox:       # se il parametro ricevuto è un bounding box
            (xmin, xmax, ymin, ymax) = lv.get()
        #------------------------------------------------------------------------
        elif type(lv) in (list, tuple):               # se il parametro ricevuto è una lista o una tupla
            if len(lv) == 4:        # verifica che ci siano effettivamente quattro elementi nella tupla
                (xmin, xmax, ymin, ymax) = (lv[0], lv[1], lv[2], lv[3])
        #------------------------------------------------------------------------
        else:   # in tutti gli altri casi assegna coordinate vuote
            xmin = xmax = ymin = ymax = None
        # memorizza le proprietà nell'oggetto
        self.__xmin = xmin
        self.__xmax = xmax
        self.__ymin = ymin
        self.__ymax = ymax


    # restituisce il bounding box sotto forma di tupla
    def get(self):
        """ restituisce la tupla dei parametri del bounding box corrente
        """
        t = (self.__xmin, self.__xmax, self.__ymin, self.__ymax)
        return t

    # restituisce il valore xmin
    def getXMin(self):
        """ restituisce il valore xmin
        """
        return self.__xmin

    # restituisce il valore xmax
    def getXMax(self):
        """ restituisce il valore xmax
        """
        return self.__xmax

    # restituisce il valore ymin
    def getYMin(self):
        """ restituisce il valore ymin
        """
        return self.__ymin

    # restituisce il valore ymax
    def getYMax(self):
        """ restituisce il valore ymax
        """
        return self.__ymax
    # ------------------------------------------------------------------------------------

    # restituisce il bounding box come stringa
    # col metodo speciale __str__
    def __str__(self):
        """ restituisce il bounding box in formato stringa
        """
        if self.__xmin == None:
            s = ''
        else:
            s = f"BB({round(self.getXMin(), gcPunto.getPrecisione())}, " \
                f"{round(self.getXMax(), gcPunto.getPrecisione())}, " \
                f"{round(self.getYMin(), gcPunto.getPrecisione())}, " \
                f"{round(self.getYMax(), gcPunto.getPrecisione())})"
        return s

    # restituisce la rappresentazione bounding box come stringa col metodo speciale __repr__
    # che viene implicitamente utilizzata nelle altre classi
    def __repr__(self):
        """ restituisce il bounding box in formato stringa per le altre implementazioni
            (ad esempio per l'utilizzo in altre classi)
        """
        return str(self)

    # ------------------------------------------------------------------------------------

    # restituisce la larghezza del bounding box
    def larghezza(self):
        """ restituisce la larghezza del bounding box corrente
        """
        return self.__xmax - self.__xmin

    # restituisce l'altezza del bounding box
    def altezza(self):
        """ restituisce l'altezza del bounding box corrente
        """
        return self.__ymax - self.__ymin

    # restituisce l'area del bounding box
    def area(self):
        """ restituisce l'area del bounding box corrente
        """
        return self.larghezza()*self.altezza()

    # restituisce il bounding box sotto forma di poligono
    def toPoligono(self):
        """ restituisce il poligono corrispondente al bounding box corrente
        """
        pol = gcPoligono()
        pol.aggiungi(gcPunto(self.__xmin, self.__ymin))
        pol.aggiungi(gcPunto(self.__xmax, self.__ymin))
        pol.aggiungi(gcPunto(self.__xmax, self.__ymax))
        pol.aggiungi(gcPunto(self.__xmin, self.__ymax))
        return pol

    #----------------------------------------------------------------------------------------

    # restituisce True se il punto si trova all'interno del bounding box
    def contienePunto(self, p):
        """ test di appartenenza di un punto al bounding box corrente
            (include il bordo sinistro e inferiore ma esclude il bordo destro e superiore)
        """
        (xmin, xmax, ymin, ymax) = self.get()   # estrae le coordinate del bounding box corrente
        (x, y) = p.get()      # estrae le coordinate del punto come tupla (coppia)
        return xmin <= x < xmax and ymin <= y < ymax


    # restituisce l'intersezione (eventualmente vuota) tra il bounding box corrente
    # e quello passato come parametro
    # se l'intersezione è vuota restituisce None
    def intersezione(self, bb):
        """ restituisce l'intersezione (eventualmente vuota) tra il bounding box corrente
            e quello passato come parametro
        """
        (xmin, xmax, ymin, ymax) = self.get()   # estrae le coordinate dei due bounding box
        (xmin2, xmax2, ymin2, ymax2) = bb.get()
        # determina le coordinate del bounding box intersezione (eventualmente vuoto se sono disgiunti)
        xmin = max(xmin, xmin2)
        xmax = min(xmax, xmax2)
        ymin = max(ymin, ymin2)
        ymax = min(ymax, ymax2)
        if xmin <= xmax and ymin <= ymax :
            bbintersez = gcBoundingBox([xmin, xmax, ymin, ymax])
            return bbintersez
        else:
            return None

    # restituisce True se il bounding box corrente interseca quello passato come parametro
    # escludendo il bordo destro ed il bordo superiore verificando le condizioni:
    # max(xmin1, xmin2)<=min(xmax1, xmax2)  e  max(ymin1, ymin2)<=min(ymax1, ymax2)
    def interseca(self, bb):
        """ test di intersezione tra il bounding box corrente interseca quello passato come parametro
        """
        #---------------------- versione alternativa --------------------
        # # anziché ricorrere alla verifica delle condizioni:
        # # max(xmin, xmin2)<=min(xmax, xmax2)  e  max(ymin, ymin2)<=min(ymax, ymax2)
        # # per comodità si richiama il metodo intersezione e si controlla se restituisce
        # # un bounding box valido oppure il valore None che corrisponde a una intersezione vuota
        # intersez = self.intersezione(bb) != None
        # return intersez
        (xmin, xmax, ymin, ymax) = self.get()   # estrae le coordinate dei due bounding box
        (xmin2, xmax2, ymin2, ymax2) = bb.get()
        intersez = max(xmin, xmin2)<=min(xmax, xmax2) and max(ymin, ymin2)<=min(ymax, ymax2)
        return intersez

#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

class gcBoundingDiamond:
    """ classe di geometria computazionale in Python
        che definisce i bounding diamond nel piano ed i relativi metodi primitivi
        autore: Giorgio Nordo - Dipartimento MIFT Università di Messina
        www.nordo.it   |  giorgio.nordo@unime.it """


    # costruttore del bounding diamond di un oggetto di tipo punto, segmento
    # lista di punti, poligono, oggetto bounding diamond
    # o direttamente come tupla (quadrupla) delle coordinate estremali
    # memorizzando le coordinate estremali
    def __init__(self, lv=None):
        """ crea il bounding diamon di un oggetto di tipo punto, segmento, triangolo
            lista di punti o poligono o anche come oggetto bounding diamond
            o direttamente come tupla (quadrupla) dei parametri estremali
        """
        elaboraPunti = True     # flag per indicare se occorre trasformare i punti in parametri
        #-----------------------------------------------------
        if type(lv) == gcPunto:               # se il parametro ricevuto è un punto
            lista = gcListaPunti([lv])
        #------------------------------------------------------------------------
        elif type(lv) == gcSegmento:          # se il parametro ricevuto è un segmento
            lista = gcListaPunti([lv.getInizio(), lv.getFine()])
        #------------------------------------------------------------------------
        elif type(lv) == gcTriangolo:         # se il parametro ricevuto è un triangolo
            lista = gcListaPunti([lv[1], lv[2], lv[3]])
        #------------------------------------------------------------------------
        elif type(lv) == gcListaPunti:        # se il parametro ricevuto è una lista di punti
            lista = lv
        #------------------------------------------------------------------------
        elif type(lv) == gcPoligono:          # se il parametro ricevuto è un poligono
            lista = lv
        #------------------------------------------------------
        elif type(lv) == gcBoundingDiamond:   # se il parametro ricevuto è un bounding diamond
            elaboraPunti = False    # memorizza direttamente le proprietà nell'oggetto
            (pmin, pmax, ppmin, ppmax) = lv.get()
            self.__pmin = pmin
            self.__pmax = pmax
            self.__ppmin = ppmin
            self.__ppmax = ppmax
        #-----------------------------------------------------
        elif type(lv) in (list, tuple):    # se il parametro ricevuto è una lista o una tupla
            if len(lv) == 4:          # verifica che ci siano quattro elementi nella tupla
                elaboraPunti = False    # memorizza direttamente le proprietà nell'oggetto
                self.__pmin = lv[0]
                self.__pmax = lv[1]
                self.__ppmin = lv[2]
                self.__ppmax = lv[3]
        #-----------------------------------------------------
        else:   # in tutti gli altri casi assegna una lista di punti vuota
            lista = None
        #--------------------------------------------------------------
        # esegue (se necessario) la trasformazione dei punti in parametri
        if elaboraPunti == True :
            # determina i punti estremali
            Pmin = lista.minimo(gcPunto.primaBisettrice)
            Pmax = lista.massimo(gcPunto.primaBisettrice)
            PPmin = lista.minimo(gcPunto.secondaBisettrice)
            PPmax = lista.massimo(gcPunto.secondaBisettrice)
            # memorizza le proprietà nell'oggetto
            self.__pmin = Pmin.getx() - Pmin.gety()
            self.__pmax = Pmax.getx() - Pmax.gety()
            self.__ppmin = PPmin.getx() + PPmin.gety()
            self.__ppmax = PPmax.getx() + PPmax.gety()


    # restituisce il bounding diamond sotto forma di tupla
    def get(self):
        """ restituisce la tupla dei parametri del bounding diamond corrente
        """
        t = (self.__pmin, self.__pmax, self.__ppmin, self.__ppmax)
        return t

    # restituisce il valore pmin
    def getPMin(self):
        """ restituisce il valore xmin
        """
        return self.__pmin

    # restituisce il valore pmax
    def getPMax(self):
        """ restituisce il valore pmax
        """
        return self.__pmax

    # restituisce il valore ppmin
    def getPPMin(self):
        """ restituisce il valore ppmin
        """
        return self.__ppmin

    # restituisce il valore ppmax
    def getPPMax(self):
        """ restituisce il valore ppmax
        """
        return self.__ppmax

    # ------------------------------------------------------------------------------------

    # restituisce il bounding diamond come stringa
    # col metodo speciale __str__
    def __str__(self):
        """ restituisce il bounding diamond in formato stringa
        """
        if self.__pmin == None:
            s = ''
        else:
            s = f"BD({round(self.getPMin(), gcPunto.getPrecisione())}, " \
                f"{round(self.getPMax(), gcPunto.getPrecisione())}, " \
                f"{round(self.getPPMin(), gcPunto.getPrecisione())}, " \
                f"{round(self.getPPMax(), gcPunto.getPrecisione())})"
        return s

    # restituisce la rappresentazione bounding diamond come stringa col metodo speciale __repr__
    # che viene implicitamente utilizzata nelle altre classi
    def __repr__(self):
        """ restituisce il bounding diamond in formato stringa per le altre implementazioni
            (ad esempio per l'utilizzo in altre classi)
        """
        return str(self)

    # ------------------------------------------------------------------------------------

    # restituisce il bounding diamond sotto forma di poligono
    def toPoligono(self):
        """ restituisce il poligono corrispondente al bounding diamond corrente
        """
        (pmin, pmax, ppmin, ppmax) = self.get()
        pol = gcPoligono()
        D1 = gcPunto((ppmin + pmin) / 2, (ppmin - pmin) / 2)
        D2 = gcPunto((ppmin + pmax) / 2, (ppmin - pmax) / 2)
        D3 = gcPunto((ppmax + pmax) / 2, (ppmax - pmax) / 2)
        D4 = gcPunto((ppmax + pmin) / 2, (ppmax - pmin) / 2)
        pol.aggiungi(D1)
        pol.aggiungi(D2)
        pol.aggiungi(D3)
        pol.aggiungi(D4)
        return pol

    #----------------------------------------------------------------------------------------

    # restituisce True se il punto si trova all'interno del bounding diamond
    def contienePunto(self, p):
        """ test di appartenenza di un punto al bounding diamond corrente
            (include il bordo sinistro e inferiore ma esclude il bordo destro e superiore)
        """
        (pmin, pmax, ppmin, ppmax) = self.get()
        (x, y) = p.get()      # estrae le coordinate del punto come tupla (coppia)
        return pmin <= x-y < pmax and ppmin <= x+y < ppmax


    # restituisce l'intersezione (eventualmente vuota) tra il bounding diamond corrente
    # e quello passato come parametro
    # se l'intersezione è vuota restituisce None
    def intersezione(self, bd):
        """ restituisce l'intersezione (eventualmente vuota) tra il bounding box corrente
            e quello passato come parametro
        """
        (pmin, pmax, ppmin, ppmax) = self.get()
        (qmin, qmax, qpmin, qpmax) = bd.get()
        imin = max(pmin, qmin)
        imax = min(pmax, qmax)
        ipmin = max(ppmin, qpmin)
        ipmax = min(ppmax, qpmax)
        bd_intersez = gcBoundingDiamond([imin, imax, ipmin, ipmax])
        return bd_intersez
        #---------------------- versione alternativa --------------------
        # pol1 = self.toPoligono()
        # pol2 = bd.toPoligono()
        # pol_intersez = pol1.intersezionePoligoniConvessi(pol2)
        # if pol_intersez.lunghezza() > 0:
        #     bd_intersez = gcBoundingDiamond(pol_intersez)
        #     return bd_intersez
        # else:
        #     return None

    # restituisce True se il bounding diamond corrente interseca quello passato come parametro
    # escludendo il bordo destro ed il bordo superiore verificando le condizioni:
    #     max(pmin, pmin2)<=min(pmax, pmax2)  e  max(ppmin, ppmin2)<=min(ppmax, ppmax2)
    def interseca(self, bd):
        """ test di intersezione tra il bounding box corrente interseca quello passato come parametro
        """
        # intersez = self.intersezione(bd) != None
        (pmin, pmax, ppmin, ppmax) = self.get()
        (pmin2, pmax2, ppmin2, ppmax2) = bd.get()
        intersez = max(pmin, pmin2) <= min(pmax, pmax2) and max(ppmin, ppmin2) <= min(ppmax, ppmax2)
        return intersez

#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------


class gcBoundingOctagon:
    """ classe di geometria computazionale in Python
        che definisce i bounding octagon nel piano ed i relativi metodi primitivi
        autore: Giorgio Nordo - Dipartimento MIFT Università di Messina
        www.nordo.it   |  giorgio.nordo@unime.it """

    # costruttore del bounding box di un oggetto di tipo punto, segmento
    # lista di punti, poligono, oggetto bounding octagon
    # o direttamente come tupla (quadrupla) delle coordinate estremali
    # memorizzando le coordinate estremali
    def __init__(self, lv=None):
        """ crea il bounding octagon di un oggetto di tipo segmento, triangolo
            lista di punti,poligono o anche come oggetto bounding box
            o direttamente come tupla (ottupla) dei parametri estremali
        """
        elaboraPunti = True     # flag per indicare se occorre trasformare i punti in parametri
        #-----------------------------------------------------
        if type(lv) == gcPunto:               # se il parametro ricevuto è un punto
            lista = gcListaPunti([lv])
        #------------------------------------------------------------------------
        elif type(lv) == gcSegmento:          # se il parametro ricevuto è un segmento
            lista = gcListaPunti([lv.getInizio(), lv.getFine()])
        #------------------------------------------------------------------------
        elif type(lv) == gcTriangolo:         # se il parametro ricevuto è un triangolo
            lista = gcListaPunti([lv[1], lv[2], lv[3]])
        #------------------------------------------------------------------------
        elif type(lv) == gcListaPunti:        # se il parametro ricevuto è una lista di punti
            lista = lv
        #------------------------------------------------------------------------
        elif type(lv) == gcPoligono:          # se il parametro ricevuto è un poligono
            lista = lv
        #------------------------------------------------------
        elif type(lv) == gcBoundingOctagon:   # se il parametro ricevuto è un bounding diamond
            elaboraPunti = False    # memorizza direttamente le proprietà nell'oggetto
            (xmin, xmax, ymin, ymax, pmin, pmax, ppmin, ppmax) = self.get()
            self.__xmin = xmin
            self.__xmax = xmax
            self.__ymin = ymin
            self.__ymax = ymax
            self.__pmin = pmin
            self.__pmax = pmax
            self.__ppmin = ppmin
            self.__ppmax = ppmax
        #-----------------------------------------------------
        elif type(lv) in (list, tuple):    # se il parametro ricevuto è una lista o una tupla
            if len(lv) == 8:          # verifica che ci siano otto elementi nella tupla
                elaboraPunti = False    # memorizza direttamente le proprietà nell'oggetto
                self.__xmin = lv[0]
                self.__xmax = lv[1]
                self.__ymin = lv[2]
                self.__ymax = lv[3]
                self.__pmin = lv[4]
                self.__pmax = lv[5]
                self.__ppmin = lv[6]
                self.__ppmax = lv[7]
        #-----------------------------------------------------
        else:   # in tutti gli altri casi assegna una lista di punti vuota
            lista = None
        #--------------------------------------------------------------
        # esegue (se necessario) la trasformazione dei punti in parametri
        if elaboraPunti == True :
            bb = gcBoundingBox(lv)        # genera il bounding box
            param_bb = bb.get()           # ottiene la tupla dei 4 parametri del bounding box
            bd = gcBoundingDiamond(lv)    # genera il bounding diamond
            param_bd = bd.get()           # ottiene la tupla dei 4 parametri del bounding diamond
            # memorizza le proprietà nell'oggetto
            self.__xmin = param_bb[0]
            self.__xmax = param_bb[1]
            self.__ymin = param_bb[2]
            self.__ymax = param_bb[3]
            self.__pmin = param_bd[0]
            self.__pmax = param_bd[1]
            self.__ppmin = param_bd[2]
            self.__ppmax = param_bd[3]

    # restituisce il bounding octagon sotto forma di tupla
    def get(self):
        """ restituisce la tupla dei parametri del bounding octagon corrente
        """
        t = (self.__xmin, self.__xmax, self.__ymin, self.__ymax, self.__pmin, self.__pmax, self.__ppmin, self.__ppmax)
        return t


    # restituisce il valore xmin
    def getXMin(self):
        """ restituisce il valore xmin
        """
        return self.__xmin

    # restituisce il valore xmax
    def getXMax(self):
        """ restituisce il valore xmax
        """
        return self.__xmax

    # restituisce il valore ymin
    def getYMin(self):
        """ restituisce il valore ymin
        """
        return self.__ymin

    # restituisce il valore ymax
    def getYMax(self):
        """ restituisce il valore ymax
        """
        return self.__ymax

    # restituisce il valore pmin
    def getPMin(self):
        """ restituisce il valore xmin
        """
        return self.__pmin

    # restituisce il valore pmax
    def getPMax(self):
        """ restituisce il valore pmax
        """
        return self.__pmax

    # restituisce il valore ppmin
    def getPPMin(self):
        """ restituisce il valore ppmin
        """
        return self.__ppmin

    # restituisce il valore ppmax
    def getPPMax(self):
        """ restituisce il valore ppmax
        """
        return self.__ppmax

    # ------------------------------------------------------------------------------------

    # restituisce il bounding octagon come stringa
    # col metodo speciale __str__
    def __str__(self):
        """ restituisce il bounding octagon in formato stringa
        """
        if self.__pmin == None:
            s = ''
        else:
            s = f"BO({round(self.getXMin(), gcPunto.getPrecisione())}, " \
                f"{round(self.getXMax(), gcPunto.getPrecisione())}, "    \
                f"{round(self.getYMin(), gcPunto.getPrecisione())}, "    \
                f"{round(self.getYMax(), gcPunto.getPrecisione())}, "    \
                f"{round(self.getPMin(), gcPunto.getPrecisione())}, "    \
                f"{round(self.getPMax(), gcPunto.getPrecisione())}, "    \
                f"{round(self.getPPMin(), gcPunto.getPrecisione())}, "   \
                f"{round(self.getPPMax(), gcPunto.getPrecisione())})"
        return s

    # restituisce la rappresentazione bounding octagon come stringa col metodo speciale __repr__
    # che viene implicitamente utilizzata nelle altre classi
    def __repr__(self):
        """ restituisce il bounding octagon in formato stringa per le altre implementazioni
            (ad esempio per l'utilizzo in altre classi)
        """
        return str(self)

    # ------------------------------------------------------------------------------------

    # restituisce il bounding octagon sotto forma di poligono
    def toPoligono(self):
        """ restituisce il poligono corrispondente al bounding octagon corrente
        """
        (xmin, xmax, ymin, ymax, pmin, pmax, ppmin, ppmax) = self.get()   # estrae i parametri del bounding octagon
        bb = gcBoundingBox([xmin, xmax, ymin, ymax])        # crea un bounding box con i parametri
        bd = gcBoundingDiamond([pmin, pmax, ppmin, ppmax])  # crea un bounding diamond con i parametri
        pol_bb = bb.toPoligono()
        pol_bd = bd.toPoligono()
        pol_bo = pol_bb.intersezionePoligoniConvessi(pol_bd)
        pol_bo.semplifica()   # elimina eventual vertici ripetuti
        return pol_bo

    #----------------------------------------------------------------------------------------

    # restituisce True se il punto si trova all'interno del bounding octagon
    def contienePunto(self, p):
        """ test di appartenenza di un punto al bounding otatgon corrente
            (include i bordi sinistri e inferiore ma esclude il bordo destro e superiore)
        """
        (xmin, xmax, ymin, ymax, pmin, pmax, ppmin, ppmax) = self.get()   # estrae i parametri del bounding octagon
        bb = gcBoundingBox([xmin, xmax, ymin, ymax])        # crea un bounding box con i parametri
        bd = gcBoundingDiamond([pmin, pmax, ppmin, ppmax])  # crea un bounding diamond con i parametri
        return bb.contienePunto(p) and bd.contienePunto(p)

    # restituisce l'intersezione (eventualmente vuota) tra il bounding octagon corrente
    # e quello passato come parametro
    # se l'intersezione è vuota restituisce None
    def intersezione(self, bo):
        """ restituisce l'intersezione (eventualmente vuota) tra il bounding octagon corrente
            e quello passato come parametro
        """
        (xmin, xmax, ymin, ymax, pmin, pmax, ppmin, ppmax) = self.get()
        (xmin2, xmax2, ymin2, ymax2, pmin2, pmax2, ppmin2, ppmax2) = bo.get()
        bb = gcBoundingBox([xmin, xmax, ymin, ymax])
        bb2 = gcBoundingBox([xmin2, xmax2, ymin2, ymax2])
        bd = gcBoundingDiamond([pmin, pmax, ppmin, ppmax])
        bd2 = gcBoundingDiamond([pmin2, pmax2, ppmin2, ppmax2])
        ibb = bb.intersezione(bb2)
        ibd = bd.intersezione(bd2)
        (ixmin, ixmax, iymin, iymax) = ibb.get()
        (ipmin, ipmax, ippmin, ippmax) = ibd.get()
        bo_intersez = gcBoundingOctagon([ixmin, ixmax, iymin, iymax, ipmin, ipmax, ippmin, ippmax])
        return bo_intersez
        #---------------------- versione alternativa --------------------
        # pol1 = self.toPoligono()
        # pol2 = bo.toPoligono()
        # pol_intersez = pol1.intersezionePoligoniConvessi(pol2)
        # if pol_intersez.lunghezza() > 0:
        #     bo_intersez = gcBoundingOctagon(pol_intersez)
        #     return bo_intersez
        # else:
        #     return None



    # restituisce True se il bounding diamond corrente interseca quello passato come parametro
    # escludendo il bordo destro ed il bordo superiore
    # richiamando il metodo intersezione e controllando se restituisce
    # un diamond box valido oppure il valore None che corrisponde a una intersezione vuota
    def interseca(self, bo):
        """ test di intersezione tra il bounding box corrente interseca quello passato come parametro
        """
        intersez = self.intersezione(bo) != None
        return intersez
