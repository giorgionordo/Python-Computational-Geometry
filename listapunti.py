from pygc.punto import gcPunto
from pygc.segmento import gcSegmento
import matplotlib.pyplot as plt
import seaborn   # pacchetto che aggiunge uno stile più moderno nella resa grafica
seaborn.set()    # avvia l'interfaccia grafica di seaborn

class gcListaPunti:
    """ classe di geometria computazionale in Python
        che definisce le liste di punti del piano ed i relativi metodi primitivi
        utilizzando come contenitore gli oggetti poligono
        osia come classe figlio della classe gcPoligono
        autore: Giorgio Nordo - Dipartimento MIFT Università di Messina
        www.nordo.it   |  giorgio.nordo@unime.it """

    # costruttore di una lista di punti come oggetti di tipo punto, stringhe
    # o come copia di un oggetto lista di punti
    def __init__(self, lv=None):
        """ crea una list di punti del piano forniti come punti, stringhe
            o come copia di un altro oggetto poligono
        """
        if type(lv) == list:  # se il parametro ricevuto è una lista
            lunghezza = len(lv)  # costruisci il poligono come lista di punti
            if lunghezza > 0:
                self.__v = list()  # costruisci il poligono come lista di punti
                for i in range(lunghezza):
                    p = gcPunto(lv[i])  # converti il generico elemento in oggetto punto in caso sia una stringa
                    self.__v.append(p)  # aggiungilo alla lista di punti della classe
        #------------------------------------------------------------------------
        elif type(lv) == gcListaPunti:  # crea una copia della lista di punti come oggetto
            self.__v = list()
            for i in range(lv.lunghezza()):
                self.__v.append(lv[i])
        #------------------------------------------------------------------------
        else:  # in tutti gli altri casi (compreso quando lv è None) crea una lista vuota
            self.__v = list()

    # costruttore alternativo di una lista di punti da un file di testo
    # costituito da coppie di numeri separati da una virgola
    # eventualmente racchiusi tra parentesi e disposte su righe differenti
    @classmethod
    def fromFile(cls, nomefile):
        """ crea un oggetto lista punti leggendo l'elenco dei punti da un file di testo
        """
        cls.__v = list()
        with open(nomefile) as f:
            linee = f.readlines()
        listapunti = [gcPunto(l.rstrip()) for l in linee]
        return cls(listapunti)

    # restituisce l'i-esimo punto della lista come oggetto punto
    # estendendo l'operatore di indicizzazione col metodo speciale __getitem__
    # l'indice i può anche essere negativo (-1=ultimo, -2=penultimo, ecc.)
    def __getitem__(self, i):
        """ restituisce il punto di indice i della lista
        """
        if type(i) == int:  # se il parametro passato è un intero
            n = len(self.__v)
            if i >= 0 and i < n :
                return self.__v[i]
            elif i < 0 :
                return self.__v[i + n]
            else:
                return None
        elif type(i) == slice:  # se il parametro passato è di tipo slice(i,j,k)
            # recupera i valori degli indici dello slice
            # per restituire lo slice della lista __v
            return gcListaPunti(self.__v[i.start: i.stop: i.step])

    # metodo che restituisce l'i-esimo punto della lista
    def punto(self, i):
        """ restituisce il punto di indice i
        """
        return self[i]  # utilizza l'overload di __getitem__ per gcPUnto definito sopra

    # restituisce la lista di punti come stringa costituita da un elenco di punti
    # col metodo speciale __str__
    def __str__(self):
        """ restituisce la lista di punti in formato stringa come elenco dei suoi vertici
        """
        if len(self.__v) == 0:
            s = ''
        else:
            listapuntistringa = [str(p) for p in self.__v]
            s = "[ " + ", ".join(listapuntistringa) + " ]"
        return s

    # restituisce la rappresentazione lista punti come stringa col metodo speciale __repr__
    # che viene implicitamente utilizzata nelle altre classi
    def __repr__(self):
        """ restituisce la lista di punti in formato stringa per le altre implementazioni
            (ad esempio per l'utilizzo in altre classi)
        """
        return str(self)

    #------------------------------------------------------------------------------------

    # confronta due liste di punti (con una certa approssimazione)
    # sovraccaricando l'operatore di uguaglianza ==
    # col metodo speciale __eq__
    def __eq__(self, pl):
        """ confronta due liste di punti con l'uguale con approssimazione data da _TOLLERANZA
        """
        if pl == None:
            return False
        n = self.lunghezza()
        if len(pl) != n:   # se le due liste hanno lunghezze diverse sono certamente differenti
            return False
        else :
            uguali = True
            for i in range(n) :
                if self[i] != pl[i] :
                    uguali = False
            return uguali

    # confronta due liste di punti (con una certa approssimazione)
    # sovraccaricando l'operatore di uguaglianza !=
    # col metodo speciale __ne__
    def __ne__(self, pl):
        """ confronta due liste di punti col diverso con approssimazione data da _TOLLERANZA
        """
        differenti = not (self == pl)
        return differenti

    #------------------------------------------------------------------------------------
    # restituisce la lunghezza (il numero dei punti) della lista
    # col metodo speciale __len__ che sovrascrive la funzione len()
    def __len__(self):
        """ lunghezza (ovvero numero dei punti) della lista
        """
        return len(self.__v)

    # restituisce la lunghezza (il numero dei punti) della lista
    def lunghezza(self):
        """ lunghezza (ovvero numero dei punti) della lista
        """
        return len(self.__v)

    #--------------------------------------------------------------------------

    # restituisce l'ascissa di valore minimo della lista di punti
    def xMin(self):
        """ minima ascissa della lista di punti
        """
        if len(self.__v) > 0 :
            m = min(p.getx() for p in self.__v)
            return m

    # restituisce l'ascissa di valore massimo della lista di punti
    def xMax(self):
        """ massima ascissa della lista di punti
        """
        if len(self.__v) > 0 :
            m = max(p.getx() for p in self.__v)
            return m

    # restituisce l'ordinata di valore minimo della lista di punti
    def yMin(self):
        """ minima ordinata della lista di punti
        """
        if len(self.__v) > 0 :
            m = min(p.gety() for p in self.__v)
            return m

    # restituisce l'ordinata di valore massimo della lista di punti
    def yMax(self):
        """ massima ordinata della lista di punti
        """
        if len(self.__v) > 0 :
            m = max(p.gety() for p in self.__v)
            return m

    # --------------------------------------------------------------------------

    # cancella la lista di punti eliminando tutti i suoi elementi
    def cancella(self):
        """ cancella la lista eliminando tutti i suoi punti
        """
        self.__v = list()

    # aggiunge un punto in coda alla lista
    # sia che venga passato come oggetto di tipo gcPunto
    # sia che venga passato come stringa (nel qual caso viene prima convertito)
    def aggiungi(self, p):
        """ aggiunge un vertice alla lista passandolo indifferentemente
            come punto oppure come stringa
        """
        p = gcPunto(p)  # converti il parametro in oggetto punto in caso sia una stringa
        self.__v.append(p)

    # inserisce un punto in una determinata posizione (indice) della lista
    # sia che venga passato come oggetto di tipo gcPunto
    # sia che venga passato come stringa (nel qual caso viene prima convertito)
    def inserisci(self, i, p):
        """ inserisce un vertice p nella posizione i della lista
            passandolo indifferentemente come punto oppure come stringa
        """
        p = gcPunto(p)  # converti il parametro in oggetto punto in caso sia una stringa
        # if i >= 0 and i < self.lunghezza():
        self.__v.insert(i, p)

    # estrae restituendolo il vertice di indice i ed eliminandolo dalla lista
    # se l'indice viene omesso viene estratto il primo punto (quello di indice 0)
    def estrai(self, i=0):
        """ estrae il vertice di indice i e lo rimuove dalla lista
        """
        if i >= 0 and i < self.lunghezza():
            pp = self.__v.pop(i)
            return pp

    # elimina un punto in una determinata posizione (indice, anche negativo) del poligono
    def elimina(self, i=0):
        """ elimina il punto di indice i della lista
        """
        if i < self.lunghezza():
            self.__v.pop(i)

    # restituisce True se la lista contiene un punto
    # sia che venga passato come oggetto di tipo gcPunto
    # sia che venga passato come stringa (nel qual caso viene prima convertito)
    def haPunto(self, p):
        """ verifica se il punto p appartiene alla lista
        """
        if p == None :     # se il punto è nullo certamente non appartiene alla lista
            return False
        if self.lunghezza() > 0:
            p = gcPunto(p)  # converti il parametro in oggetto punto in caso sia una stringa
            hapt = p in self.__v
            return hapt
        else:  # se la lista è vuoto (cioè se ha lunghezza 0) è falso che il punto p vi appartiene
            return False

    # restituisce True se il punto appartiene alla lista di punti
    # col metodo speciale __contains__ che sovrascrive l'operatore in
    # sia che venga passato come oggetto di tipo gcPunto o come stringa
    # richiamando il metodo haPunto
    def __contains__(self, p):
        """ verifica se il punto p appartiene alla lista
        """
        return self.haPunto(p)

    # restituisce l'indice corrispondente al punto della lista passato come parametro
    # sia come oggetto di tipo gcPunto sia come stringa
    def indice(self, p):
        """ restituisce l'indice corrispondente ad un punto della lista """
        if self.lunghezza() > 0:
            p = gcPunto(p)  # converti il parametro in oggetto punto in caso sia una stringa
            if p in self.__v:
                indice = self.__v.index(p)
                return indice
            else:
                return None
        else:  # se la lista è vuoto (cioè se ha lunghezza 0) il punto non può appartenervi
            return None

    # rimuove un punto della lista passandone il valore
    # sia che venga passato come indice (nel qual caso si trova il punto corrispondente)
    # oppure come oggetto di tipo gcPunto
    # o ancora che venga passato come stringa (nel qual caso viene prima convertito)
    # ATTENZIONE: viene rimossa solo la prima occorrenza del punto
    # giacché nella lista lo stesso punto potrebbe essere presente altre volte
    def rimuovi(self, p):
        """ rimuovi il punto della lista passandone il valore
        """
        if type(p) == int:   # se è stato passato un intero trovo il punto di indice corrispondente
            p = self.__v[p]
        else:
            p = gcPunto(p)   # converti il parametro in oggetto punto in caso sia una stringa
        if p in self.__v:
            self.__v.remove(p)

    #----------------------------------------------------------------------------------------

    # inverte la lista ordinando i punti in verso opposto
    def inverti(self):
        """ inverte l'ordine dei punti contenuti nella lista
        """
        self.__v.reverse()

    #----------------------------------------------------------------------------------------

    # definisce l'iteratore per l'oggetto lista di punti azzerando l'indice
    def __iter__(self):
        self.__i = 0   # inizializza l'indice privato __i da usare come contatore
        return self

    # restituisce il prossimo elemento iterato dell'oggetto lista di punti
    def __next__(self):
        if self.__i < len(self.__v):  # se l'indice __i non eccede la lunghezza della lista di punti
            pt = self.__v[self.__i]   # preleva il punto di indice __i
            self.__i +=1              # incremente il contatore privato __i
            return pt                 # e restituisce il punto
        raise StopIteration           # altrimenti interrompi l'iterazione


    # ----------------------------------------------------------------------------------------

    # metodo per estendere (accodare o concatenare) la lista punti corrente
    # con un'altra lista di punti passato come parametro
    def estendi(self, pol):
        """ estendi una lista di punti con un'altra lista passata come parametro
        """
        for p in pol :
            self.aggiungi(p)

    # restituisce la concatenzione di due poligoni sovraccaricando l'operatore di addizione +
    # col metodo speciale __add__
    def __add__(self, pol):
        """ concatenazione di due liste di punti
        """
        listaconcat = gcListaPunti(self)
        listaconcat.estendi(pol)
        return listaconcat

    # ----------------------------------------------------------------------------------------

    # restituisce come segmento il lato il cui estremo iniziale
    # è il punto di indice i (partendo dall'indice 0)
    def lato(self, i):
        """ restituisce il segmento tra il punto di indice i e quello successivo"""
        n = self.lunghezza()
        if i >= 0 and i < n:
            p1 = self[i]
            if i != n-1:
                p2 = self[i+1]
            else:
                p2 = self[0]
            s = gcSegmento(p1, p2)
            return s
        else:
            return None

    # ------------------------------------------------------------------------------------

    # elimina eventuali punti ripetuti
    def eliminaPuntiRipetuti(self):
        """ elimina eventuali punti ripetuti dalla lista
        """
        i = 0
        while i < self.lunghezza() - 1:
            j = i + 1
            while j < self.lunghezza():
                if self[i] == self[j]:
                    self.elimina(i)
                j += 1
            i += 1

    # ------------------------------------------------------------------------------------

    # restituisce il punto minimo rispetto ad una relazione di ordine di punti del piano
    # (lessicografico verticale o polare) passata come parametro
    def minimo(self, ordinamento=gcPunto.lessicograficoVerticale, polo=None):
        """ restituisce il punto minimo rispetto ad un dato ordinamento
        """
        n = self.lunghezza()
        if n > 0:
            mn = None
            for i in range(n):
                if mn is None or ordinamento(self[i], mn, polo):
                    mn = self[i]
            return mn
        else:
            return None

    # restituisce il punto massimo rispetto ad una relazione di ordine di punti del piano
    # (lessicografico verticale o polare) passata come parametro
    def massimo(self, ordinamento=gcPunto.lessicograficoVerticale, polo=None):
        """ restituisce il puntoe minimo rispetto ad un dato ordinamento
        """
        n = self.lunghezza()
        if n > 0:
            mx = None
            for i in range(n):
                if mx is None or ordinamento(mx, self[i], polo):
                    mx = self[i]
            return mx
        else:
            return None

    # ------------------------------------------------------------------------------------

    # calcola il baricentro geometrico della lista di punti corrente
    def baricentro(self):
        """ restituisce il baricentro geometrico della lista di punti corrente
            come oggetto punto
        """
        n = self.lunghezza()
        xb = sum([p.getx() for p in self]) / n
        yb = sum([p.gety() for p in self]) / n
        b = gcPunto(xb, yb)
        return b

    # ------------------------------------------------------------------------------------

    # funzione di ordinamento col mergesort
    # su una lista di punti rappresentata
    # rispetto ad una relazione di ordine di punti del piano (lessicografico verticale o polare)
    # passata come parametro
    def mergeSort(lista, ordinamento, polo):
        """ esegue l'ordinamento di una lista di punti col metodo del merge sort
        """
        if lista.lunghezza() > 1:
            medio = lista.lunghezza() // 2  # calcola l'indice intermedio
            sx = gcListaPunti(lista[:medio])  # dividi la lista in due sottoliste sinistra e destra
            dx = gcListaPunti(lista[medio:])
            # ordina ricorsivamente le due sottoliste
            gcListaPunti.mergeSort(sx, ordinamento, polo)
            gcListaPunti.mergeSort(dx, ordinamento, polo)
            # unisce la lista ricopiando i valori delle sottoliste
            lista.cancella()
            i = j = 0
            while i < sx.lunghezza() and j < dx.lunghezza():
                if ordinamento(sx[i], dx[j], polo):  # se sx[i]<=dx[j]
                    lista.aggiungi(sx[i])
                    i += 1
                else:
                    lista.aggiungi(dx[j])
                    j += 1
            # aggiunge eventuali elementi residui delle due sottoliste
            while i < sx.lunghezza():
                lista.aggiungi(sx[i])
                i += 1
            while j < dx.lunghezza():
                lista.aggiungi(dx[j])
                j += 1

    # ordina i vertici di una lista di punti rispetto a un dato ordinamento
    # (lessicografico verticale o polare)
    # e restituisce la lista di punti ordinata
    def ordina(self, ordinamento=gcPunto.lessicograficoVerticale, polo=None):
        """ restituisce la lista dei punti ordinata rispetto
            a un dato ordinamento (lessicografico verticale o polare)
        """
        listapunti = gcListaPunti(self)  # copia il poligono per non perdere l'originale
        gcListaPunti.mergeSort(listapunti, ordinamento, polo)  # richiama il merge sort sulla lista di punti
        # self.__init__(listapunti)   # memorizza la lista ordinata nell'oggetto corrente
        return listapunti  # restituisce la lista di punti ordinata


    # ------------------------------------------------------------------------------------

    # aggiunge i punti della lista al grafico usando il modulo pyplot
    # lati = True disegna i punti come semplice lista senza unire i segmenti
    def plot(self, tipo='o--', colore='', colore_punto='black', colore_lato='lighgray',
             autonumerazione=False, etichetta_vertici='P', colore_etichetta='', lati=False):
        """ traccia la lista di punti sul grafico
        """
        n = self.lunghezza()
        if n > 0:
            if colore != '':        # definisce il colore in blocco
                colore_punto = colore
                colore_lato = colore
            if colore_etichetta == '':
                colore_etichetta = colore_punto
            for i in range(n):
                if lati == True:  # disegna la linea spezzata (punti e lati)
                    s = self.lato(i)
                    s.plot(colore_segmento=colore_lato, colore_punto=colore_punto, tipo=tipo)
                    if autonumerazione == True:
                        p = gcPunto(self.__v[i])
                        p.plot(etichetta=f"${etichetta_vertici}_{{{i}}}$", colore=colore_punto, colore_etichetta=colore_etichetta)
                else:  # se lati=False disegna solo i punti (lista di punti)
                    p = gcPunto(self.__v[i])
                    if autonumerazione == True:
                        # le triple parentesi graffe servono per interpolare LaTeX dentro le f-string
                        p.plot(etichetta=f"${etichetta_vertici}_{{{i}}}$", colore=colore_punto, colore_etichetta=colore_etichetta)
                    else:
                        p.plot(colore=colore_punto)
