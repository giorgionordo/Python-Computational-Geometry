from pygc.punto import gcPunto
from pygc.segmento import gcSegmento
from pygc.listapunti import gcListaPunti
import matplotlib.pyplot as plt
import seaborn   # pacchetto che aggiunge uno stile più moderno nella resa grafica
seaborn.set()    # avvia l'interfaccia grafica di seaborn


class gcPoligono:
    """ classe di geometria computazionale in Python
        che definisce i poligoni nel piano ed i relativi metodi primitivi
        autore: Giorgio Nordo - Dipartimento MIFT Università di Messina
        www.nordo.it   |  giorgio.nordo@unime.it """

    # TODO: implementare la costruzione come lista di tuple di reali
    # costruttore di poligono piano come lista ordinata di vertici o di stringhe
    # o come copia di un oggetto poligono
    def __init__(self, lv=None):
        """ crea un poligono del piano come lista di punti, di stringhe
            di un oggetto listaPunti
            o come copia di un altro oggetto poligono
        """
        if type(lv) == list:        # se il parametro ricevuto è una lista
            lunghezza = len(lv)     # costruisci il poligono come lista di punti
            if lunghezza>0:
                self.__v = list()       # costruisci il poligono come lista di punti
                for i in range(lunghezza):
                    p = gcPunto(lv[i])  # converti il generico elemento in oggetto punto in caso sia una stringa
                    self.__v.append(p)  #aggiungilo alla lista di punti della classe
        #------------------------------------------------------------------------
        elif type(lv) in (gcPoligono, gcListaPunti) :  # crea una copia del poligono come oggetto o come lista di punti
            self.__v = list()
            for i in range(lv.lunghezza()):
                self.__v.append(lv[i])
        # ------------------------------------------------------------------------
        elif type(lv) == gcSegmento :  # costruisci il poligono con i due soli estremi iniziale e finale del segmento
            self.__v = list()
            self.__v.append(lv.getInizio())
            self.__v.append(lv.getFine())
        #------------------------------------------------------------------------
        else:   # in tutti gli altri casi (compreso quando lv è None) crea una lista di punti vuota
            self.__v = list()

    # costruttore alternativo di un poligono da un file di testo
    # costituito da coppie di numeri separati da una virgola
    # eventualmente racchiusi tra parentesi e disposte su righe differenti
    @classmethod
    def fromFile(cls, nomefile):
        """ crea un poligono leggendo l'elenco dei punti da un file di testo
        """
        cls.__v = list()
        with open(nomefile) as f:
            linee = f.readlines()
        listapunti = [gcPunto(l.rstrip()) for l in linee]
        return cls(listapunti)

    # restituisce il poligono come un oggetto lista di punti
    def toListaPunti(self):
        """ restituisce un oggetto lista di punti
        """
        lp = gcListaPunti()
        for i in range(len(self.__v)) :
            lp.aggiungi(self.__v[i])
        return lp

    # restituisce il vertice di indice i del poligono come oggetto punto
    # estendendo l'operatore di indicizzazione col metodo speciale __getitem__
    # l'indice si intende modulo la lunghezza n del poligono
    # per cui, detto 0 l'indice del primo vertice,
    # il vertice di indice n corrisponde a quello di indice 0 (il primo)
    # e il vertice di indice -1 corrisponde a quello di indice n-1 (l'ultimo)
    def __getitem__(self, i):
        """ restituisce il vertice di indice i (modulo la lunghezza del poligono)
            o lo slice
        """
        if type(i)==int:         # se il parametro passato è un intero
            n = len(self.__v)
            indice = i % n   # perche nei poligoni v_n = v_0 e v_{-1}=v_{n-1}
            return self.__v[indice]
        elif type(i) == slice:   # se il parametro passato è di tipo slice(i,j,k)
            # recupera i valori degli indici dello slice
            # per restituire lo slice della lista __v
            return gcPoligono(self.__v[i.start : i.stop : i.step])


    # metodo che restituisce il vertice di indice i del poligono
    def vertice(self, i):
        """ restituisce il vertice di indice i (anche negativo)
        """
        return self[i]   # utilizza l'overload di __getitem__ per gcPUnto definito sopra


    # restituisce il vertice precedente a quello passato
    # come oggetto di tipo gcPunto o come stringa
    def verticePrecedente(self, p):
        """ restituisce il vertice successivo a quello passato come punto
        """
        p = gcPunto(p)  # converti il parametro in oggetto punto in caso sia una stringa
        if p in self.__v:
            indice = self.__v.index(p)
            if indice == 0:
                return self.__v[len(self.__v) - 1]
            else:
                return self.__v[indice - 1]
        else:
            return None

    # restituisce il vertice successivo a quello passato
    # come oggetto di tipo gcPunto o come stringa
    def verticeSuccessivo(self, p):
        """ restituisce il vertice successivo a quello passato come punto
        """
        p = gcPunto(p)  # converti il parametro in oggetto punto in caso sia una stringa
        if p in self.__v:
            indice = self.__v.index(p)
            if indice == len(self.__v) - 1:
                return self[0]
            else:
                return self[indice + 1]
        else:
            return None

    # restituisce True se i due vertici passati come oggetti di tipo gcPunto o come stringa
    # sono adiacenti
    def adiacenti(self, p, q):
        """ verifica se due vertici del poligono sono adiacenti
        """
        p = gcPunto(p)  # converti i parametro in oggetto punto in caso siano stringhe
        q = gcPunto(q)
        p_prec = self.verticePrecedente(p)
        p_succ = self.verticeSuccessivo(p)
        if p_prec is None or p_succ is None:
            return False
        else:
            adiac = (p_prec == q or p_succ == q)
            return adiac

    # restituisce il poligono come stringa costituita da un elenco di punti
    # col metodo speciale __str__
    def __str__(self):
        """ restituisce il poligono in formato stringa come elenco dei suoi vertici
        """
        if len(self.__v) == 0:
            return "[]"
        else :
            listapuntistringa = [str(p) for p in self.__v]
            s = "[ " + ", ".join(listapuntistringa) + " ]"
            return s

    # restituisce la rappresentazione poligono come stringa col metodo speciale __repr__
    # che viene implicitamente utilizzata nelle altre classi
    def __repr__(self):
        """ restituisce il poligono in formato stringa per le altre implementazioni
            (ad esempio per l'utilizzo in altre classi)
        """
        return str(self)

    #------------------------------------------------------------------------------------

    # confronta due poligoni (con una certa approssimazione)
    # sovraccaricando l'operatore di uguaglianza ==
    # col metodo speciale __eq__
    def __eq__(self, pl):
        """ confronta due poligoni con l'uguale con approssimazione data da _TOLLERANZA
        """
        if pl == None:
            return False
        n = self.lunghezza()
        if len(pl) != n:   # se i due poligoni hanno lunghezze diverse sono certamente differenti
            return False
        else :
            uguali = True
            for i in range(n) :
                if self[i] != pl[i] :
                    uguali = False
            return uguali

    # confronta due poligoni (con una certa approssimazione)
    # sovraccaricando l'operatore di uguaglianza !=
    # col metodo speciale __ne__
    def __ne__(self, pl):
        """ confronta due poligoni col diverso con approssimazione data da _TOLLERANZA
        """
        differenti = not (self == pl)
        return differenti

    #------------------------------------------------------------------------------------

    # restituisce la lunghezza (il numero dei vertici) del poligono
    # col metodo speciale __len__ che sovrascrive la funzione len()
    def __len__(self):
        """ lunghezza (ovvero numero dei vertici) di un poligono
        """
        return len(self.__v)

    # restituisce la lunghezza (il numero dei vertici) del poligono
    def lunghezza(self):
        """ lunghezza (ovvero numero dei vertici) di un poligono
        """
        return len(self.__v)

    # --------------------------------------------------------------------------

    # restituisce l'ascissa di valore minimo dei vertici del poligono
    def xMin(self):
        """ minima ascissa dei vertici del poligono
        """
        if len(self.__v) > 0 :
            m = min(p.getx() for p in self.__v)
            return m

    # restituisce l'ascissa di valore massimo dei vertici del poligono
    def xMax(self):
        """ massima ascissa dei vertici del poligono
        """
        if len(self.__v) > 0 :
            m = max(p.getx() for p in self.__v)
            return m

    # restituisce l'ordinata di valore minimo dei vertici del poligono
    def yMin(self):
        """ minima ordinata dei vertici del poligono
        """
        if len(self.__v) > 0 :
            m = min(p.gety() for p in self.__v)
            return m

    # restituisce l'ordinata di valore massimo dei vertici del poligono
    def yMax(self):
        """ massima ordinata dei vertici del poligono
        """
        if len(self.__v) > 0 :
            m = max(p.gety() for p in self.__v)
            return m

    # --------------------------------------------------------------------------

    # cancella il poligono eliminando tutti i vertici
    def cancella(self):
        """ cancella il poligono eliminando tutti i suoi vertici
        """
        # self.__v = list()
        self.__v.clear()

    # aggiunge un punto in coda al poligono
    # sia che venga passato come oggetto di tipo gcPunto
    # sia che venga passato come stringa (nel qual caso viene prima convertito)
    def aggiungi(self, p):
        """ aggiunge un vertice al poligono passandolo indifferentemente
            come punto oppure come stringa
        """
        p = gcPunto(p)  # converti il parametro in oggetto punto in caso sia una stringa
        self.__v.append(p)


    # inserisce un punto in una determinata posizione (indice) del poligono
    # sia che venga passato come oggetto di tipo gcPunto
    # sia che venga passato come stringa (nel qual caso viene prima convertito)
    def inserisci(self, i, p):
        """ inserisce un vertice p nella posizione i del poligono
            passandolo indifferentemente come punto oppure come stringa
        """
        p = gcPunto(p)  # converti il parametro in oggetto punto in caso sia una stringa
        # if i >= 0 and i < self.lunghezza():
        self.__v.insert(i, p)

    # estrae restituendolo il vertice di indice i ed eliminandolo dal poligono
    # se l'indice viene omesso viene estratto il primo punto (quello di indice 0)
    def estrai(self, i=0):
        """ estrae il vertice di indice i (anche negativo) e lo rimuove dal poligono
        """
        pp = self.__v.pop(i)
        return pp

    # # estrae restituendolo il primo vertice eliminandolo dal poligono
    # def estraiPrimo(self):
    #     """ estrae e rimuove il primo vertice del poligono
    #     """
    #     return self.estrai(0)
    #
    # # estrae restituendolo l'ultimo vertice eliminandolo dal poligono
    # def estraiUltimo(self):
    #     """ estrae e rimuove l'ultimo vertice del poligono
    #     """
    #     return self.estrai(self.lunghezza()-1)


    # elimina un punto in una determinata posizione (indice) del poligono
    def elimina(self, i=0):
        """ elimina il vertice di indice i (anche negativo) del poligono
        """
        if i < self.lunghezza():
            self.__v.pop(i)

    # restituisce True se il poligono contiene un punto come suo vertice
    # sia che venga passato come oggetto di tipo gcPunto
    # sia che venga passato come stringa (nel qual caso viene prima convertito)
    def haVertice(self, p):
        """ verifica se il punto p è un vertice del poligono
        """
        p = gcPunto(p)  # converti il parametro in oggetto punto in caso sia una stringa
        havert = p in self.__v
        return havert

    # restituisce True se il punto appartiene al poligono
    # col metodo speciale __contains__ che sovrascrive l'operatore in
    # sia che venga passato come oggetto di tipo gcPunto o come stringa
    # richiamando il metodo haVertice
    def __contains__(self, p):
        """ verifica se il punto p è un vertice del poligono
        """
        return self.haVertice(p)

    # restituisce True se il poligono contiene un segmento come suo lato
    # sia che venga passato come oggetto di tipo gcSegmento
    # sia che venga passato come stringa (nel qual caso viene prima convertito)
    # il valore False del parametro verso fa si che il segmento venga considerato lato
    # anche se fornito in verso opposto
    def haLato(self, s, verso=True):
        """ verifica se il segmento s è un lato del poligono
            con verso=False ci considera lato anche un segmento di verso opposto
        """
        s = gcSegmento(s)  # converti il parametro in oggetto segmento in caso sia una stringa
        halato = False
        n = self.lunghezza()
        if n>0:
            for i in range(n):
                if self.lato(i) == s :
                    halato = True
                elif verso == False and self.lato(i) == s.opposto() :
                    halato = True
        return halato


    # restituisce l'indice corrispondente al vertice del poligono passato come parametro
    # sia come oggetto di tipo gcPunto sia come stringa
    def indice(self, p):
        """ restituisce l'indice corrispondente ad un vertice del poligono
        """
        p = gcPunto(p)  # converti il parametro in oggetto punto in caso sia una stringa
        if p in self.__v:
            indice = self.__v.index(p)
            return indice
        else:
            return None

    # rimuove un vertice del poligono passandone il valore
    # sia che venga passato come indice (nel qual caso si trova il punto corrispondente)
    # oppure come oggetto di tipo gcPunto
    # o ancora che venga passato come stringa (nel qual caso viene prima convertito)
    # ATTENZIONE: non è necessario specificare che rimuoviamo solo la prima occorrenza
    # perché trattandosi di un POLIGONO SEMPLICE nessun vertice può essere ripetuto
    def rimuovi(self, p):
        """ rimuovi il vertice del poligono passando un punto
        """
        if type(p) == int:    # se è stato passato un intero trovo il punto di indice corrispondente
            p = self.__v[p]
        else:
            p = gcPunto(p)    # converti il parametro in oggetto punto in caso sia una stringa
        if p in self.__v:
            self.__v.remove(p)

    #----------------------------------------------------------------------------------------

    # inverte l'orientamento del poligono ordinando i punti in verso opposto
    def inverti(self):
        """ inverte l'ordine dei punti contenuti nella lista
        """
        self.__v.reverse()

    # ---------------------------------------------------------------------------------------

    # restituisce la somma del poligono corrente con un altro poligono passato come parametro
    def somma(self, pol):
        """ addizione tra il poligono corrente e un altro poligono passato come parametro
        """
        n = self.lunghezza()
        n2 = pol.lunghezza()
        somma = gcPoligono()
        if n != n2 or n * n2 == 0:  # se i due poligoni hanno lunghezze diverse o uno dei due è nullo
            return somma  # restituisci il poligono nullo
        for i in range(n):
            ptsomma = self[i] + pol[i]    # addizione tra punti o vettori
            somma.aggiungi(ptsomma)
        return somma

    # restituisce la somma del poligono corrente con un punto passato come parametro
    # ossia trasla il poligono per mezzo del vettore p
    def sommaPunto(self, p):
        """ addizione tra il poligono corrente e un punto
        """
        somma = gcPoligono()
        for i in range(self.lunghezza()):
            ptsomma = self[i] + p    # addizione tra punti o vettori
            somma.aggiungi(ptsomma)
        return somma

    # restituisce il prodotto del poligono corrente per uno scalare reale passato come parametro
    def moltiplicaPerScalare(self, r):
        """ moltiplicazione tra un poligono e uno scalare
        """
        prodotto = gcPoligono()
        for i in range(self.lunghezza()):
            ptprodotto = self[i] @ r  # moltiplicazione punto/scalare
            prodotto.aggiungi(ptprodotto)
        return prodotto

    #----------------------------------------------------------------------------------------

    # definisce l'iteratore per l'oggetto poligono azzerando l'indice
    def __iter__(self):
        self.__i = 0   # inizializza l'indice privato __i da usare come contatore
        return self

    # restituisce il prossimo elemento iterato dell'oggetto poligono
    def __next__(self):
        if self.__i < len(self.__v):  # se l'indice __i non eccede la lunghezza del poligono
            pt = self.__v[self.__i]   # preleva il punto di indice __i
            self.__i +=1              # incremente il contatore privato __i
            return pt                 # e restituisce il punto
        raise StopIteration           # altrimenti interrompi l'iterazione

    # ----------------------------------------------------------------------------------------

    # metodo per estendere (accodare o concatenare) il poligono corrente
    # con un altro poligono passato come parametro
    def estendi(self, pol):
        """ estendi un poligono con un altro poligono passato come parametro
        """
        for p in pol :
            self.aggiungi(p)

    # restituisce la concatenzione di due poligoni sovraccaricando l'operatore di addizione +
    # col metodo speciale __add__
    def __add__(self, pol):
        """ concatenazione di due poligoni
        """
        polconcat = gcPoligono(self)
        polconcat.estendi(pol)
        return polconcat

    # ----------------------------------------------------------------------------------------

    # restituisce come segmento il lato il cui estremo iniziale
    # è l'i-esimo vertice (partendo dall'indice 0)
    def lato(self, i):
        """ restituisce il lato che ha estremo iniziale nel vertice di indice i
        """
        if self.lunghezza()>0:
            return gcSegmento(self[i], self[i+1])
        # n = self.lunghezza()
        # if i >= 0 and i < n:
        #     p1 = self[i]
        #     if i != n-1:
        #         p2 = self[i+1]
        #     else:
        #         p2 = self[0]
        #     s = gcSegmento(p1, p2)
        #     return s
        # else:
        #     return None

    # restituisce la lista dei lati del poligono corrente
    def listaLati(self):
        """ restituisce la lista dei lati del poligono
        """
        n = self.lunghezza()
        if n>0:
            lista = list()
            for i in range(n):
                lista.append(self.lato(i))
            return lista
        else:
            return None

    # ------------------------------------------------------------------------------------

    # restituisce il vertice minimo rispetto ad una relazione di ordine di punti del piano
    # (lessicografico verticale o polare) passata come parametro
    def minimo(self, ordinamento=gcPunto.lessicograficoVerticale, polo=None):
        """ restituisce il vertice minimo rispetto ad un dato ordinamento
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

    # restituisce il vertice massimo rispetto ad una relazione di ordine di punti del piano
    # (lessicografico verticale o polare) passata come parametro
    def massimo(self, ordinamento=gcPunto.lessicograficoVerticale, polo=None):
        """ restituisce il vertice minimo rispetto ad un dato ordinamento
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

    # funzione di ordinamento col mergesort
    # su una lista di punti rappresentata come poligono
    # rispetto ad una relazione di ordine di punti del piano (lessicografico verticale o polare)
    # passata come parametro
    def mergeSort(lista, ordinamento, polo):
        """ esegue l'ordinamento di una lista di punti col metodo del merge sort
        """
        if lista.lunghezza() > 1:
            medio = lista.lunghezza() // 2  # calcola l'indice intermedio
            sx = gcPoligono(lista[:medio])  # dividi la lista in due sottoliste sinistra e destra
            dx = gcPoligono(lista[medio:])
            # ordina ricorsivamente le due sottoliste
            gcPoligono.mergeSort(sx, ordinamento, polo)
            gcPoligono.mergeSort(dx, ordinamento, polo)
            # unisce la lista ricopiando i valori delle sottoliste
            lista.cancella()
            i = j = 0
            while i < sx.lunghezza() and j < dx.lunghezza():
                if ordinamento(sx[i], dx[j], polo):   #  se sx[i]<=dx[j]
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

    # ordina i vertici del poligono (o di una lista di punti) rispetto a un dato ordinamento
    # (lessicografico verticale o polare)
    # e restituisce la lista di punti ordinata
    def ordina(self, ordinamento=gcPunto.lessicograficoVerticale, polo=None):
        """ restituisce la lista dei vertici ordinata rispetto
            a un dato ordinamento (lessicografico verticale o polare)
        """
        listapunti = gcPoligono(self)   # copia il poligono per non perdere l'originale
        gcPoligono.mergeSort(listapunti, ordinamento, polo)   # richiama il merge sort sulla lista di punti
        return listapunti  # restituisce la lista di punti ordinata

    # ------------------------------------------------------------------------------------

    # verifica se la lista di punti definisce un poligono semplice
    # controllando che nessuna coppia di segmenti non adiacenti si intersechi
    # in caso positivo restituisce True
    # in caso negativo restituisce la coppia (tupla) formata
    # dai primi due segmenti non adiacenti che si intersecano tra loro
    def isPoligonoSemplice(self):
        """ verifica se la lista ordinata di punti costituisce un poligono semplice
            ed eventualmente restituisce la prima coppia di segmenti che si intersecano
        """
        n = self.lunghezza()
        if n>2:
            for i in range(0, n-2):  # fino a n-2 escluso cioè fino a n-3
                li = self.lato(i)
                for j in range(i+2, n-1):  # fino a n-1 escluso cioè fino a n-2
                    lj = self.lato(j)
                    if li.interseca(lj) == True:  # se due lati non adiacenti si intersecano
                        return (li,lj)            # esci restituendo la coppia di lati
            # altrimenti se non è stata trovata alcuna intersezione tra lati restituisci True
            return True
        else:
            return None


    # semplifica i vertici di un poligono semplice
    # eliminando eventuali terne di punti collineari
    # rimuovendo il punto centrale
    def semplifica(self):
        """ semplifica un poligono semplice rimuovendo i vertici non necessari
            perché collineari ad altri
        """
        i = 0
        while (i < self.lunghezza() - 2):  # fino a n-1 escluso cioè n-2 incluso
            if gcPunto.collineari(self[i], self[i+1], self[i+2]):
                self.elimina(i+1)
                # nel caso in cui anche i due vertici successivi a quello eliminato
                # sono ancora collineari col vertice precedente, per poterlo rimuovere dobbiamo considerare
                # lo stesso vertice di partenza e quindi, sapendo che l'indice verrà incrementato
                # dovremo decrementarlo preventivamente per restare sullo stesso punto
                i -= 1
            i += 1


    # verifica se il poligono è convesso
    # controllando la convessità di tutti i suoi angoli interni
    # e restituendo True in caso positivo
    # oppure restituendo il vertice del primo angolo non convesso che viene trovato
    def isPoligonoConvesso(self):
        """ verifica se il poligono è convesso
        """
        n = self.lunghezza()
        if n>2:
            for i in range(n):
                if gcPunto.isConvesso(self[i-1], self[i], self[i+1]) == False:
                    return i  # esce restituendo l'indice del primo vertice con angolo interno NON convesso
        # se invece la condizione risulta sempre vero, conclude restituendo True (poligono convesso)
        return True

    # calcola il baricentro geometrico del poligono corrente
    def baricentro(self):
        """ restituisce il baricentro geometrico del poligono corrente
            come oggetto punto
        """
        n = self.lunghezza()
        xb = sum([p.getx() for p in self]) / n
        yb = sum([p.gety() for p in self]) / n
        b = gcPunto(xb, yb)
        return b


    # restituisce l'area del poligono corrente
    # utilizzando la forma discreta della formula di Gauss-Green
    def area(self):
        """ restituisce l'area del poligono
        """
        n = self.lunghezza()
        if n>2:
            somma1 = 0
            somma2 = 0
            for i in range(n):
                somma1 += self[i].getx() * self[i+1].gety()
                somma2 += self[i+1].getx() * self[i].gety()
        a = (somma1 - somma2) / 2
        return a

    # ------------------------------------------------------------------------------------

    # restituisce True se il punto si trova sulla frontiera del poligono (sia convesso che non)
    def puntoInFrontiera(self, p):
        """ verifica se il punto appartiene alla frontiera del poligono
        """
        n = self.lunghezza()
        if n>2:
            # crea una tupla con le posizioni ammissibili del punto sui vari lati del poligono
            casi_ammessi = ('inizio', 'fine', 'interno')
            for i in range(n):
                if self.lato(i).posizione(p) in casi_ammessi:
                    return True # se il punto si trova su uno dei lati (estremi inclusi) esce restituendo True
        # se invece la condizione non si verifica mai conclude restituendo False (il punto non è sulla frontiera)
        return False


    # restituisce True se il punto si trova all'interno del poligono convesso corrente
    # esclusa la frontiera controllando che ogni terna di punti costituita
    # dai due vertici consecutivi del poligono e dal punto dato
    # abbia orientamento CCW cioè la sua area segnata sia strettamente maggiore di zero
    def puntoInPoligonoConvesso(self, p):
        """ verifica se il punto è contenuto all'interno di un poligono convesso
        """
        n = self.lunghezza()
        if n>2:
            for i in range(n):
                if gcPunto.areaSegnata(self[i], self[i+1], p) <= 0:
                    return False  # esce restituendo False (il punto NON è interno al poligono)
            # se invece l'area segnata si è sempre mantenuta >0 restituisce True (il punto è interno al poligono)
            return True

    # restituisce True se il segmento passato come parametro
    # è interamente contenuto all'interno di un poligono convesso correnre
    # verificando che entrambi gli estremi siano interni al poligono stesso
    # (ossia sfruttando la definizione di convessità)
    def segmentoInPoligonoConvesso(self, s):
        """ verifica se il segmento passato come parametro è contenuto interamente
            all'interno del poligono convesso corrente
        """
        p = s.getInizio()
        q = s.getFine()
        if self.puntoInPoligonoConvesso(p) and self.puntoInPoligonoConvesso(q):
            return True
        else:
            return False

    # ------------------------------------------------------------------------------------

    # restituisce True se il punto si trova all'interno del poligono semplice corrente
    # non necessariamente convesso per mezzo dell'algoritmo ray-shooting (o di Jordan)
    # i punti sulla frontiera vengono considerati (per convenzione) interni al poligono
    # soltanto se appartenti:
    # - agli interni dei lati percorsi in verso antiorario (CCW) in senso discendente
    # - agli estremi iniziali dei lati percorsi da sinistra verso destra in senso discendente
    # - agli estremi finali dei lati percorsi da destra verso sinistra in senso discendente
    def puntoInPoligono(self, p):
        """ verifica se il punto è contenuto all'interno di un poligono convesso
        """
        num_intersezioni = 0  # crossing number
        n = self.lunghezza()
        if n>2 :
            for i in range(n) :
                lato = self.lato(i)
                posiz = lato.posizione(p)
                p_i = lato.getInizio()
                p_f = lato.getFine()
                if posiz == 'sinistra' :  # segmento verso l'alto
                    if p_i.gety() < p.gety() <= p_f.gety():  # secante
                        num_intersezioni += 1
                elif posiz == 'destra' :  # segmento verso il basso
                    if p_f.gety() < p.gety() <= p_i.gety():  # secante
                        num_intersezioni += 1
            punto_interno = True if num_intersezioni % 2 == 1 else False
            return punto_interno


    # ------------------------------------------------------------------------------------

    # restituisce True se il punto si trova all'interno di un poligono semplice
    # o sulla sua frontiera, ossia nella sua chiusura
    def puntoInChiusuraPoligono(self, p):
        """ verifica se il punto è contenuto nella chiusura di un poligono convesso
        """
        return self.puntoInPoligono(p) or self.puntoInFrontiera(p)


    # ------------------------------------------------------------------------------------

    # restituisce True se il segmento passato come parametro
    # è interamente contenuto all'interno del poligono
    # verificando che:
    # - gli estremi del segmento siano entrambi punti interni al poligono
    # - il segmento non interseca propriamente la frontiera del poligono
    # - il punto medio del segmento è anch'esso interno al poligono
    def segmentoInPoligono(self, s):
        """ verifica se il segmento passato come parametro è contenuto interamente
            all'interno del poligono corrente
            (se il segmento interseca anche solo un vertice dall'interno non viene
            considerato contenuto propriamente nel poligono)
        """
        n = self.lunghezza()
        if n>2 :
            # se tutti i due estremi del segmento non sono interni al poligono,
            # il segmento non può essere interno
            pi = s.getInizio()
            pf = s.getFine()
            if self.puntoInPoligono(pi)==False or self.puntoInPoligono(pf)== False :
                return False
            else :    # se il segmento interseca la frontiera, il segmento non può essere interno
                intersez = False
                for i in range(n):
                    l = self.lato(i)  # lato corrente
                    p = self.vertice(i)  # vertice corrente
                    if s.interseca(l) :
                        intersez = True
                # se gli estremi sono interni e il segmento non interseca la frontiera
                # e il suo punto medio è interno allora il segmento è interno
                if intersez == False :
                    m = s.getMedio()               # verifichiamo che il segmento sia interamente interno al poligono
                    return self.puntoInPoligono(m) # controllando che il suo punto medio sia interno
                else :
                    return False

    # ----------------------------------------------------------------------------------------

    # metodo che restituisce True se per una coppia di vertici passati come parametri
    # passa una diagonale del poligono
    def isDiagonale(self, p1, p2):
        """ verifica che il segmento individuato dai due vertici costituisca una diagonale
        """
        n = self.lunghezza()
        if n == 0 :  # se il poligono è nullo non può esserci alcuna diagonale
            return False
        elif not p1 in self or not p2 in self :   # se anche solo uno dei punti non è un vertice
            return False                        # non ci può essere una diagonale
        elif self.adiacenti(p1,p2) :     # due vertici adiacenti non possono formare una diagonale
            return False
        else :
            s = gcSegmento(p1, p2)
            intersez = False
            # verifica che il segmento non abbia intersezioni proprie con i lati del poligono
            # e che il suo interno non contenga alcun altro vertice
            for i in range(n) :
                l = self.lato(i)         # lato corrente
                p = self.vertice(i)      # vertice corrente
                if s.intersecaPropriamente(l) or s.posizione(p) == 'interno' :
                    intersez = True
            if intersez == False :
                m = s.getMedio()               # verifichiamo che il segmento sia interamente interno al poligono
                return self.puntoInPoligono(m) # controllando che il suo punto medio sia interno
            else :
                return False


    # metodo che restituisce True se il vertice passato come parametro
    # costituisce una orecchia del poligono
    # verificando che il segmento tra i vertici adiacenti sia una diagonale
    def isOrecchia(self, p):
        """ verifica che nel vertice passato come parametro ci sia una orecchia
        """
        if not p in self :   # se il punto passato non è un vertice non può essere un'orecchia
            return False
        p_prec = self.verticePrecedente(p)
        p_succ = self.verticeSuccessivo(p)
        return self.isDiagonale(p_prec, p_succ)

    # ------------------------------------------------------------------------------------

    # metodo che trova e restituisce la coppia di vertici corrispondenti
    # alla prima diagonale utile del poligono corrente
    def verticiDiagonale(self):
        """ restituisce la coppia dei vertici corrispondenti
            alla prima diagonale utile del poligono corrente
        """
        n = self.lunghezza()
        for i in range(n-2) :
            for j in range(i+2, n) :
                if self.isDiagonale(self.vertice(i), self.vertice(j)) :
                    return (self.vertice(i), self.vertice(j))

    # ------------------------------------------------------------------------------------

    # metodo statico che restituisce l'inviluppo convesso di un insieme di punti
    # calcolato mediante l'algoritmo del Gift Wrapping
    @staticmethod
    def inviluppoConvessoGiftWrapping(listapunti):
        """ calcola e restituisce l'inviluppo convesso della lista di punti corrente
            mediante l'algoritmo del Gift Wrapping
        """
        pnt = gcListaPunti(listapunti)  # crea una copia della lista di punti da utilizzare per il procedimento
        pnt.eliminaPuntiRipetuti()  # elimina eventuali punti ripetuti nella lista
        # trova il punto iniziale come minimo rispetto all'ordinamento lessicografico verticale
        p0 = pnt.minimo(ordinamento=gcPunto.lessicograficoVerticale)
        # aggiungiamo il minimo (che sicuramente vi appartiene) al futuro inviluppo convesso
        # e lO RIMUOVIAMO TEMPORANEAMENTE dalla lista di punti per farlo ritrovare alla conclusione
        inv = gcPoligono([p0])
        pnt.rimuovi(p0)
        mn = pnt.minimo(ordinamento=gcPunto.giftWrapping, polo=p0)  # estraiamo un minimo rispetto al punto base
        pnt.rimuovi(mn)  # lo rimuoviamo dalla lista dei punti
        inv.aggiungi(mn)  # e lo aggiungiamo all'inviluppo corrente
        # aggiungiamo di nuovo alla lista dei punti il punto iniziale
        # che ci servirà come indicatore per concludere il processo
        pnt.aggiungi(p0)
        # trova il nuovo minimo rispetto all'ordinamento con polo nell'ultimo punto dell'inviluppo
        # fino a quando questo non coincide col punto iniziale
        continua = True
        while continua:
            mn = pnt.minimo(ordinamento=gcPunto.giftWrapping, polo=inv[-1])  # estrae un nuovo minimo
            pnt.rimuovi(mn)  # e lo rimuove dalla lista dei punti
            if mn == p0:  # se ritroviamo il punto iniziale
                continua = False  # il procedimento si è concluso
            else:
                inv.aggiungi(mn)  # aggiungiamo il punto all'inviluppo corrente
        # semplifica il poligono inviluppo per evitare che un segmento contenga punti intermedi allineati
        inv.semplifica()
        return inv


    # metodo statico che restituisce l'inviluppo convesso di un insieme di punti
    # calcolato mediante l'algoritmo della scansione di Graham
    @staticmethod
    def inviluppoConvessoGrahamScan(listapunti):
        """ calcola e restituisce l'inviluppo convesso della lista di punti corrente
            mediante l'algoritmo Graham Scan
        """
        pnt = gcListaPunti(listapunti)  # crea una copia della lista di punti da utilizzare per il procedimento
        # ---- elimina eventuali punti ripetuti nella lista
        # E' UNA OPERAZIONE DI ALLEGGERIMENTO che velocizza l'esecuzione MA NON E' INDISPENSABILE
        # PERCHE' L'ALGORITMO RESTITUISCE IL RISULTATO CORRETTO ANCHE SENZA
        # QUESTA OPERAZIONE DI RIPULITURA PRELIMINARE
        # in quanto è in grado di eliminare successivamente i punti con angoli uguali
        # (cioè allineati col punto base) di distanza minore
        pnt.eliminaPuntiRipetuti()
        # trova il minimo rispetto all'ordinamento lessicografico orizzontale
        puntobase = pnt.minimo(gcPunto.lessicograficoOrizzontale)
        # ordina lo lista rispetto all'ordinamento polare con polo nel minimo
        pnt = pnt.ordina(ordinamento=gcPunto.polare, polo=puntobase)
        # semplifica la lista di punti
        # verificando se ci sono punti che formano lo stesso angolo rispetto al polo
        # ed in caso positivo scarta il più vicino al polo
        i = 1
        while i < pnt.lunghezza() - 1:
            j = i + 1
            while j < pnt.lunghezza():
                if pnt[0].isCollineare(pnt[i], pnt[j]):
                    if pnt[0].distanza(pnt[i]) <= pnt[0].distanza(pnt[j]):
                        pnt.elimina(i)
                    else:
                        pnt.elimina(j)
                j += 1
            i += 1
        # aggiungi i primi due punti al futuro inviluppo
        inv = gcPoligono([pnt.estrai(), pnt.estrai()])
        # calcola l'inviluppo convesso
        while pnt.lunghezza() > 0:
            # estrai un punto dalla lista e aggiungilo all'inviluppo corrente
            inv.aggiungi(pnt.estrai())
            # finché gli ultimi tre punti dell'inviluppo avranno orientamento a destra
            # elimina il penultimo punto
            while not gcPunto.CCW(inv[-3], inv[-2], inv[-1]):
                inv.elimina(-2)
        return inv


    # metodo statico che restituisce l'inviluppo convesso di un insieme di punti
    # calcolato mediante l'algoritmo incrementale Insertion Hull
    @staticmethod
    def inviluppoConvessoInsertionHull(listapunti):
        """ calcola e restituisce l'inviluppo convesso della lista di punti corrente
            mediante l'algoritmo Insertion Hull
        """
        pnt = gcListaPunti(listapunti)  # crea una copia della lista di punti da utilizzare per il procedimento
        # ordina i punti rispetto all'ordinamento lessicografico verticale
        # in modo da avere ordinatamente solo punti esterni all'inviluppo corrente
        # e non dover verificare ad ogni passaggio che il nuovo punto considerato
        # sia interno o esterno all'inviluppo corrente
        pnt = pnt.ordina(ordinamento=gcPunto.lessicograficoOrizzontale)
        # estrae i primi tre punti della lista ordinata
        # per creare l'inviluppo iniziale
        inv = gcPoligono([pnt.estrai(), pnt.estrai(), pnt.estrai()])
        # itera finché la lista di punti non si esaurisce
        while pnt.lunghezza() > 0:
            p = pnt.estrai()
            p_inf = inv.massimo(ordinamento=gcPunto.polare, polo=p)  # punto di tangenza inferiore
            p_sup = inv.minimo(ordinamento=gcPunto.polare, polo=p)  # punto di tangenza superiore
            i_inf = inv.indice(p_inf)  # determina l'indice del punto di tangenza inferiore
            # elimina tutti i punti intermedi a partire da quello successivo al punto di tangenza inferiore
            # fino a quando non raggiunge il punto di tangenza superiore
            while inv[i_inf + 1] != p_sup:
                inv.elimina(i_inf + 1)
            inv.inserisci(i_inf + 1, p)  # aggiungi il nuovo punto in posizione intermedia tra i punti di tangenza
        # poiché l'algoritmo di insertion hull non verifica se quando si aggiunge un punto
        # questo possa essere allineato con i due punti precedenti o i due punti successivi
        # dell'inviluppo corrente, alla fine vengono rimossi eventuali punti intermedi allineati
        inv.semplifica()
        return inv


    # ------------------------------------------------------------------------------------

    # # metodo statico che restituisce l'inviluppo convesso di un insieme di punti
    # # calcolato mediante l'algoritmo incrementale Insertion Hull
    # @staticmethod
    # def triangolazionePerDiagonali(pol, triangolazione, diagonali):
    #     if pol.lunghezza() == 3:  # se il poligono si è ridotto a solo tre punti
    #         triang = gcTriangolo(pol)  # restituiamo il poligono convertito in triangolo
    #         triangolazione.append(triang)
    #         return True
    #     else:
    #         (p1, p2) = pol.verticiDiagonale()  # troviamo i vertici di una diagonale
    #         diag = gcSegmento(p1, p2)
    #         diagonali.append(diag)
    #         # spezziamo il poligono in due sottopoligoni mediante la diagonale
    #         i1 = pol.indice(p1)  # determiniamo gli indici dei vertici su cui insiste la diagonale
    #         i2 = pol.indice(p2)  # con 0<=i1<i2
    #         pol1 = pol[i1:i2 + 1]
    #         pol2 = pol[i2:] + pol[0:i1 + 1]
    #         # applichiamo la triangolazione ai due sottopoligoni
    #         triangolazione_per_diagonali(pol1, triangolazione, diagonali)
    #         triangolazione_per_diagonali(pol2, triangolazione, diagonali)

    # ------------------------------------------------------------------------------------


    # restituisce i punti di intersezione propri (che non siano vertici)
    # tra la frontiera del poligono corrente con quella di un altro poligono passato come parametro
    # oppure una lista di punti vuota se non ci sono intersezioni
    def puntiIntersezionePropriPoligoni(self, pol):
        """ restituisce i punti di intersezione propri tra la frontiera del poligono corrente
            con quella di un altro poligono passato come parametro
        """
        intersez_proprie = gcListaPunti()              # determina le intersezioni proprie dei due poligoni
        for i in range(self.lunghezza()):
            l1 = self.lato(i)
            for j in range(pol.lunghezza()):
                l2 = pol.lato(j)
                if l1.intersecaPropriamente(l2):    # interseca in punti diversi dagli estremi
                    p = l1.intersezione(l2)
                    if intersez_proprie.haPunto(p) == False:
                        intersez_proprie.aggiungi(p)
        return intersez_proprie


    # restituisce i punti di intersezione anche impropri (cioè coincidenti coi vertici)
    # tra la frontiera del poligono corrente con quella di un altro poligono passato come parametro
    # oppure una lista di punti vuota se non ci sono intersezioni
    def puntiIntersezionePoligoni(self, pol):
        """ restituisce i punti di intersezione (anche impropri) tra la frontiera del poligono corrente
            con quella di un altro poligono passato come parametro
        """
        intersez = gcListaPunti()              # determina le intersezioni dei due poligoni
        for i in range(self.lunghezza()):
            l1 = self.lato(i)
            for j in range(pol.lunghezza()):
                l2 = pol.lato(j)
                if l1.interseca(l2):     # interseca anche nei vertici
                    p = l1.intersezione(l2)   # trova l'intersezione dei due segmenti ma esclude estremo finale del primo con estremo iniziale del secondo
                    if p==None :      # ***** restituisce il solo estremo inziale del lato quando non viene trovata alcuna intersezione
                        intersez.aggiungi(l1.getInizio())
                        return intersez
                    if intersez.haPunto(p) == False:
                        intersez.aggiungi(p)
        return intersez

    # metodo che restituisce i vertici del poligono corrente
    # contenuti all'interno di un altro poligono passato come parametro
    def verticiInPoligono(self, pol):
        """ restituisce i vertici del poligono corrente contenuti all'interno
            del poligono passato come parametro
        """
        n = self.lunghezza()
        if n>2 :
            l = gcListaPunti()
            for p in self:
                if pol.puntoInChiusuraPoligono(p) == True :
                    l.aggiungi(p)
            return l


    # restituisce il poligono intersezione di due poligoni convessi
    # oppure un poligono vuoto se i due poligoni sono disgiunti
    def intersezionePoligoniConvessi(self, pol):
        """ restituisce il poligono intersezione di due poligoni convessi
            oppure None se i due poligoni sono disgiunti
        """
        if self == None or pol == None:
            return gcPoligono()
        vertici1 = self.verticiInPoligono(pol)                # trova i vertici del primo poligono contenuti nel secondo
        vertici2 = pol.verticiInPoligono(self)                # trova i vertici del secondo poligono contenuti nel primo
        intersezioni = self.puntiIntersezionePoligoni(pol)    # determina le intersezioni dei due poligoni   ****** ERRORE
        if vertici1 == None or vertici2 == None or intersezioni == None:
            return gcPoligono()
        lista = vertici1 + vertici2 + intersezioni            # unisce i vertici e le intersezioni trovate
        if len(lista) != 0 :
            b = lista.baricentro()      # trasforma la lista in poligono ordinando i punti con l'ordinamento polare
            lista = lista.ordina(ordinamento=gcPunto.polare, polo=b)  # rispetto al loro baricentro geometrico
        poligono_intersezione = gcPoligono(lista)
        poligono_intersezione.semplifica()
        return poligono_intersezione


    # ------------------------------------------------------------------------------------

    # restituisce il poligono ritagliato (clipped) del poligono corrente (preso come soggetto)
    # rispetto al poligono convesso di ritaglio (clipping) usando l'algoritmo di Sutherland-Hodgman
    def ritaglio(self, pol_clipping):
        """ restituisce il poligono ritaglio del poligono corrente
            rispetto ad un poligono convesso di ritaglio passato come parametro
        """
        pol_nuovo = gcPoligono(self)
        for i in range(pol_clipping.lunghezza()):
            lato_clipping = pol_clipping.lato(i)  # i-esimo lato del poligono di ritaglio (clipping polygon)
            pol_corrente = gcPoligono(pol_nuovo)  # memorizza il poligono ritagliato parziale ottenuto al passaggio precedente
            pol_nuovo.cancella()  # cancella il nuovo poligono
            for j in range(pol_corrente.lunghezza()):
                p = pol_corrente[j]  # punto corrente del lato del poligono soggetto
                p_prec = pol_corrente[j - 1]  # punto del poligono soggetto precedente di quello corrente
                lato_soggetto = pol_corrente.lato(j - 1)  # lato del poligono soggetto corrente
                intersez = lato_clipping.intersezione(lato_soggetto)
                if lato_clipping.semipianoSinistroContiene(p):
                    if not lato_clipping.semipianoSinistroContiene(p_prec):  # p a sx e p_prec a dx
                        if intersez is not None:
                            pol_nuovo.aggiungi(intersez)
                    pol_nuovo.aggiungi(p)
                elif lato_clipping.semipianoSinistroContiene(p_prec):  # p a dx, p_prec a sx
                    if intersez is not None:
                        pol_nuovo.aggiungi(intersez)
        pol_nuovo.semplifica()  # elimina eventuali punti collineari consecutivi
        return pol_nuovo

    # ------------------------------------------------------------------------------------

    # restituisce i punti di intersezione anche impropri (cioè coincidenti coi vertici)
    # tra la frontiera del poligono corrente e una retta rappresentata dalla direzione di un segmento
    # passato come parametro oppure una lista vuota se non ci sono intersezioni
    def puntiIntersezioneRetta(self, s):
        """ restituisce i punti di intersezione (anche impropri) tra la frontiera del poligono corrente
            e una retta rappresentata dalla direzione di un segmento passato come parametr
        """
        intersez = gcListaPunti()
        for i in range(self.lunghezza()):
            lato = self.lato(i)
            p = lato.intersezioneRette(s, rette=True)
            if p != None:
                if intersez.haPunto(p) == False:
                    intersez.aggiungi(p)
        return intersez


    # ------------------------------------------------------------------------------------

    # aggiunge il poligono al grafico usando il modulo pyplot
    # lati = True disegna i punti come semplice lista senza unire i segmenti
    def plot(self, tipo='o-', colore='', colore_vertice='black', colore_lato='orange',
             stampa_etichette=True, autonumerazione=False, etichetta_vertici='P', colore_etichetta='', lati=True,
             riempimento=False, colore_riempimento='lightyellow', trasparenza_riempimento=1):
        """ traccia il poligono sul grafico
        """
        n = self.lunghezza()
        if n > 0:
            if colore != '':        # definisce il colore in blocco
                colore_vertice = colore
                colore_lato = colore
            if colore_etichetta == '':
                colore_etichetta = colore_vertice
            if riempimento == True:  # colora l'interno del poligono
                listax = [self[i].getx() for i in range(n)]
                listay = [self[i].gety() for i in range(n)]
                plt.fill(listax, listay, colore_riempimento, alpha=trasparenza_riempimento)
            for i in range(n):
                if lati == True:  # disegna il poligono (punti e lati)
                    s = self.lato(i)
                    s.plot(colore_segmento=colore_lato, colore_punto=colore_vertice, tipo=tipo)
                    if autonumerazione == True:
                        p = self.__v[i]
                        if stampa_etichette == True:
                            stringa_etichetta = f"${etichetta_vertici}_{{{i}}}$"
                        else:
                            stringa_etichetta = ''
                        p.plot(etichetta=stringa_etichetta, colore=colore_vertice, colore_etichetta=colore_etichetta, tipo=tipo)
                else:  # se lati=False disegna solo i punti (lista di punti)
                    p = gcPunto(self.__v[i])
                    if autonumerazione == True:
                        # le triple parentesi graffe servono per interpolare LaTeX dentro le f-string
                        p.plot(etichetta=stringa_etichetta, colore=colore_vertice, tipo=tipo, colore_etichetta=colore_etichetta)
                    else:
                        p.plot(colore=colore_vertice, tipo=tipo)
