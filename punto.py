from math import sqrt, isclose
import matplotlib.pyplot as plt
import seaborn   # pacchetto che aggiunge uno stile più moderno nella resa grafica
seaborn.set()    # avvia l'interfaccia grafica di seaborn

class gcPunto:
    """ classe di geometria computazionale in Python
        che definisce i punti 2D ed i relativi metodi primitivi
        autore: Giorgio Nordo - Dipartimento MIFT Università di Messina
        www.nordo.it   |  giorgio.nordo@unime.it
    """

    #----- variabili di classe
    __TOLLERANZA = 1e-5   # il valore della tolleranza assoluta da usare per i confronti numerici
    __precisione = 4      # il valore della precisione (numero dei decimali) nella rappresentazione dei punti

    # costruttore di un punto del piano
    # come coppia di coordinate
    # come oggetto punto
    # o come stringa di numeri separati da una virgola (eventualmente racchiusi tra parentesi)
    # (si utilizza una lista *args di parametri di lunghezza variabile)
    #TODO: aggiungere argomento passato anche come tupla
    def __init__(self, *args):
        """ crea un punto del piano da una coppia di coordinate,
            come copia di un altro oggetto punto o da una stringa
        """
        lunghezza = len(args)
        #------------------------------------------------------------------------
        if lunghezza == 2:  #---- costruisci il punto per mezzo delle coordinate
            x = float(args[0])  # ascissa del punto (o prima componente del vettore) in floating point
            y = float(args[1])  # ordinata del punto (o seconda componente del vettore) in floating point
            coord = (x,y)           # crea la coppia di coordinate come tupla
            self.__coord = coord    # memorizza privatamente la coppia (tupla) di coordinate appena creata
        # ------------------------------------------------------------------------
        elif lunghezza == 1:
            if type(args[0]) == gcPunto:  #---- crea una copia del punto come oggetto
                x = args[0].getx()
                y = args[0].gety()
                coord = (x,y)           # crea la coppia di coordinate come tupla
                self.__coord = coord    # memorizza privatamente la coppia di coordinate a
            # --------------------------------------------------------------------
            elif type(args[0]) == str:  #---- crea il punto a partire da una stringa
                testo = args[0]
                testo = testo.replace("(", "")
                testo = testo.replace(")", "")
                (x, y) = testo.strip().split(",")
                coord = (float(x), float(y))    # crea la coppia (tupla) di coordinate convertendo in float
                self.__coord = coord            # memorizza privatamente la coppia di coordinate a
        else:    # in tutti gli altri casi definisce delle coordinate nulle (punto vuoto)
            self.__coord = None


    # metodo che restituisce il punto come tupla
    def get(self):
        """ restituisce il punto come tupla
        """
        return self.__coord

    # metodo che restituisce la coordinata x di un punto
    def getx(self):
        """ restituisce l'ascissa x del punto
        """
        return self.__coord[0]

    # metodo che restituisce la coordinata y di un punto
    def gety(self):
        """ restituisce l'ordinata y del punto
        """
        return self.__coord[1]

    #------------------------------------------------------------------------------------

    # restituisce il punto come stringa col metodo speciale __str__
    def __str__(self):
        """ restituisce il punto in formato stringa (x,y) per l'utente
        """
        if self.__coord == None:    # punto nullo
            s = ''
        else:
            s = f"({round(self.getx(), gcPunto.getPrecisione())}, {round(self.gety(), gcPunto.getPrecisione())})"
        return s

    # restituisce la rappresentazione punto come stringa col metodo speciale __repr__
    # che viene implicitamente utilizzata nelle altre classi
    def __repr__(self):
        """ restituisce il punto in formato stringa (x,y) per le altre implementazioni
            (ad esempio per l'utilizzo in altre classi)
        """
        return str(self)

    #------------------------------------------------------------------------------------

    # metodo di classe che assegna la precisione (in termini di numero di cifre decimali)
    # della rappresentazione a video  delle coordinate dei punti (non il valore interno dei punti)
    @classmethod
    def setPrecisione(cls, precisione):
        """ assegna la precisione dei decimali delle coordinate dei punti
        """
        cls.__precisione = int(precisione)

    # metodo di classe che fornisce il valore della precisione (in termini di numero di cifre decimali)
    # della rappresentazione a video delle coordinate dei punti (non il valore interno dei punti)
    @classmethod
    def getPrecisione(cls):
        """ assegna la precisione dei decimali delle coordinate dei punti
        """
        return gcPunto.__precisione

    #------------------------------------------------------------------------------------

    # confronta due punti (con una certa approssimazione)
    # sovraccaricando l'operatore di uguaglianza ==
    # col metodo speciale __eq__
    def __eq__(self, pp):
        """ confronta due punti con l'uguale con approssimazione data da _TOLLERANZA
        """
        if pp != None:
            uguali = isclose(self.getx(), pp.getx(), abs_tol=gcPunto.__TOLLERANZA)   \
                 and isclose(self.gety(), pp.gety(), abs_tol=gcPunto.__TOLLERANZA)
            return uguali

    # confronta due punti (con una certa approssimazione)
    # sovraccaricando l'operatore di uguaglianza !=
    # col metodo speciale __ne__
    def __ne__(self, pp):
        """ confronta due punti col diverso con approssimazione data da _TOLLERANZA
        """
        differenti = not (self == pp)
        return differenti

    #------------------------------------------------------------------------------------

    # restituisce la somma di due punti sovraccaricando l'operatore di addizione +
    # col metodo speciale __add__
    def __add__(self, pp):
        """ addizione tra due punti
        """
        xx = self.getx() + pp.getx()
        yy = self.gety() + pp.gety()
        somma = gcPunto(xx, yy)
        return somma

    # restituisce la differenza di due punti sovraccaricando l'operatore di sottrazione -
    # col metodo speciale __sub__
    def __sub__(self, pp):
        """ sottrazione tra due punti
        """
        xx = self.getx() - pp.getx()
        yy = self.gety() - pp.gety()
        differenza = gcPunto(xx, yy)
        return differenza

    # restituisce il prodotto di un punto rappresentato come vettore
    # per uno scalare sovraccaricando l'operatore @ col metodo speciale __matmul__
    # secondo la forma v @ l (con v vettore o punto ed l scalare)
    def __matmul__(self, l):
        """ moltiplicazione v @ l tra un punto (o vettore) v e uno scalare l
        """
        xx = self.getx() * l
        yy = self.gety() * l
        prodotto = gcPunto(xx, yy)
        return prodotto

    # metodo che restituisce il modulo del punto
    def modulo(self):
        """ modulo di un punto (o di un vettore)
        """
        md = sqrt(self.getx() ** 2 + self.gety() ** 2)
        return md

    # restituisce la divisione di un punto rappresentato come vettore
    # per uno scalare sovraccaricando l'operatore / col metodo speciale __truediv__
    def __truediv__(self, l):
        """ divisione tra un punto (o vettore) e uno scalare
        """
        xx = self.getx() / l
        yy = self.gety() / l
        quoziente = gcPunto(xx, yy)
        return quoziente

    #------------------------------------------------------------------------------------

    # metodo che restituisce la distanza (euclidea) tra il punto corrente
    # ed un altro punto passato come parametro
    def distanza(self, pp):
        """ restituisce la distanza tra il punto corrente e un altro punto dato
        """
        dist = (self - pp).modulo()
        return dist

    # metodo statico che calcola la distanza euclidea tra due punti
    @staticmethod
    def d(p1, p2):
        """ restituisce la distanza tra due punti
        """
        return p1.distanza(p2)

    # metodo statico che calcola il
    # prodotto scalare di due vettori rappresentati come punti
    @staticmethod
    def prodottoScalare(p1, p2):
        """ restituisce il prodotto scalare tra due punti (o vettori)
        """
        prodscal = p1.getx() * p2.getx() + p1.gety() * p2.gety()
        return prodscal

    # restituisce il prodotto scalare di due vettori rappresentati come punti
    # sovraccaricando l'operatore di moltiplicazione * col metodo speciale __mul__
    def __mul__(self, pp):
        """ esegue il prodotto scalare
        """
        prodscal = self.prodottoScalare(self, pp)  # utilizza il metodo prodottoScalare già definito
        return prodscal

    #------------------------------------------------------------------------------------

    # restituisce true se i due vettori sono ortogonali
    # controllando (con una certa approssimazione) se il loro prodotto scalare è nullo
    def isOrtogonale(self, pp):
        """ test di ortogonalità tra il vettore corrente e un vettore dato
        """
        prodscal = self.prodottoScalare(self, pp)
        return isclose(prodscal, 0, abs_tol=gcPunto.__TOLLERANZA)

    # restituisce il vettore ortogonale (-y,x)
    def ortogonale(self):
        """ restituisce il vettore ortogonale (perp) a quello corrente
        """
        return gcPunto( - self.gety(), self.getx())

    # metodo statico che
    # restituisce il prodotto ortogonale (perp operator) di due vettori rappresentati come punti
    # si preferisce effettuare direttamente il calcolo
    @staticmethod
    def prodottoOrtogonale(p1, p2):
        """ restituisce il prodotto ortogonale di due vettori (o punti)
        """
        prodort = (p1.getx() * p2.gety() - p1.gety() * p2.getx())
        return prodort

    # restituisce true se i due vettori sono paralleli
    # controllando (con una certa approssimazione) se il loro prodotto ortogonale è nullo
    def isParallelo(self, pp):
        """ test di parallelismo tra due vettori
        """
        prodort = self.prodottoOrtogonale(self, pp)
        return isclose(prodort, 0, abs_tol=gcPunto.__TOLLERANZA)

    # metodo statico che restituisce l'area segnata di tre punti
    @staticmethod
    def areaSegnata(p0, p1, p2):
        """ restituisce l'area segnata di tre punti
        """
        a = gcPunto.prodottoOrtogonale(p1 - p0, p2 - p0)
        return a

    # metodo statico che restituisce l'area (NON segnata)
    # del triangolo individuato da tre punti
    @staticmethod
    def area(p0, p1, p2):
        """ restituisce l'area (non segnata) del triangolo
            individuato da tre punti
        """
        a = abs(gcPunto.areaSegnata(p0, p1, p2))/2
        return a

    # metodo statico che restituisce il punto medio di due punti
    @staticmethod
    def medio(p1, p2):
        """ restituisce il punto medio di due punti
        """
        m = (p1 + p2) / 2
        return m

    # metodo statico che restituisce il baricentro di una terna di punti
    @staticmethod
    def baricentro(p0, p1, p2):
        """ restituisce il baricentro di una terna di punti
        """
        b = (p0 + p1 + p2) / 3
        return b


    #------------------------------------------------------------------------------------

    # metodo che verifica la collinearità di un punto con altri due
    # passati come parametri restituendo true se i punti sono allineati
    def isCollineare(self, p1, p2):
        """ test di collinearità tra il punto corrente e altri due punti dati
            (ossia con la retta individuata dai due punti)
        """
        a = gcPunto.areaSegnata(self, p1, p2)
        return isclose(a, 0, abs_tol=gcPunto.__TOLLERANZA)

    # metodo statico che restituisce true se (con una certa approssimazione)
    # i tre punti sono allineati (o collineari)
    @staticmethod
    def collineari(p0, p1, p2):
        """ test di collinearità tra tre punti
        """
        return p0.isCollineare(p1, p2)

    # metodo statico che restituisce true se una terna ordinata di punti
    # è orientata in verso antiorario (CCW o counterclockwise)
    @staticmethod
    def CCW(p0, p1, p2):
        """ test di orientamento in verso antoriario CCW (o counterclockwise)
        """
        areasegn = gcPunto.areaSegnata(p0, p1, p2) > 0
        return areasegn

    # metodo statico che restituisce true se una terna ordinata di punti
    # è orientata in verso antiorario (CCW o counterclockwise)
    # o è formata da punti collineari
    @staticmethod
    def CCW_Collineari(p0, p1, p2):
        """ test di orientamento in verso antoriario CCW e collinearità
        """
        areasegn = gcPunto.areaSegnata(p0, p1, p2) >= 0
        return areasegn

    #------------------------------------------------------------------------------------

    # metodo statico che restituisce True se l'angolo in p1 è convesso (minore di 180°)
    # attenzione ai vettori
    @staticmethod
    def isConvesso(p0, p1, p2):
        """ test di convessità di un angolo
            (restituisce True se l'angolo è minore di 180°)
        """
        seno = gcPunto.prodottoOrtogonale(p1 - p0, p2 - p1)
        return (seno > 0)

    #------------------------------------------------------------------------------------

    # metodo statico che implementa l'ordinamento lessicografico verticale <=
    # il terzo parametro polo qui è inutile ma deve essere presente per uniformarsi
    # all'altro ordinamento polare che lo prevede
    @staticmethod
    def lessicograficoVerticale(p1, p2, polo=None):
        """ restituisce True se il primo punto p1 è minore o uguale del secondo punto p2
            rispetto all'ordinamento lessicografico verticale (<=)
        """
        mnrugl = ((p1.getx() < p2.getx())
                  or ((p1.getx() == p2.getx()) and (p1.gety() <= p2.gety())))
        return mnrugl

    # metodo statico che implementa l'ordinamento lessicografico verticale stretto <
    # il terzo parametro polo qui è inutile ma deve essere presente per uniformarsi
    # all'altro ordinamento polare che lo prevede
    @staticmethod
    def lessicograficoVerticaleStretto(p1, p2, polo=None):
        """ restituisce True se il primo punto p1 è strettamente minore del secondo punto p2
            rispetto all'ordinamento lessicografico verticale stretto (<)
        """
        mnr = ((p1.getx() < p2.getx())
               or ((p1.getx() == p2.getx()) and (p1.gety() < p2.gety())))
        return mnr

    #------------------------------------------------------------------------------------

    # metodo statico che implementa l'ordinamento lessicografico orizzontale <=
    # il terzo parametro polo qui è inutile ma deve essere presente per uniformarsi
    # all'ordinamento polare che lo prevede
    @staticmethod
    def lessicograficoOrizzontale(p1, p2, polo=None):
        """ restituisce True se il primo punto p1 è minore o uguale del secondo punto p2
            rispetto all'ordinamento lessicografico verticale (<=)
        """
        mnrugl = ((p1.gety() < p2.gety())
                  or ((p1.gety() == p2.gety()) and (p1.getx() <= p2.getx())))
        return mnrugl

    #------------------------------------------------------------------------------------

    # metodo statico che implementa l'ordinamento polare debole (col minore uguale)
    # rispetto ad un polo (opzionale) che per default coincide con l'origine
    # verificando che l'angolo del primo punto rispetto all'asse X
    # è minore dell'angolo del secondo punto
    # oppure, se gli angoli coincidono, se il primo punto è più vicino o uguale al polo
    # rispetto al secondo
    @staticmethod
    def polare(p1, p2, polo=None):
        """ restituisce True se il primo punto p1 è minore o uguale al secondo punto p2
            rispetto all'ordinamento polare relativo al polo
        """
        if polo is None:          # se il terzo parametro non viene passato
            polo = gcPunto(0,0)   # il polo viene assunto essere nell'origine
        q1 = p1 - polo    # considera i vettori differenza rispetto al polo specificato (origine per default)
        q2 = p2 - polo

        # se q1 e q2 si trovano in semipiani opposti dell'asse X
        # il minore è quello del semipiano positivo (o sinistro)
        if q1.gety() >= 0 and q2.gety() < 0:          # semipiani dell'asse X
            return True                               # il minore è q1  (q1<q2 è True)
        elif q1.gety() < 0 and q2.gety() >= 0:        # il minore è q2  (q1<q2 è False)
            return False

        # se q1 e q2 sono collineari col polo il minore è quello con la distanza più piccola dal polo
        if polo.isCollineare(p1, p2):

            # se q1 e q2 si trovano sull'asse Y
            if (q1.getx()==0 and q2.getx()==0):
                if q1.modulo() <= q2.modulo():  # d(polo,q1)<=d(polo,q2)  (q1<=q2 è True)
                    return True
                else:  # altrimenti q1<=q2 è False
                    return False

            # se q1 e q2 si trovano in semipiani opposti dell'asse Y
            # il minore è quello del semipiano positivo (o sinistro)
            if q1.getx() > 0 and q2.getx() < 0:  # semipiani dell'asse Y
                return True  # il minore è q1  (q1<q2 è True)
            elif q1.getx() < 0 and q2.getx() > 0:  # il minore è q2  (q1<q2 è False)
                return False

            # negli altri casi il minore è quello che ha la distanza più piccola dal polo
            elif q1.modulo() < q2.modulo():  # d(polo,q1)<=d(polo,q2)  (q1<=q2 è True)
                return True
            else:  # altrimenti q1<=q2 è False
                return False

        # se non sono collineari e si trovano sullo stesso semipiano coordinato
        # il maggiore è quello che svolta a destra (CCW) rispetto al polo ed all'altro punto
        if gcPunto.areaSegnata(polo, p1, p2) > 0 :  # p2 è nel semipiano sinistro di Op1
            return True                               # (q1<q2 è True)
        else:                                         # altrimenti q1<q2 è False
            return False


    # metodo statico che implementa l'ordinamento polare stretto
    # rispetto ad un polo (opzionale) che per default coincide con l'origine
    # verificando che l'angolo del primo punto rispetto all'asse X
    # è minore dell'angolo del secondo punto
    # oppure, se gli angoli coincidono, se il primo punto è più vicino al polo
    # rispetto al secondo
    @staticmethod
    def polareStretto(p1, p2, polo=None):
        """ restituisce True se il primo punto p1 è strettamente minore del secondo punto p2
            rispetto all'ordinamento polare stretto relativo al polo
        """
        if polo is None:          # se il terzo parametro non viene passato
            polo = gcPunto(0,0)   # il polo viene assunto essere nell'origine
        mnr = gcPunto.polare(p1, p2, polo) and not polo.isCollineare(p1, p2)
        return mnr

    #------------------------------------------------------------------------------------

    # metodo statico che implementa l'ordinamento del gift wrapping
    # rispetto ad un polo (opzionale) che per default coincide con l'origine
    # verificando che l'angolo del primo punto rispetto all'asse Y
    # è minore dell'angolo del secondo punto
    # (ossia se la terna ordinata di punti è orientata a destra)
    # oppure, se gli angoli coincidono, se il primo punto è più vicino al polo
    # rispetto al secondo
    @staticmethod
    def giftWrapping(p1, p2, polo=None):
        """ restituisce True se il primo punto p1 è strettamente minore del secondo punto p2
            rispetto all'ordinamento del gift wrapping
        """
        if polo is None:          # se il terzo parametro non viene passato
            polo = gcPunto(0,0)   # il polo viene assunto essere nell'origine
        q1 = p1 - polo    # considera i vettori differenza rispetto al polo specificato (origine per default)
        q2 = p2 - polo
        a= gcPunto.areaSegnata(polo, p1, p2)
        if a < 0 :  # p2 è nel semipiano destro di Op1
            return True
        elif a==0 :
            if q1.modulo() < q2.modulo():  # d(polo,q1)<=d(polo,q2)  (q1<=q2 è True)
                return True
            else:  # altrimenti q1<=q2 è False
                return False
        else:
            return False

    #------------------------------------------------------------------------------------

    # metodo statico che implementa l'ordinamento secondo le rette parallele
    # alla prima bisettrice dei quadranti (ossia alle rette di equazione x-y=k )
    # il terzo parametro polo qui è inutile ma deve essere presente per uniformarsi
    # all'altro ordinamento polare che lo prevede
    @staticmethod
    def primaBisettrice(p1, p2, polo=None):
        """ restituisce True se il primo punto p1 è strettamente minore del secondo punto p2
            rispetto all'ordinamento lungo le rette parallele alla prima bisettrice (x-y=k)
        """
        mnr = ( p1.getx() - p1.gety() < p2.getx() - p2.gety() )
        return mnr

    #------------------------------------------------------------------------------------

    # metodo statico che implementa l'ordinamento secondo le rette parallele
    # alla seconda bisettrice dei quadranti (ossia alle rette di equazione x+y=k )
    # il terzo parametro polo qui è inutile ma deve essere presente per uniformarsi
    # all'altro ordinamento polare che lo prevede
    @staticmethod
    def secondaBisettrice(p1, p2, polo=None):
        """ restituisce True se il primo punto p1 è strettamente minore del secondo punto p2
            rispetto all'ordinamento lungo le rette parallele alla seconda bisettrice (x+y=k)
        """
        mnr = (p1.getx() + p1.gety() < p2.getx() + p2.gety())
        return mnr

    # ------------------------------------------------------------------------------------

    # restituisce true se il primo punto è minore del secondo
    # rispetto all'ordinamento lessicografico verticale stretto
    # sovraccaricando l'operatore di minore col metodo speciale __lt__ (minore stretto < )
    def __lt__(self, pp):
        """ minore lessicografico verticale stretto (<) tra due punti
        """
        mnr = self.lessicograficoVerticaleStretto(self, pp)  # utilizza l'ordinamento lessicografico verticale stretto
        return mnr

    # restituisce true se il primo punto è minore del secondo
    # rispetto all'ordinamento lessicografico
    # sovraccaricando l'operatore di minore col metodo speciale __le__ (minore uguale <= )
    def __le__(self, pp):
        """ minore o uguale lessicografico verticale (<=) tra due punti
        """
        mnrugl = self.lessicograficoVerticale(self, pp)  # utilizza l'ordinamento lessicografico verticale
        return mnrugl

    #------------------------------------------------------------------------------------

    # aggiunge il punto al grafico usando il modulo pyplot
    def plot(self, tipo='o', etichetta='', colore='blue', colore_etichetta=''):
        """ traccia il punto sul grafico
        """
        if self.__coord != None:    # ci assicuriamo che il punto non sia nullo
            plt.plot([self.getx()], [self.gety()], tipo, color=colore)
            if etichetta != '':
                if colore_etichetta == '':
                    colore_etichetta = colore
                plt.text(self.getx(), self.gety(), '  '+etichetta, color=colore_etichetta)
