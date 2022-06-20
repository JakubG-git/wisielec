
import string
from random import random as rd
class Obiekt:
    def __init__(self, slowo = "", zycie = 1, pudla = [], trafienia = []):
        self.slowo = slowo
        self.zycie = zycie
        self.pudla = pudla
        self.trafienia = trafienia
        self.alfabet = string.ascii_lowercase # tu wybieramy alfabet
    def save(self, file_name):
        with open(file_name, 'w') as f:
            f.write(self.slowo + '\n')
            f.write(str(self.zycie) + '\n')
            f.write(str(self.pudla) + '\n')
            f.write(str(self.trafienia) + '\n')
            f.close()
    def load(self, file_name):
        with open(file_name, 'r') as f:
            self.slowo = f.readline()[:-1]
            self.zycie = int(f.readline()[:-1])
            self.pudla = [i for i in f.readline()[:-1] if i in self.alfabet]
            self.trafienia = [i for i in f.readline()[:-1] if i in self.alfabet]
            f.close()
    def __str__(self):
        return "({0}, {1}, {2}, {3})".format(self.slowo, self.zycie, self.pudla, self.trafienia) # debbuging
class Gra:
    def __init__(self, slowo = "Gra"):
        self.obiekt = Obiekt(slowo)
        self.wczytana_gra = False
        self.wygrana = False
        self.przegrana = False
    def __init__(self, Obiekt = Obiekt()):
        self.obiekt = Obiekt
        self.wczytana_gra = False
        self.wygrana = False
        self.przegrana = False
    def save(self):
        file_name = (input("Podaj nazwe pliku: "))
        self.obiekt.save(file_name)
    
    def load(self):
        file_name = (input("Podaj nazwe pliku: "))
        self.obiekt.load(file_name)
        self.wczytana_gra = True
    
    def random_word(self) -> str:
        with open("polski.txt", 'r') as f:
            slowa = f.readlines()
            f.close()
        return slowa[int(len(slowa) * (rd()))][:-1]

    def stats(self):
        print("Życia: ", self.obiekt.zycie)
        print("Pudły: ", self.obiekt.pudla)
        print("Trafienia: ", self.obiekt.trafienia)
    
    def menu(self):
        print("Witaj w grze Wisielec!")
        print("1. Nowa gra")
        print("2. Zapisz gre")
        print("3. Wczytaj gre")
        print("4. Twoje statystyki")
        print("5. Wyjdz")

    def start(self):
        self.menu()
        while(not self.select()):
            self.menu()

    def win_loss_check(self):
        if self.obiekt.zycie == 0:
            print("Przegrana!")
            print(self.obiekt.slowo)
            self.przegrana = True
        if len(self.obiekt.trafienia) == len(self.obiekt.slowo):
            print("Wygrana!")
            self.wygrana = True


    def print_word(self):
        odgadniente_slowo  = [literka if literka in self.obiekt.trafienia else "_" for literka in self.obiekt.slowo]
        for letter in odgadniente_slowo:
            print(letter, end=" ")
        print("")

    def hit_n_miss(self):
        litera = input("Podaj literke: ")
        if litera in self.obiekt.slowo and (litera not in self.obiekt.trafienia):
            for letter in self.obiekt.slowo:
                if litera == letter:
                    self.obiekt.trafienia.append(litera)
        elif litera not in self.obiekt.slowo:
            self.obiekt.pudla.append(litera)
            self.obiekt.zycie -= 1

    def end(self):
        if self.wygrana or self.przegrana:
            wybor = input("Czy chcesz rozpoczac nowa gre? (t/n)")
            if wybor == "t":
                self.start()
            else:
                self.stats()
                self.quit()
                exit()
        else:
            wybor = input("Czy chcesz zakończyć gre? (t/n)")
            if wybor == "t":
                self.obiekt.save("default.txt")
                self.quit()
                exit()
            elif wybor == "n":
                wybor2 = input("Czy chcesz zapisać? (t/n)")
                if wybor2 == "t":
                    self.save()
                    self.quit()
                    exit()
            else:
                pass
        
    def new_game(self):
        print("Nowa gra!")
        self.select_word()
        while(self.obiekt.zycie > 0 and (not self.wygrana) and (not self.przegrana)):
            self.win_loss_check()
            self.hit_n_miss()
            self.win_loss_check()
            self.print_word()
            self.end()
    def quit(self):
        print("Do zobaczenia!")
    def select(self) -> bool:
        wybor = int(input("Wybierz opcje: "))
        if wybor == 1:
            self.new_game()
            return True
        elif wybor == 2:
            self.save()
            return False
        elif wybor == 3:
            self.load()
            return True
        elif wybor == 4:
            self.stats()
            return False
        elif wybor == 5:
            self.quit()
            return True
    def select_word(self):
        print("1. Losuj slowo")
        print("2. Wpisz slowo")
        wybor = int(input("Wybierz opcje: "))
        if wybor == 1:
            self.obiekt.slowo = self.random_word()
        elif wybor == 2:
            self.obiekt.slowo = input("Podaj slowo: ")
        self.obiekt.zycie = len(self.obiekt.slowo)

if __name__ == "__main__":
    gra = Gra()
    gra.start()
