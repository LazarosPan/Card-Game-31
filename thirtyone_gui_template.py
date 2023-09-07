#31gui 3/18
''' απλοποιημένη έκδοση του 31. Παίζουν 2 o υπολογιστής και ο παίκτης. Ο υπολογιστής παίζει πρώτος., ο κάθε παίκτης
τραβάει διαδοχικά 'φύλλα'. Στόχος είναι να πετύχει όσο το δυνατόν υψηλότερο συνολικό σκορ. Αν το συνολικό του σκορ
περάσει όμως το 31 καίγεται.
Κερδίζει ο παίκτης που έχει το υψηλότερο σκορ σε κάθε γύρο
'''
import PlayingCards as pc
from thirtyone import Player, Game # εισάγουμε τις κλάσεις Player, Game από την αρχική έκδοση του παιχνιδιού
import tkinter as tk
import os
from tkinter import simpledialog
import pickle
import random

class GUICard():
    '''κλάση που γνωρίζει και τη γραφική ταυτότητα της card'''
    theCards = {}
    def __init__(self, card, canvas):
        self.canvas = canvas
        self.value = card.value
        self.symbol = card.symbol
        self.position = None
        self.image = None
        GUICard.theCards[card] = self
    def _fetch_image(self):
        if self.face:
            return CardImages.images[self.symbol][pc.Deck.values.index(self.value)]
        else: return CardImages.images['b']
    def _animate_image(self):
        self.canvas.move(self.image, self.img_vx, self.img_vy)
        x1,y1,x2,y2 = self.canvas.bbox(self.image)
        if abs(x1 - self.position[0]) < 5 and abs(y1 - self.position[1]) < 5:
            return
        else:
            self.canvas.update_idletasks()
            self.canvas.after(20, self._animate_image)
    def set_face(self, face):
        if self.position and face != self.face:
            self.face = face
            self.canvas.itemconfig(self.image, image= self._fetch_image())
        else:
            self.face = face
    def move_to(self, new_position):
        if not self.position: self.position = new_position
        if not self.image:
            self.image = self.canvas.create_image(*self.position, image =  self._fetch_image())
        self.canvas.itemconfig(self.image, anchor='nw')
        if new_position != self.position:
            self.img_vx = (new_position[0] - self.position[0]) / 20
            self.img_vy = (new_position[1] - self.position[1]) / 20
            self._animate_image()
            self.position = new_position
    def __str__(self):
        out = self.value + self.symbol
        if self.position:
            out += '['+str(self.position[0])+','+str(self.position[1])+']'
        return out

