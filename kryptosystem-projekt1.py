# kryptosystem - projekt 1
# szyfr zalezy od sumy indeksow mod 3:
# 0 - podstawieniowy, 1 - vigenere, 2 - permutacyjny

alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# permutacja na sztywno (numeracja od 1)
perm = [3, 6, 1, 5, 2, 4]


def sprawdz_tekst(tekst):
    # wielkie litery, bez spacji
    tekst = tekst.upper().replace(" ", "")
    if tekst == "":
        raise ValueError("tekst jest pusty")
    for z in tekst:
        if z not in alfabet:
            raise ValueError("niedozwolony znak: " + z + " (tylko litery A-Z)")
    return tekst


# - a) podstawieniowy -
def podstawieniowy(tekst, klucz, szyfrowanie):
    if not szyfrowanie:
        klucz = -klucz
    wynik = ""
    for z in tekst:
        nr = alfabet.index(z)
        wynik += alfabet[(nr + klucz) % 26]
    return wynik


# - b) vigenere -
def vigenere(tekst, klucz, szyfrowanie):
    wynik = ""
    for i in range(len(tekst)):
        nr = alfabet.index(tekst[i])
        # litera klucza, klucz sie powtarza
        przesuniecie = alfabet.index(klucz[i % len(klucz)])
        if szyfrowanie:
            wynik += alfabet[(nr + przesuniecie) % 26]
        else:
            wynik += alfabet[(nr - przesuniecie) % 26]
    return wynik


# - c) permutacyjny -
def perm_szyfruj(tekst):
    # dopelniam iksami do pelnego bloku
    while len(tekst) % len(perm) != 0:
        tekst += "X"
    wynik = ""
    for start in range(0, len(tekst), len(perm)):
        blok = tekst[start:start + len(perm)]
        for p in perm:
            wynik += blok[p - 1]
    return wynik


def perm_deszyfruj(tekst):
    if len(tekst) % len(perm) != 0:
        raise ValueError("dlugosc szyfrogramu musi byc podzielna przez " + str(len(perm)))
    wynik = ""
    for start in range(0, len(tekst), len(perm)):
        blok = tekst[start:start + len(perm)]
        # odwracamy permutacje
        odp = [""] * len(perm)
        for i in range(len(perm)):
            odp[perm[i] - 1] = blok[i]
        wynik += "".join(odp)
    return wynik


# - pobieranie danych -
def pobierz_tryb():
    while True:
        dane = input("Podaj numery indeksow (oddzielone spacja): ")
        try:
            liczby = [int(x) for x in dane.split()]
            if len(liczby) == 0:
                print("Musisz podac przynajmniej jeden numer!")
                continue
            return sum(liczby) % 3
        except ValueError:
            print("Blad: indeksy musza byc liczbami!")


def pobierz_klucz_liczba():
    try:
        return int(input("Podaj klucz (liczba calkowita): "))
    except ValueError:
        raise ValueError("klucz musi byc liczba calkowita")


def pobierz_klucz_slowo():
    klucz = input("Podaj slowo kluczowe (min. 8 liter): ").upper().strip()
    if len(klucz) < 8:
        raise ValueError("slowo kluczowe jest za krotkie (min. 8 liter)")
    for z in klucz:
        if z not in alfabet:
            raise ValueError("w kluczu moga byc tylko litery A-Z")
    return klucz


def szyfruj_lub_deszyfruj(tryb, szyfrowanie):
    tekst = sprawdz_tekst(input("Podaj tekst: "))

    if tryb == 0:
        klucz = pobierz_klucz_liczba()
        wynik = podstawieniowy(tekst, klucz, szyfrowanie)
    elif tryb == 1:
        klucz = pobierz_klucz_slowo()
        wynik = vigenere(tekst, klucz, szyfrowanie)
    else:
        if szyfrowanie:
            wynik = perm_szyfruj(tekst)
        else:
            wynik = perm_deszyfruj(tekst)

    print("Wynik:", wynik)


# - menu -
def main():
    nazwy = ["podstawieniowy", "Vigenere", "permutacyjny"]
    tryb = pobierz_tryb()
    print("Szyfr dla tych indeksow:", nazwy[tryb])

    while True:
        print()
        print("--- MENU ---")
        print("1 - szyfruj")
        print("2 - deszyfruj")
        print("3 - zmien indeksy")
        print("0 - wyjscie")
        wybor = input("Twoj wybor: ")

        try:
            if wybor == "1":
                szyfruj_lub_deszyfruj(tryb, True)
            elif wybor == "2":
                szyfruj_lub_deszyfruj(tryb, False)
            elif wybor == "3":
                tryb = pobierz_tryb()
                print("Szyfr dla tych indeksow:", nazwy[tryb])
            elif wybor == "0":
                print("Koniec programu")
                break
            else:
                print("Nie ma takiej opcji, wybierz 0-3")
        except ValueError as e:
            print("Blad:", e)


main()
