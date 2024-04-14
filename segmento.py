from pygc.punto import gcPunto
import matplotlib.pyplot as plt
import seaborn   # pacchetto che aggiunge uno stile più moderno nella resa grafica
seaborn.set()    # avvia l'interfaccia grafica di seaborn

class gcSegmento:
    """ classe di geometria computazionale in Python
        che definisce i segmenti nel piano ed i relativi metodi primitivi
        autore: Giorgio Nordo - Dipartimento MIFT Università di Messina
        www.nordo.it   |  giorgio.nordo@unime.it """

    # costruttore di un segmento del piano
    # per mezzo degli estremi (oggetti punto)
    # o come copia di un oggetto segmento
    # (si utilizza una lista *args di parametri di lunghezza variabile)
    def __init__(self, *args):
        """ crea un segmento del piano da una coppia di punti (estremi),
            da una o più stringhe o come copia di un altro oggetto segmento
        """
        lunghezza = len(args)
        #------------------------------------------------------------------------
        if lunghezza == 2:  # costruisci il segmento per mezzo dei suoi estremi (punti o stringhe)
            self.__p_inizio = gcPunto(args[0])   # estremo iniziale
            self.__p_fine = gcPunto(args[1])     # estremo finale
        #------------------------------------------------------------------------
        elif lunghezza == 1:
            if type(args[0]) == gcSegmento:  # crea una copia del segmento come oggetto
                self.__p_inizio = args[0].getInizio()
                self.__p_fine = args[0].getFine()
        #------------------------------------------------------------------------
            elif type(args[0] == str) : # crea un segmento da una stringa dal formato [(x1,y1), (x2,y2)]
                s = args[0]
                car_da_rimuovere = ('[', ']', '(', ')')
                for c in car_da_rimuovere :    # elimina i caratteri superflui
                    s = s.replace(c, '')
                comp = s.split(',')
                self.__p_inizio = gcPunto(float(comp[0]), float(comp[1]))
                self.__p_fine = gcPunto(float(comp[2]), float(comp[3]))
        #------------------------------------------------------------------------
        else:  # in tutti gli altri casi definisce degli estremi nulli
            self.__p_inizio = gcPunto()
            self.__p_fine = gcPunto()


    # restituisce il punto estremo iniziale del segmento
    def getInizio(self):
        """ restituisce l'estremo iniziale
        """
        return self.__p_inizio

    # restituisce il punto estremo finale del segmento
    def getFine(self):
        """ restituisce l'estremo finale del segmento
        """
        return self.__p_fine

    # restituisce il punto medio del segmento
    def getMedio(self):
        """ restituisce il punto medio del segmento corrente
        """
        m = (self.getInizio() + self.getFine()) / 2
        return m


    #------------------------------------------------------------------------------------

    # restituisce la direzione del segmento come:
    # x = parallela all'asse X
    # y = parallela all'asse Y
    # 1 = primo e terzo quadrante
    # 2 = secondo e quarto quadrante
    def direzione(self):
        """ direzione del segmento
        """
        dx = self.getFine().getx() - self.getInizio().getx()
        dy = self.getFine().gety() - self.getInizio().gety()
        if dx == 0:
            direz = 'y'
        elif dy == 0:
            direz = 'x'
        elif dx*dy > 0:
            direz = '1'
        else:            # se dx*dy <
            # 0
            direz = '2'
        return direz

    # restituisce il verso del segmento come:
    # a = verso l'alto
    # b = verso il basso
    def verso(self):
        """ verso del segmento
        """
        dx = self.getFine().getx() - self.getInizio().getx()
        if dx != 0 :
            if dx > 0:
                vrs = 'c'
            else:
                vrs = 'd'
        else:     # se dx == 0
            dy = self.getFine().gety() - self.getInizio().gety()
            if dy > 0:
                vrs = 'c'
            else:
                vrs = 'd'
        return vrs

    #------------------------------------------------------------------------------------

    # restituisce il segmento di verso opposto
    def opposto(self):
        """ restituisce il segmento di verso opposto
        """
        s_o = gcSegmento(self.__p_fine, self.__p_inizio)
        return s_o

    # inverti il verso del segmento corrente
    # cioè modifica il segmento corrente nel suo opposto
    def inverti(self):
        """ modifica il verso del segmento corrente
        """
        (self.__p_inizio, self.__p_fine) = (self.__p_fine, self.__p_inizio)

    #------------------------------------------------------------------------------------

    # restituisce il segmento come stringa col metodo speciale __str__
    def __str__(self):
        """ restituisce il segmento in formato stringa [p,q] per l'utente
        """
        s = f"[{self.getInizio()}, {self.getFine()}]"
        return s

    # restituisce la rappresentazione segmento come stringa col metodo speciale __repr__
    # che viene implicitamente utilizzata nelle altre classi
    def __repr__(self):
        """ restituisce il segmento in formato stringa [p,q] per le altre implementazioni
            (ad esempio per l'utilizzo in altre classi)
        """
        return str(self)

    #------------------------------------------------------------------------------------

    # confronta due segmenti (con una certa approssimazione)
    # sovraccaricando l'operatore di uguaglianza ==
    # col metodo speciale __eq__
    def __eq__(self, ss):
        """ confronta due segmenti con l'uguale con approssimazione data da _TOLLERANZA
        """
        uguali = self.getInizio() == ss.getInizio() and self.getFine() == ss.getFine()
        return uguali

    # confronta due segmenti (con una certa approssimazione)
    # sovraccaricando l'operatore di uguaglianza !=
    # col metodo speciale __ne__
    def __ne__(self, ss):
        """ confronta due poligoni col diverso con approssimazione data da _TOLLERANZA
        """
        differenti = not (self == ss)
        return differenti


    #------------------------------------------------------------------------------------

    # restituisce il tipo di posizione di un punto rispetto al segmento corrente
    # e precisamente classificandoli come:
    # - inizio = se il punto coincide con l'estremo iniziale del segmento
    # - fine = se il punto coincide con l'estremo finale del segmento
    # - sinistra = se il punto si trova nel semipiano sinistro aperto individuato dal segmento
    # - destra = se il punto si trova nel semipiano destro aperto individuato dal segmento
    # - indietro = se si trova sulla retta passante per il segmento prima del suo estremo iniziale
    # - avanti = se si trova sulla retta passante per il segmento dopo il suo estremo finale
    # - interno = se il punto è interno al segmento
    # DA CONTROLLARE ESATTAMENTE IN QUEST'ORDINE (in-fi-si-de-ind-ava-int)
    def posizione(self, p):
        """ restituisce la posizione di un punto rispetto al segmento corrente
            classificandolo in inizio, fine, sinistra, destra, indietro, avanti o interno
        """
        pos = ''
        if p == self.getInizio():     # casi banali di coincidenza con gli estremi del segmento
            pos = 'inizio'
        elif p == self.getFine():
            pos = 'fine'
        else:
            areasegnata = gcPunto.areaSegnata(self.__p_inizio, self.__p_fine, p)
            if areasegnata > 0:   # casi banali di non collinearità e di appartenenza ad uno dei due semipiani
                pos = 'sinistra'
            elif areasegnata < 0:
                pos = 'destra'
            else:    # se l'area segnata è nulla, cioè se il punto è allineato col segmento
                     # si hanno casi di collinearità non banali da valutare con le distanze (o moduli)
                p_i = self.getInizio()
                p_f = self.getFine()
                # se almeno una delle due componenti dei vettori differenza
                # p_i p_f e p_i p  ha segno discorde è indietro
                if ((p_f - p_i).getx() * (p - p_i).getx() < 0) or ((p_f - p_i).gety() * (p - p_i).gety() < 0) :
                    pos = 'indietro'
                # # se la distanza di p dall'estremo iniziale è maggiore della distanza tra gli estremi
                elif (p_f - p_i).modulo() < (p - p_i).modulo():
                    pos = 'avanti'
                else:       # nell'unico caso restante non può che essere interno al segmento
                    pos = 'interno'
        return pos


    #------------------------------------------------------------------------------------

    # restituisce True se il segmento corrente contiene al suo interno
    # (anche impropriamente estremo iniziale incluso, estremo finale escluso)
    # un punto passato come parametro
    def contiene(self, p):
        """ restituisce True se il punto passato come parametro
            è interno (anche impropriamente) al segmento corrente
        """
        return self.posizione(p) in {'inizio', 'interno'}    #, 'fine'}  RIMOSSO per non inludere l'estremo finale


    #------------------------------------------------------------------------------------

    # restituisce true se il punto si trova nel semipiano sinistro chiuso
    # individuato dal segmento corrente cioè se la terna orientata di punti
    # formata dagli estremi iniziale e finale del segmento e dal punto p
    # è orientata in verso antiorario
    def semipianoSinistroChiusoContiene(self, p):
        """ restituisce True se il punto p si trova nel semipiano sinistro
            individuato dal segmento corrente
        """
        return self.posizione(p) != 'destra'

    # restituisce true se il punto si trova nell'interno semipiano sinistro
    # individuato dal segmento corrente cioè se la terna orientata di punti
    # formata dagli estremi iniziale e finale del segmento e dal punto p
    # è orientata in verso antiorario
    def semipianoSinistroContiene(self, p):
        """ restituisce True se il punto p si trova nell'interno del semipiano sinistro
            individuato dal segmento corrente
        """
        return self.posizione(p) == 'sinistra'


    #------------------------------------------------------------------------------------

    # restituisce true se il segmento corrente ha intersezione propria con un altro segmento
    # cioè se si intersecano solo i loro interni escludendo gli estremi
    def intersecaPropriamente(self, s):
        """ verifica se il segmento corrente interseca propriamente un altro segmento
        """
        (p1, p2) = (self.__p_inizio, self.__p_fine)   # troviamo gli estremi dei due segmenti
        (q1, q2) = (s.getInizio(), s.getFine())
        as_q1 = gcPunto.areaSegnata(p1,p2,q1)         # calcoliamo le quattro aree segnate
        as_q2 = gcPunto.areaSegnata(p1,p2,q2)
        as_p1 = gcPunto.areaSegnata(q1,q2,p1)
        as_p2 = gcPunto.areaSegnata(q1,q2,p2)
        intersez= (as_q1 * as_q2 < 0) and (as_p1 * as_p2 < 0)
        return intersez


    # restituisce true se il segmento corrente ha intersezione anche impropria con un altro segmento
    # cioè se si intersecano i loro interni con l'estremo iniziale incluso e l'estremo finale escluso
    def interseca(self, s):
        """ verifica se il segmento corrente interseca (anche impropriamente) un altro segmento
        """
        (p1, p2) = (self.__p_inizio, self.__p_fine)   # troviamo gli estremi dei due segmenti
        (q1, q2) = (s.getInizio(), s.getFine())
        #---- calcoliamo le quattro aree segnate
        as_q1 = gcPunto.areaSegnata(p1,p2,q1)         # nullo se p1p2 interseca l'estremo iniziale q1 di q1q2
        as_q2 = gcPunto.areaSegnata(p1,p2,q2)
        as_p1 = gcPunto.areaSegnata(q1,q2,p1)         # nullo se q1q2 interseca l'estremo iniziale p1 di p1p2
        as_p2 = gcPunto.areaSegnata(q1,q2,p2)
        intersez =    ( (as_q1 * as_q2 <= 0) and (as_p1 * as_p2 < 0) )   \
                   or ( (as_q1 * as_q2 < 0) and (as_p1 * as_p2 <= 0) )   \
                   or  (p1==q1)   # per includere il caso in cui l'estremo iniziale del primo segmento coincida con quello del secondo
        return intersez


    # # calcola il punto di intersezione del segmento corrente (considerato anche come direzione di una retta)
    # # con un altro segmento (o retta) o restituisce None se i due segmenti non si intersecano
    # # o sono collineari e sovrapposti in tutto o in parte
    # # se il parametro posizionale rette ha il valore True
    # # i segmenti vengono interpretati come direzioni di rette
    # # e se queste rette risultano incidenti viene restituito il loro punto di intersezione
    # # (anche se i segmenti che rappresentano le rette sono disgiunti)
    # # def intersezioneRette
    # # (self, s, rette=False):
    # def intersezione(self, s, retta=False):
    #     """ restituisce l'intersezione del segmento corrente (considerato anche come direzione di retta)
    #         con un altro segmento (o direzione di retta) come oggetto punto
    #         oppure None se non si intersecano o se l'intersezione è un segmento
    #         (cioè se sono sovrapposti in tutto o in parte)
    #         - se il parametro rette ha il valore True viene restituito il punto di intersezione
    #           delle rette su cui giacciono i duesegmenti
    #     """
    #     if self.interseca(s) == False and retta == False:
    #         return None
    #     else:
    #         (p1, p2) = (self.__p_inizio, self.__p_fine)   # calcolo degli estremi
    #         (q1, q2) = (s.getInizio(), s.getFine())
    #         u = p2 - p1   # u=p1p2
    #         v = q2 - q1   # v=q1q2
    #         w = p1 - q1   # w=q1p1
    #         v_ort = v.ortogonale()
    #         denom = v_ort * u    # con * prodotto scalare
    #         if denom == 0:          # se il prodotto orgonale di v e u è nullo
    #             return None         # le rette sono parallele e viene restituito None
    #         else:
    #             t_0 = - (v_ort * w) / (v_ort * u)
    #             pp = p1 + u @ t_0    # con @ prodotto vettore per scalare
    #             return pp

    # calcola il punto di intersezione del segmento corrente
    # con un altro segmento o restituisce None se i due segmenti non si intersecano
    # o sono collineari e sovrapposti in tutto o in parte
    def intersezione(self, s):
        """ restituisce l'intersezione del segmento corrente con un altro segmento come oggetto punto
            oppure None se non si intersecano o se l'intersezione è un segmento
            (cioè se sono sovrapposti in tutto o in parte)
        """
        (p1, p2) = (self.__p_inizio, self.__p_fine)   # calcolo degli estremi
        (q1, q2) = (s.getInizio(), s.getFine())
        u = p2 - p1   # u=p1p2
        v = q2 - q1   # v=q1q2
        w = p1 - q1   # w=q1p1
        v_ort = v.ortogonale()
        denom = v_ort * u    # con * prodotto scalare
        if denom == 0:          # se il prodotto orgonale di v e u è nullo
            return None         # le rette sono parallele e viene restituito None
        else:
            t_0 = - (v_ort * w) / (v_ort * u)
            pp = p1 + u @ t_0    # con @ prodotto vettore per scalare
            return pp


    # calcola il punto di intersezione del segmento corrente (considerato anche come direzione di una retta)
    # con un altro segmento (o retta) o restituisce None se i due segmenti non si intersecano
    # o sono collineari e sovrapposti in tutto o in parte
    # se il parametro posizionale rette ha il valore True
    # i segmenti vengono interpretati come direzioni di rette
    # e se queste rette risultano incidenti viene restituito il loro punto di intersezione
    # (anche se i segmenti che rappresentano le rette sono disgiunti)
    def intersezioneRette(self, s, rette=False):
        """ restituisce l'intersezione del segmento corrente (considerato anche come direzione di retta)
            con un altro segmento (o direzione di retta) come oggetto punto
            oppure None se non si intersecano o se l'intersezione è un segmento
            (cioè se sono sovrapposti in tutto o in parte)
            - se il parametro rette ha il valore True viene restituito il punto di intersezione
              delle rette su cui giacciono i duesegmenti
        """
        if self.interseca(s) == False and rette == False:
            return None
        else:
            (p1, p2) = (self.__p_inizio, self.__p_fine)   # calcolo degli estremi
            (q1, q2) = (s.getInizio(), s.getFine())
            u = p2 - p1   # u=p1p2
            v = q2 - q1   # v=q1q2
            w = p1 - q1   # w=q1p1
            v_ort = v.ortogonale()
            denom = v_ort * u    # con * prodotto scalare
            if denom == 0:          # se il prodotto orgonale di v e u è nullo
                return None         # le rette sono parallele e viene restituito None
            else:
                t_0 = - (v_ort * w) / (v_ort * u)
                pp = p1 + u @ t_0    # con @ prodotto vettore per scalare
                return pp



    # restituisce True se il segmento corrente (visto come vettore)
    # è parallalelo al segmento passato come parametro
    def parallelo(self, s):
        """ verifica se il segmento corrente è parallelo a quello passato come parametro
        """
        v1 = self.getFine() - self.getInizio()
        v2 = s.getFine() - s.getInizio()
        return v1.isParallelo(v2)


    # restituisce True se la retta individuata dalla direzione del segmento corrente
    # è incidente (cioè interseca, ossia non è parallela) alla retta individuata dalla direzione del segmento passato come parametro
    # o restituisce True anche se i segmenti individuano la stessa retta
    def incidente(self, s):
        """ verifica se la retta avente la direzione del segmento corrente è incidente
            alla retta avente la direzione del segmento passato come parametro
            restituisce True anche se i due segmenti individuano la stessa retta
        """
        if self.parallelo(s) == True:
            p1 = self.getInizio()
            p2 = self.getFine()
            q = s.getInizio()
            if q.isCollineare(p1,p2) == True :
                return True    # rette parallele e coincidenti (perché collineari)
            else:
                return False   # rette parallele e distinte, quindi non incidenti
        else:
            return True        # rette non parallele, quindi incidenti

    # ------------------------------------------------------------------------------------

    # aggiunge il segmento al grafico usando il modulo pyplot
    def plot(self, tipo='o-', colore='', colore_segmento='green', colore_punto='black',
             etichetta_inizio='', etichetta_fine='', colore_etichetta='',
             estremi=True, etichetta_segmento=''):
        """ traccia il segmento sul grafico
        """
        if colore != '':        # definisce il colore in blocco
            colore_segmento = colore
            colore_punto = colore
        # traccia i segmenti
        plt.plot([self.getInizio().getx(), self.getFine().getx()],
                 [self.getInizio().gety(), self.getFine().gety()], tipo, color=colore_segmento)
        # traccia gli estremi
        if estremi == True :
            self.getInizio().plot(colore=colore_punto, etichetta=etichetta_inizio, tipo=tipo)
            self.getFine().plot(colore=colore_punto, etichetta=etichetta_fine, tipo=tipo)
        # aggiungi l'eventuale etichetta del segmento
        if etichetta_segmento != '':
            puntomedio = self.getMedio()
            if colore_etichetta == '':
                colore_etichetta = colore_segmento
            plt.text(puntomedio.getx(), puntomedio.gety(), '  ' + etichetta_segmento, color=colore_etichetta)
