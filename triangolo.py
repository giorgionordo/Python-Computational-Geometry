from pygc.punto import gcPunto
from pygc.segmento import gcSegmento
from pygc.listapunti import gcListaPunti
from pygc.poligono import gcPoligono
import matplotlib.pyplot as plt
import seaborn   # pacchetto che aggiunge uno stile più moderno nella resa grafica
seaborn.set()    # avvia l'interfaccia grafica di seaborn


class gcTriangolo:
    """ classe di geometria computazionale in Python
        che definisce i triangoli nel piano ed i relativi metodi primitivi
        autore: Giorgio Nordo - Dipartimento MIFT Università di Messina
        www.nordo.it   |  giorgio.nordo@unime.it """

    # costruttore di un triangolo del piano
    # per mezzo degli estremi (oggetti punto),
    # come copia di un oggetto triangolo
    # o come copia di un oggetto poligono (purché costituito da tre vertici)
    # (si utilizza una lista *args di parametri di lunghezza variabile)
    def __init__(self, *args):
        """ crea un triangolo del piano da una terna di punti,
            o come copia di un altro oggetto segmento
        """
        lunghezza = len(args)
        #------------------------------------------------------------------------
        if lunghezza == 3:  # costruisci il triangolo per mezzo dei suoi tre vertici
            self.__t = [gcPunto(args[0]), gcPunto(args[1]), gcPunto(args[2])]
        #------------------------------------------------------------------------
        elif lunghezza == 1:
            if type(args[0]) == gcTriangolo:  # crea una copia del triangolo come oggetto
                self.__t = [args[0].vertice(1), args[0].vertice(2), args[0].vertice(3)]
        #------------------------------------------------------------------------
            elif type(args[0]) == gcPoligono:  # crea una copia del triangolo dal poligono
                if len(args[0]) == 3 :    # purché abbia esattamente tre vertici
                    self.__t = [args[0].vertice(0), args[0].vertice(1), args[0].vertice(2)]
        #------------------------------------------------------------------------
            elif type(args[0] == str) : # crea un triangolo da una stringa del tipo <(x1,y1), (x2,y2), (x3,y3)>
                s = args[0]
                car_da_rimuovere = ('<', '>', '(', ')')
                for c in car_da_rimuovere :    # elimina i caratteri superflui
                    s = s.replace(c, '')
                comp = s.split(',')
                v1 = gcPunto(float(comp[0]), float(comp[1]))
                v2 = gcPunto(float(comp[2]), float(comp[3]))
                v3 = gcPunto(float(comp[4]), float(comp[5]))
                self.__t = [v1, v2, v3]

    # ------------------------------------------------------------------------------------

    # restituisce il vertice di indice i (con i=1,2,3) del triangolo come oggetto punto
    # estendendo l'operatore di indicizzazione col metodo speciale __getitem__
    def __getitem__(self, i):
        """ restituisce l'i-esimo vertice del triangolo (con i=1,2,3)
        """
        if i in (1,2,3) :
            return self.__t[i-1]
        elif i == 4 :
            return self.__t[0]

    # restituisce il vertice del triangolo di indice i (con i=1,2,3
    def vertice(self, i):
        """ restituisce l'i-esimo vertice del triangolo (con i=1,2,3)
        """
        return self[i]   # utilizza l'overload di __getitem__ per gcPUnto definito sopra

    # ------------------------------------------------------------------------------------

    # restituisce il triangolo come stringa col metodo speciale __str__
    def __str__(self):
        """ restituisce il triangolo in formato stringa <p,q,r> per l'utente
        """
        s = f"< {self.vertice(1)}, {self.vertice(2)}, {self.vertice(3)} >"
        return s

    # restituisce la rappresentazione triangolo come stringa col metodo speciale __repr__
    # che viene implicitamente utilizzata nelle altre classi
    def __repr__(self):
        """ restituisce il triangolo in formato stringa per le altre implementazioni
            (ad esempio per l'utilizzo in altre classi)
        """
        return str(self)

    #------------------------------------------------------------------------------------

    # confronta due triangoli (con una certa approssimazione)
    # sovraccaricando l'operatore di uguaglianza ==
    # col metodo speciale __eq__
    def __eq__(self, tt):
        """ confronta due triangoli con l'uguale con approssimazione data da _TOLLERANZA
        """
        # consideriamo due poligoni costituiti dai vertici dei due triangoli
        pol1 = gcPoligono([self.vertice(1), self.vertice(2), self.vertice(3)])
        pol2 = gcPoligono([tt.vertice(1), tt.vertice(2), tt.vertice(3)])
        # ordina i punti per poterli confrontare in maniera appropriata
        pol1 = pol1.ordina(ordinamento=gcPunto.lessicograficoOrizzontale)
        pol2 = pol2.ordina(ordinamento=gcPunto.lessicograficoOrizzontale)
        # confronta i triangoli come particolari poligoni
        uguali = (pol1==pol2)
        return uguali

    # confronta due triangoli (con una certa approssimazione)
    # sovraccaricando l'operatore di uguaglianza !=
    # col metodo speciale __ne__
    def __ne__(self, tt):
        """ confronta due triangoli col diverso con approssimazione data da _TOLLERANZA
        """
        differenti = not (self == tt)
        return differenti

    #------------------------------------------------------------------------------------

    # restituisce come segmento l-iesimo lato del triangolo (con i=1,2,3)
    def lato(self, i):
        """ restituisce il lato che ha estremo iniziale nel vertice di indice i (con i=1,2,3)
        """
        if i in (1,2,3) :
            p1 = self.vertice(i)
            p2 = self.vertice(i+1)
            s = gcSegmento(p1, p2)
            return s
        else:
            return None

    # restituisce True se i tre vertici sono allineati e il triangolo è degenere
    def isDegenere(self):
        """ restituisce True se il triangolo è genere
            cioè se i tre vertici sono collineari
        """
        return gcPunto.collineari(self.vertice(1), self.vertice(2), self.vertice(3))

    # orienta i vertici in verso antiorario (CCW) rispetto al primo vertice
    def orientaCCW(self):
        """ orienta i vertici del triangolo in verso antiorario (CCW)
            rispetto al primo vertice
        """
        v1 = self.vertice(1)
        v2 = self.vertice(2)
        v3 = self.vertice(3)
        if gcPunto.CCW(v1,v2,v3) == False :   # se i vertici NON sono in verso antiorario
            self.__t[1] = v3
            self.__t[2] = v2

    # orienta i vertici in verso orario (CW) rispetto al primo vertice
    def orientaCW(self):
        """ orienta i vertici del triangolo in verso orario (CW)
            rispetto al primo vertice
        """
        v1 = self.vertice(1)
        v2 = self.vertice(2)
        v3 = self.vertice(3)
        if gcPunto.CCW(v1,v2,v3) == True :   # se i vertici sono inverso antiorario
            self.__t[1] = v3
            self.__t[2] = v2

    # semplifica il triangolo riordinando opportunamente i vertici
    # ossia scegliendo il primo vertice come il minimo rispetto all'ordinamento
    # lessicografico orizzontale dei tre e ordinando gli altri due in verso antiorario (CCW)
    def semplifica(self):
        """ riordina i vertici del triangolo scegliendo il primo
            come minimo lessicografico orizzontale
            e ordinando gli altri due in verso antiorario
        """
        # consideriamo il poligono costituito dai vertici del rtriangolo
        pol = gcPoligono([self.vertice(1), self.vertice(2), self.vertice(3)])
        # ordiniamo i punti rispetto all'ordinamento lessicografico orizzontale
        pol = pol.ordina(ordinamento=gcPunto.lessicograficoOrizzontale)
        # assegniamo i punti in quest'ordine al triangolo
        self.__t = [pol[0], pol[1], pol[2]]
        # orientiamo gli altri due punti in verso antiorario lasciando invariato il primo
        self.orientaCCW()

    # restituisce il poligono (convesso) corrispondente al triangolo semplificato
    # col primo vertice corrispondente al minimo lessicografico orizzontale
    # e gli altri due orientati in verso antiorario (CCW)
    def toPoligono(self):
        """ converte il triangolo in un oggetto di tipo poligono
        """
        tt = gcTriangolo(self)
        tt.semplifica()
        pol = gcPoligono([tt.vertice(1), tt.vertice(2), tt.vertice(3)])
        return pol

    # ------------------------------------------------------------------------------------

    # restituisce True se il punto è un vertice del triangolo
    def haVertice(self, p):
        """ restituisce true se il punto p è un vertice del triangolo
        """
        p = gcPunto(p)  # converti il parametro in oggetto punto in caso sia una stringa
        havert = p in self.__t
        return havert

    # restituisce True se il punto appartiene al triangolo
    # col metodo speciale __contains__ che sovrascrive l'operatore in
    # sia che venga passato come oggetto di tipo gcPunto o come stringa
    # richiamando il metodo haVertice
    def __contains__(self, p):
        """ verifica se il punto p è un vertice del triangolo
        """
        return self.haVertice(p)

    # restituisce True se il triangolo contiene un segmento come suo lato
    # sia che venga passato come oggetto di tipo gcSegmento
    # sia che venga passato come stringa (nel qual caso viene prima convertito)
    # il valore False del parametro verso fa si che il segmento venga considerato lato
    # anche se fornito in verso opposto
    def haLato(self, s, verso=True):
        """ verifica se segmento s è un lato del triangolo
            con verso=False ci considera lato anche un segmento di verso opposto
        """
        s = gcSegmento(s)  # converti il parametro in oggetto segmento in caso sia una stringa
        halato = False
        for i in range(1,4):
            if self.lato(i) == s :
                halato = True
            elif verso == False and self.lato(i) == s.opposto() :
                halato = True
        return halato

    # metodo che restituisce True se il triangolo fornito come parametro è adiacente a quello corrente
    # ossia se condividono un solo lato ovvero se hanno esattamente due vertici in comune
    # si noti che questa condizione di adiacenza NON ESCLUDE che uno dei due triangoli
    # possa essere contenuto dentro l'altro
    def adiacente(self, tt):
        """ restituisce True se il triangolo è adiacente a quello corrente
            cioè se condivide un lato
        """
        numvertici = 0
        for i in range(1,4):
            for j in range(1,4):
                if self.vertice(i) == tt.vertice(j):
                    numvertici += 1
        if numvertici == 2 :
            return True
        else :
            return False

    # determina la posizione di un punto rispetto al triangolo classificandolo come:
    # - interno
    # - esterno
    # - vertice se coincide con uno dei vertici
    # - lato se giace su uno dei lati
    def posizione(self, p):
        # ottiene il poligono convesso corrispondente al triangolo
        pol = self.toPoligono()
        if pol.puntoInPoligonoConvesso(p) :
            return 'interno'
        elif p in self :
            return 'vertice'
        elif pol.puntoInFrontiera(p) :
            return 'lato'
        else :
            return 'esterno'

    # restituisce True se il triangolo passato come parametro
    # ha intersezione non vuota con quello corrente
    def interseca(self, tt):
        """ restituisce True se il triangolo passato come parametro
            interseca quello corrente
        """
        intersez = False
        # verifica l'intersezione (anche impropria) tra i segmenti dei due triangoli
        for i in range(1,4):
            li = self.lato(i)
            for j in range(1,4):
                lj = tt.lato(j)
                if li.interseca(lj):
                    intersez = True
                    break
        if intersez == False :
            # anche in mancanza di intersezioni tra lati
            # verifica se uno dei due triangoli è interno all'altro
            # controllando se tutti e tre i punti dell'uno sono interni all'altro
            # ----- verifica se il triangolo passato come parametro è interno a quello corrente
            tutti_interni = True
            for i in range(1,4) :
                if self.posizione(tt.vertice(i)) == 'esterno' :
                    tutti_interni = False
                    break
            if tutti_interni == True :
                intersez = True
            else :
                # ----- verifica se il triangolo corrente è interno a quello passato come parametro
                tutti_interni = True
                for i in range(1, 4):
                    if tt.posizione(self.vertice(i)) == 'esterno':
                        tutti_interni = False
                        break
                if tutti_interni == True :
                    intersez = True
        return intersez

    # ------------------------------------------------------------------------------------

    # restituisce il baricentro del triangolo come oggetto di tipo punto
    # utilizzando l'omonimo metodo statico della classe gcPunto
    def baricentro(self):
        """ restituisce il baricentro del triangolo
        """
        b = gcPunto.baricentro(self.vertice(1), self.vertice(2), self.vertice(3))
        return b

    # restituisce l'area del triangolo
    def area(self):
        """ restituisce l'area del triangolo
        """
        area = gcPunto.area(self.vertice(1), self.vertice(2), self.vertice(3))
        return area


    # ------------------------------------------------------------------------------------

    # aggiunge il triangolo al grafico usando il modulo pyplot
    def plot(self, tipo='o-', colore='', colore_lato='green', colore_vertice='black',
             autonumerazione=False, etichetta_vertici='P', etichetta_triangolo='',
             riempimento=False, colore_riempimento='lightyellow', trasparenza_riempimento=1):
        """ traccia il triangolo sul grafico
        """
        if colore != '':        # definisce il colore in blocco
            colore_vertice = colore
            colore_lato = colore
        # traccia i segmenti
        if riempimento == True:  # colora l'interno del triangolo
            listax = [self.__t[0].getx(), self.__t[1].getx(), self.__t[2].getx()]
            listay = [self.__t[0].gety(), self.__t[1].gety(), self.__t[2].gety()]
            plt.fill(listax, listay, colore_riempimento, alpha=trasparenza_riempimento)
        for i in range(1,4) :
            s = self.lato(i)
            s.plot(colore_segmento=colore_lato, colore_punto=colore_vertice, tipo=tipo)
            if etichetta_triangolo != '':
                baricentro = self.baricentro()
                plt.text(baricentro.getx(), baricentro.gety(), '  ' + etichetta_triangolo, color=colore_lato)
            if autonumerazione == True:
                p = self.vertice(i)
                # le triple parentesi graffe servono per interpolare LaTeX dentro le f-string
                p.plot(etichetta=f"${etichetta_vertici}_{{{i}}}$", colore=colore_vertice)
