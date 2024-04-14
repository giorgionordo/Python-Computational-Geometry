from pygc.punto import gcPunto
from pygc.segmento import gcSegmento
from pygc.listapunti import gcListaPunti
from pygc.poligono import gcPoligono
from pygc.boundingcontainer import *
import matplotlib.pyplot as plt
import seaborn   # pacchetto che aggiunge uno stile più moderno nella resa grafica
seaborn.set()    # avvia l'interfaccia grafica di seaborn


class gcSemipianoSinistro:
    """ classe di geometria computazionale in Python
        che definisce i semipiani sinistri nel piano ed i relativi metodi primitivi
        autore: Giorgio Nordo - Dipartimento MIFT Università di Messina
        www.nordo.it   |  giorgio.nordo@unime.it """


    # metodo costruttore che restituisce il semipiano sinistro rispetto a una retta individuata
    # da un segmento incapsulandolo in un bounding box quadrato [-lmt,lmt]x[-lmt,lmt] definito dal parametro lmt
    def __init__(self, segm, lmt):
        """ restituisce il semipiano sinistro rispetto alla retta individuata
            da un segmento incapsulandolo in un bounding box quadrato definito dal parametro lmt
        """
        # memorizza il segmento e la limitazione numerica come proprietà dell'oggetto
        self.__segmento = segm
        self.__limitazione = lmt
        # costruisce il poligono corrispondente al bounding box di estremi -/+ lmt
        bb = gcBoundingBox([-lmt, lmt, -lmt, lmt])
        bb_pol = bb.toPoligono()
        # intersezione tra poligono e retta
        intersezioni_retta = bb_pol.puntiIntersezioneRetta(segm)
        # ordina i punti di intersezione
        intersezioni_retta = intersezioni_retta.ordina(ordinamento=gcPunto.lessicograficoVerticale)
        # se ci sono più di due intersezioni (dovuti ai prolungamenti delle rette)
        # considera solo quelli più vicini eliminando i due punti estremi
        if intersezioni_retta.lunghezza() > 2:
            intersezioni_retta.elimina(-1)
            intersezioni_retta.elimina()
        # crea la retta (segmento sul bounding box)
        retta = gcSegmento(intersezioni_retta[0], intersezioni_retta[1])
        # orienta la retta nello stesso verso del segmento dato
        if segm.verso() != retta.verso():
            retta.inverti()
        # memorizza la retta come proprietà dell'oggetto
        self.__retta = retta
        # crea il poligno che rappresenta il semipiano con i primi due punti di intersezione
        semipiano_sinistro = gcPoligono(retta)
        # prepara i punti del bounding box orientati in verso antiorario
        p0 = gcPunto(-lmt, -lmt)    # p3 ----- p2
        p1 = gcPunto(lmt, -lmt)     # :        :
        p2 = gcPunto(lmt, lmt)      # :        :
        p3 = gcPunto(-lmt, lmt)     # p0 ----- p1

        # classifica la posizione dell'intersezione per aggiungere
        # al poligono che rappresenta il semipiano uno o due punti
        # della frontiera del bounding box
        (p_i, p_f) = (retta.getInizio(), retta.getFine())
        (x_i, y_i, x_f, y_f) = (p_i.getx(), p_i.gety(), p_f.getx(), p_f.gety())

        # ------------- retta verticale verso l'alto
        if y_i == -lmt and y_f == lmt:
            semipiano_sinistro.aggiungi(p3)  # aggiungo 3-0
            semipiano_sinistro.aggiungi(p0)
        # ------------- retta verticale verso il basso
        elif y_i == lmt and y_f == -lmt:
            semipiano_sinistro.aggiungi(p1)  # aggiungo 1-2
            semipiano_sinistro.aggiungi(p2)
        # ------------- retta orizzontale verso l'alto
        elif x_i == -lmt and x_f == lmt:
            semipiano_sinistro.aggiungi(p2)  # aggiungo 2-3
            semipiano_sinistro.aggiungi(p3)
        # ------------- retta orizzontale verso il basso
        elif x_i == lmt and x_f == -lmt:
            semipiano_sinistro.aggiungi(p0)  # aggiungo 0-1
            semipiano_sinistro.aggiungi(p1)

        # ------------- retta diagonale verso l'alto su spigolo 0
        elif x_i == -lmt and y_f == -lmt:
            semipiano_sinistro.aggiungi(p1)  # aggiungo 1-2-3
            semipiano_sinistro.aggiungi(p2)
            semipiano_sinistro.aggiungi(p3)
        # ------------- retta diagonale verso il basso su spigolo 0
        elif y_i == -lmt and x_f == -lmt:
            semipiano_sinistro.inserisci(1, p0)  # metto in mezzo 0

        # ------------- retta diagonale verso l'alto su spigolo 1
        elif y_i == -lmt and x_f == lmt:
            semipiano_sinistro.aggiungi(p2)  # aggiungo 2-3-0
            semipiano_sinistro.aggiungi(p3)
            semipiano_sinistro.aggiungi(p0)
        # ------------- retta diagonale verso il basso su spigolo 1
        elif x_i == lmt and y_f == -lmt:
            semipiano_sinistro.inserisci(1, p1)  # metto in mezzo 1

        # ------------- retta diagonale verso l'alto su spigolo 2
        elif x_i == lmt and y_f == lmt:
            semipiano_sinistro.aggiungi(p3)  # aggiungo 3-0-1
            semipiano_sinistro.aggiungi(p0)
            semipiano_sinistro.aggiungi(p1)
        # ------------- retta diagonale verso il basso su spigolo 2
        elif y_i == lmt and x_f == lmt:
            semipiano_sinistro.inserisci(1, p2)  # metto in mezzo 2

        # ------------- retta diagonale verso il basso su spigolo 3
        elif y_i == lmt and x_f == -lmt:
            semipiano_sinistro.aggiungi(p0)  # aggiungo 0-1-2
            semipiano_sinistro.aggiungi(p1)
            semipiano_sinistro.aggiungi(p2)
        # ------------- retta diagonale verso l'alto su spigolo 3
        elif x_i == -lmt and y_f == lmt:
            semipiano_sinistro.inserisci(1, p3)  # metto in mezzo 3
        self.__semipiano_sinistro = gcPoligono(semipiano_sinistro)


    # ------------------------------------------------------------------------------------

    # restituisce il semipiano sinistro come stringa individuata dalla retta
    # col metodo speciale __str__
    def __str__(self):
        """ restituisce il semipiano in formato stringa come retta
        """
        s= f"S_sx({self.toPoligono()})"
        return s

    # restituisce la rappresentazione semipiano sinistro come stringa col metodo speciale __repr__
    # che viene implicitamente utilizzata nelle altre classi
    def __repr__(self):
        """ restituisce il semipiano sinistro in formato stringa per le altre implementazioni
            (ad esempio per l'utilizzo in altre classi)
        """
        return str(self)

    # ------------------------------------------------------------------------------------

    # restituisce il segmento utilizzato per individuare il semipiano sinistro
    def getSegmento(self):
        """ restituisce il segmento utilizzato per individuare il semipiano corrente
        """
        return self.__segmento


    # restituisce la retta che individua il semipiano sinistro (come oggetto segmento)
    def getRetta(self):
        """ restituisce la retta che individua il semipiano corrente (come oggetto segmento
        """
        return self.__retta


    # restituisce la limitazione del bounding box fornito per rappresentare il semipiano sinsitro
    def getLimitazione(self):
        """ restituisce la limitazione del bounding box fornito per rappresentare il semipiano corrente
        """
        return self.__limitazione


    # restituisce il semipiano sotto forma di poligono incapsulato
    def toPoligono(self):
        """ restituisce il poligono corrispondente al semipiano
        """
        return self.__semipiano_sinistro


    # metodo statico che determina un valore adatto a delimitare un insieme di segmenti
    # fornito come lista in un bounding box quadrato e simmetrico
    # determinando il valore massimo tra le loro intersezioni
    @ staticmethod
    def getLimitazione(ls):
        l = gcListaPunti()
        # aggiungi gli estremi dei segmenti
        for s in ls:
            l.aggiungi(s.getInizio())
            l.aggiungi(s.getFine())
        # aggiungi tutte le intersezioni
        n = len(ls)
        for i in range(n-1):
            for j in range(i,n):
                p = ls[i].intersezioneRette(ls[j], rette=True)
                if p!= None:
                    l.aggiungi(p)
        (xmin, xmax, ymin, ymax) = (l.xMin(), l.xMax(), l.yMin(), l.yMax())
        lmt = max(abs(xmin), abs(xmax), abs(ymin), abs(ymax))
        lmt = int(lmt*1.2)
        return lmt


    # ------------------------------------------------------------------------------------

    # aggiunge il semipiano al grafico usando il modulo pyplot e richiamando il metodo plot dei poligoni
    def plot(self, tipo='>-', colore='', colore_vertice='orange', colore_lato='orange',
             autonumerazione=False, riempimento=True, colore_riempimento='yellow', trasparenza_riempimento=0.2):
        """ traccia il semipiano sul grafico
        """
        self.toPoligono().plot(tipo=tipo, colore=colore, riempimento=riempimento, colore_lato=colore_lato,
                               colore_vertice=colore_vertice, autonumerazione=autonumerazione,
                               colore_riempimento=colore_riempimento, trasparenza_riempimento=trasparenza_riempimento)