class CardImages():
    '''κλάση που δημιουργεί τις εικόνες των φύλλων από sprite sheet'''
    image_file = 'cards2.gif'
    path = '.'
    imagefile = os.path.join(path, image_file)
    images = {}
    @staticmethod
    def generate_card_images():
        # δημιουργία εικόνων των καρτών 79x123 px από το sprite sheet cards2.gif
        num_sprites = 13
        place = 0
        spritesheet = tk.PhotoImage(file= CardImages.imagefile)
        for x in 'sdhc':
            CardImages.images[x] = [CardImages._subimage(79 * i, 0 + place, \
                                            79 * (i + 1), 123 + place, spritesheet) for i in range(num_sprites)]
            place += 123
        CardImages.images['b'] = CardImages._subimage(0, place, 79, 123 + place, spritesheet) #back image
    @staticmethod
    def _subimage(l, t, r, b, spritesheet):
        dst = tk.PhotoImage()
        dst.tk.call(dst, 'copy', spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst

class ComputerPlayer(Player):
    '''κλάση που υλοποιεί τη συμπεριφορά του παίκτη'''
    def __init__(self, canvas, deck):
        self.canvas = canvas
        self.name = 'Big Blue'
        self.deck = deck
        self.score = 0
        self.hand = []  # τα χαρτιά του παίκτη
        self.start = GUI.padx, GUI.pady  # NW γωνία περιοχής για τις κάρτες του παίκτη
        self.next_card_position = self.place_of_next_card()
        self.message_place = self.start[0], round(self.start[1] + GUI.card_height * 1.1)
        self.infomessage = ""
        self.my_message = self.canvas.create_text(*self.message_place,
                                                  fill="white", text=self.infomessage, font="Arial 30", anchor='nw')
        self.active = False

    def place_of_next_card(self):
        return self.start[0] + (GUI.card_width // 2) * len(self.hand), self.start[1]

    def receive(self, card):  # adds a new card to player
        self.hand.append(card)
        self.next_card_position = self.place_of_next_card()
        return len(self.hand) - 1

    def plays(self, face=False):
        if self.active:
            card = GUICard.theCards[self.deck.draw()]
            card.set_face(face)
            card.move_to(self.place_of_next_card())
            self.receive(card)
            card_value = self._calculate_value(card)
            self.score += card_value
            self._check_if_exceeded()
            if self._computer_strategy():
                root.after(1000, self.plays)
            else:
                self.show_cards()
                self.active= False
                # if self.score == -1:
                #     self.update_message()

    def show_cards(self, all=False):
        if all: #self.score == -1 or all: ## για να μην εμφανίζει όλα τα φύλλα όταν χάνει ο υπολογιστής
            for card in self.hand:
                card.set_face(True)
        else:
            card_to_hide = random.randint(0, len(self.hand)-1)
            for i, card in enumerate(self.hand):
                if i != card_to_hide:
                    card.set_face(True)

    def _computer_strategy(self):
        return False if self.score >= 25 or self.score == -1 else True  #

    def update_message(self):
        pass
        # TODO ενημέρωση μηνύματος στην περιοχή του χρήστη
        if self.score==-1:
            self.infomessage = "{} : Δυστυχως κάηκες".format(self.name)
        else:
            self.infomessage = "{} : το σκορ είναι {}".format(self.name,self.score)
        self.canvas.delete(self.my_message)
        self.canvas.itemconfig(self.my_message, text=self.infomessage)
        self.my_message = self.canvas.create_text(*self.message_place,
                                                  fill="white", text=self.infomessage, font="Arial 30", anchor='nw')

class HumanPlayer(ComputerPlayer):
    '''κλάση που εξειδικεύει τον παίκτη για την περίπτωση του χρήστη'''
    user = None
    bool = False
    def __init__(self, *args, **kwds):
        ComputerPlayer.__init__(self, *args, **kwds)
        self.start = GUI.padx, GUI.board_height - GUI.pady - GUI.card_height  # περιοχή φύλλων χρήστη
        self.name = 'Παίκτης'
        self.message_place = self.start[0], round(self.start[1] - 0.6 * GUI.card_height)
        ### TODO να ζητείται το όνομα του χρήστη
        if HumanPlayer.bool == False:
            HumanPlayer.user = simpledialog.askstring('Όνομα χρήστη', 'Δώσε το όνομά σου:')
            self.name = HumanPlayer.user
            HumanPlayer.bool=True
        else:
            self.name= HumanPlayer.user
        if not self.name:
            self.name = 'Παίκτης'

    def plays(self, face=True):
        if self.active:
            card = GUICard.theCards[self.deck.draw()]
            card.set_face(face)
            card.move_to(self.place_of_next_card())
            self.receive(card)
            card_value = self._calculate_value(card)
            self.score += card_value
            self._check_if_exceeded()
            self.update_message()
            root.update_idletasks()
            if self.score == -1:
                self.active = False
                app.find_winner()

class GUI():
    '''κλάση με τις παραμέτρους του γραφικού περιβάλλοντος'''
    board_width, board_height = 900, 600  # διαστάσεις καμβά
    card_width, card_height = 79, 123  # διαστάσεις τραπουλόχαρτου
    padx, pady = 50, 50  # κενό μεταξύ του καμβά και ενεργού περιοχής
    deck = (800, 230)
    #περιοχή τράπουλας
    deck_of_cards_area = (deck[0], deck[1], deck[0] + card_width, deck[1] + card_height)
    @staticmethod
    def in_area(point, rect):
        if point[0]>= rect[0] and point[0] <= rect[2] \
            and point[1] >= rect[1] and point[1] <= rect[3]:
            return True
        else:
            return False

class GUIGame(Game, GUI)  :
    'Κεντρικός ελεγκτής του παιχνιδιού, δημιουργεί επιφάνεια, δημιουργεί τους παίκτες'
    def __init__(self, root):
        ##### Game parameters
        self.root = root
        root.title("Παιχνίδι 31gui")
        root.resizable(width='false', height='false')
        ##### GUI parameters
        self.infomessage_position = GUI.padx, GUI.board_height // 2 - 22
        self.top_font = 'Arial 20'
        self.f = tk.Frame(root)
        self.f.pack(expand=True, fill='both')
        self.create_widgets()
        self.run = False
        self.winner = None
        self.username = None

        # Αποθήκευση με την pickle
        self.PlayersScore = []

        if os.path.isfile('scores.db'):
            try:
                with open('scores.db', 'rb') as f: self.PlayersScore = pickle.load(f)
            except EOFError:
                pass
        #

    def create_widgets(self):
        self.message = ""
        self.score = [0, 0]
        self.canvas_info_message = ''
        # self.play_game()
        self.username = 'Παίκτης'
        #   TODO δημιουργία πλήκτρου έναρξης νέου παιχνιδιού, πλήκτρου διακοπής 'αρκετά!', σκορ,

        thefont = 'Arial 14'

        self.f1 = tk.Frame(self.f , relief='raised')
        self.f1.pack(side='top')

        self.button_start = tk.Button(self.f1, text=' Νέο παιχνίδι ', font=thefont, command=self.play_game , state='active')
        self.button_start.pack(side='left',  expand=1 , fill='x')

        self.button_stop = tk.Button(self.f1, text=' ...αρκετά! ', font=thefont, command=self.stop_drawing_cards , state='disabled')
        self.button_stop.pack(side='left', expand=1 , fill='x')

        self.thescore = tk.StringVar()
        self.thescore.set('Σκορ: Υπολογιστής {} - {} {} '.format(self.score[0], self.username, self.score[1]))
        tk.Label(self.f1, textvariable=self.thescore, font=thefont, fg='red').pack(side='right', expand=1 , fill='x')

        # TODO πλήκτρο αποθήκευσης σκορ και πλήκτρο ανάκτησης των 5 καλύτερων σκορ

        self.button_info = tk.Button(self.f1, text=' Ιστορικό σκορ ', font=thefont, command=self.info, state='normal')
        self.button_info.pack(side='left', fill='x')

        self.button_save_score = tk.Button(self.f1, text=' Αποθήκευση σκορ ', font=thefont, command=self.save_score , state='disabled')
        self.button_save_score.pack(side='left', expand=1 , fill='x')

        #==============================================================================================================

        self.f2 = tk.Frame(self.f)
        self.f2.pack( fill='both')
        self.canvas = tk.Canvas(self.f2, width=self.board_width, \
                                height=self.board_height, bg='darkgreen')
        self.canvas.pack(side='left', fill =  'x', expand=1)
        self.canvas.bind("<Button-1>", self.board_event_handler)
        # o παρακάτω κώδικας να αντικατασταθεί από την απάντηση στο ερώτημα για το πλήκτρο 'αρκετά!!'
        #self.canvas.bind("<Button-2>", self.stop)
        #self.canvas.bind("<Button-3>", self.stop)

    def save_score(self):
        pass
        # TODO δυνατότητα αποθήκευσης σκορ
        if self.username == 'Παίκτης':
            if not self.username:
                self.username = 'Παίκτης'

        self.PlayersScore.append({'username': self.username, 'loses': self.score[0], 'wins': self.score[1]})

        with open('scores.db', 'wb') as f:
            pickle.dump(self.PlayersScore, f)

    def info(self):
        pass
        # TODO δυνατότητα παρουσίασης υψηλότερων σκορ

        with open ('scores.db', 'rb') as f:
            scores = pickle.load(f)
        scores = sorted(scores, key=lambda x: (x['wins'] / (x['wins'] + x['loses']), x['wins'] + x['loses']), reverse=True)

        bestscores = tk.Toplevel()
        bestscores.title('Τα 5 καλύτερα σκορ έως τώρα είναι :')
        bestscores.focus()
        for i in range(min(5, len(scores))):
            history = tk.StringVar()
            history.set("{:1d}. Υπολογιστής - {:45s} : {:4d}   -{:4d} ".format(i + 1, scores[i]['username'], scores[i]['loses'],scores[i]['wins']))
            label = tk.Label(bestscores, textvariable=history, font=self.top_font)
            label.pack()

    def play_game(self):
        self.deck = pc.Deck()
        self.deck.shuffle()
        self.computer = ComputerPlayer(self.canvas, self.deck)
        self.human = HumanPlayer(self.canvas, self.deck) #
        self.username = self.human.name
        self.canvas.delete('all')
        for card in self.deck.content:
            c= GUICard(card, self.canvas)
            c.set_face(False)
            c.move_to(GUI.deck)
        self.run = True
        # ενημέρωση ονομάτων μόλις δίνει όνομα ο χρήστης
        self.thescore.set('Σκορ: {} {} - {} {} '.format(self.computer.name, self.score[0], self.username, self.score[1]))
        #
        # απενεργοποίησε πλήκτρο επανεκίνησης - ενεργοποίησε πλήκτρο '...αρκετά!'
        self.button_start.configure(state='disabled')
        self.button_stop.configure(state='active')
        #
        self.winner = None
        self.computer.active = True
        self.computer.plays()
        # human to play
        root.update_idletasks()
        if self.computer.score == -1 :
            root.after_idle(self.stop_drawing_cards)
        else:
            root.after_idle(self.human_turn)
    def human_turn(self):
        self.human.active = True

    def board_event_handler(self, event):
        x = event.x
        y = event.y
        if self.human.active and self.human.score != -1:
            if GUI.in_area((x, y), GUI.deck_of_cards_area):
                # Ο χρήστης έχει πατήσει στην περιοχή της τράπουλας
                self.human.plays()

    def find_winner(self):# αποφασίζει ποιος είναι ο νικητής
        max_score = max(self.computer.score, self.human.score)
        if max_score == -1:
            the_winner_is = 'Δεν υπάρχει νικητής'
            winner = False
        else:
            winner = 'human' if self.human.score == max_score else 'computer'
            the_winner_is = self.human.name if winner=='human' else self.computer.name
            article = 'ο' if the_winner_is[-1] in "sς" else 'η'
            the_winner_is = 'Νικητής είναι {} {} !!!'.format(article, the_winner_is)
        self.computer.show_cards(all=True)
        self.computer.update_message()
        self.pop_up(the_winner_is)
        self.run = False
        self.winner= None
        # πρόσθεσε βαθμό στον νικητή
        if winner == 'human':
            self.score[1]+=1
        elif winner == 'computer':
            self.score[0]+=1
        #
        # ενεργοποίηση πλήκτρου αποθήκευσης μετά τα 3 παιχνίδια
        if sum(self.score)>=3:
            self.button_save_score.configure(state = 'active')
        #
        # ενεργοποίησε πλήκτρο επανεκίνησης, απενεργοποίησε πλήκτρο διακοπής
        self.button_start.configure(state='active')
        self.button_stop.configure(state='disable')
        # ενημέρωση σκορ μετά το αποτέλεσμα
        self.thescore.set('Σκορ: {} {} - {} {} '.format(self.computer.name , self.score[0], self.username, self.score[1]))

    def pop_up(self, msg):
        #TODO συντεταγμένες στο όριο του καμβά
        tk.messagebox.showinfo('Αποτέλεσμα', msg)
    def stop(self, event):
        self.stop_drawing_cards()
    def stop_drawing_cards(self):
        self.find_winner()
        self.canvas.update_idletasks()

if __name__ == '__main__':
    root = tk.Tk()
    CardImages.generate_card_images()
    app = GUIGame(root)
    root.mainloop()
