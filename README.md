# Python - Projekt "Okręty"
---
## Opis gry:

Po urachamieniu gracz widzi okno z dwoma siatkami: ___komputera___ oraz ___człowieka___. 
Na dole są przyciski: ___AUTO___ oraz ___Ręcznie___. 
+ W razie wyboru przycisku _AUTO_ program sam rozmieszci okręty na siatkie gracza i można będzie grać.
+ W razie wyboru przycisku _Ręcnie_ program da graczowi możliwość rozmieszczenia okrętów samemu. Żeby umieszcić okręt, graczowi trzeba nacisnąc na potrzebny kwadracik i ciągnąć w potrzebny kierunek. Można umieszcić taki okręty:
    * Jeden czteromasztowiec;
    * Dwa trójmastosztowca;
    * Trzy dwumasztowca;
    * Cztery jednomasztowca. 
* Okręty nie mogą się dotykać ani bokami ani rogami. W przeciwnym razie zostanie wyświetlony komunikat o tym. 
* Przy rozmieszcieniu okrętów można anulować ostani umieszczony okręt. Można to zrobić za pomocą przycisku ___Skasować___.
* Pod czas gry grać nie może "strzelać" za siatkę. W przeciwnym razie zostanie wyświetlony komunikat o tym.
* Gdy któryś gracz straci ostatni okręt, będzię informacja _"Wygrano"_ albo _"Przegrano"_.

---

## Klasy oraz ich metody

#### Class Grid
Klasa `Grid` sługuje do rysowania siatek i dodawania do nich tytułu, cyfr i liter.
W klasie są atrybuty:
* `title (str):` Imię gracza, które ma być wyświetlane na górze jego siatki;
* `offset (int):` Gdzie zaczyna się siatka (w liczbie bloków)
 (zazwyczaj 0 dla komputera i 15 dla człowieka)
 
 W klasie są trzy metody:
1. `draw_grid(self):` Rysuje dwie siatki dla obu graczy;
2. `add_nums_letters_to_grid():` Rysuje cyfry od 1 do 10 wzdłuż pionu i dodaje litery poniżej linii poziomych dla obu siatek;
3. `sign_grid():` Umieszcza imiona graczy (tytuły) na środku nad siatkami

#### Class Button
Klasa `Button` sługuje do tworzenia przycisków i pisze dla nich komunikat wyjaśniający.
Klasa ma takie atrybuty:
* `__title (str):` Nazwa przycisku (tytuł);
* `__message (str):` Komunikat wyjaśniający do wydrukowania na ekranie;
* `__x_start (int):` przesunięcie w poziomie, od którego należy rozpocząć rysowanie przycisku;
* `__y_start (int):` przesunięcie w pionie, gdzie rozpocząć rysowanie przycisku;
* `rect_for_draw:` Prostokąt przycisku do narysowania;
* `rect (pygame Rect):` obiekt Rect pygame;
* `__rect_for_button_title:` prostokąt w przycisku, aby wydrukować w nim tekst;
* `__color:` kolor przycisku

Metody klasy:
* `draw_button():` Rysuje przycisk jako prostokąt koloru (domyślnie BLACK);
* `change_color_on_hover():` Rysuje przycisk jako prostokąt koloru GREEN_BLUE;
* `print_message_for_button():` Wyświetla komunikat wyjaśniający obok przycisku

#### Class AutoShips
Klasa `AutoShips` losowo tworze wszystkie statki graczy na siatce.
W klasie są takie atrybuty:
* `offset (int):` Gdzie zaczyna się siatka (w liczbie bloków) (zwykle 0 dla komputera i 15 dla człowieka); 
* `available_blocks (set of tuples):` współrzędne wszystkich bloków dostępnych do tworzenia statków (aktualizowane za każdym razem, gdy tworzony jest statek);
* `ships_set (set of tuples):` wszystkie bloki zajmowane przez statki;
* `ships (list of lists):` lista wszystkich pojedynczych statków (jako listy)

Metody klasy `AutoShips:`
* `__create_start_block(available_blocks):`
    Losowo wybiera blok, od którego zaczyna się tworzenie statku.
    Losowo wybiera poziomy lub pionowy typ statku
    Losowo wybiera kierunek (od bloku startowego) - prosty lub wsteczny
    Zwraca trzy losowo wybrane wartości
    * *Argumenty*:
    `available_blocks(set of tuples):` współrzędne wszystkich bloków dostępnych do tworzenia statków (aktualizowane za każdym razem, gdy tworzony jest statek);
    * *Zwraca:*
    int: x współrzędna bloku losowego
    int: współrzędna y bloku losowego
    int: 0=poziomo (zmiana x), 1=pionowo (zmiana y)
    int: 1 = proste, -1 = odwrotne
* `__create_ship(number_of_blocks, available_blocks):`
 Tworzy statek o podanej długości (number_of_blocks) zaczynając od bloku początkowego zwróconego przez poprzednią metodę, używając typu statku i kierunku (zmieniając go, jeśli wychodzi poza siatkę) zwróconego przez poprzednią metodę. Sprawdza, czy statek jest ważny (nie sąsiaduje z innymi statkami i znajduje się w siatce) i dodaje go do listy statków;
    * *Argumenty:*
    `number_of_blocks (int):` długość potrzebnego statku;
    `available_blocks (set):` darmowe bloki do tworzenia statków;
    * *Zwraca:*
    list: lista krotek z nowymi współrzędnymi statku;
* `__get_new_block_for_ship(self, coor, direction, orientation, ship_coordinates):` 
 Sprawdza, czy nowe pojedyncze bloki dodawane do statku w poprzedniej metodzie znajdują się w siatce, w przeciwnym razie zmienia kierunek.
    * *Argumenty:*
    `coor (int):` współrzędna x lub y do zwiększenia/zmniejszenia;
    `direction (int):` 1 albo -1;
    `orientation (int):` współrzędne niedokończonego statku;
    * *Zwraca:*
    direction (int): prosto lub do tyłu;
    zwiększona/zmniejszona współrzędna ostatniego/pierwszego bloku statku w budowie (int)
* `__is_ship_valid(self, new_ship):`
Sprawdza, czy wszystkie współrzędne statku mieszczą się w dostępnym zestawie bloków.
     * *Argumenty:*
     `new_ship (list):` lista krotek z nowo utworzonymi współrzędnymi statku;
     * *Zwraca:*
     bool: True albo False
* `__add_new_ship_to_set(self, new_ship):` 
Dodaje wszystkie bloki z listy statków do zestawu statków.
    * *Argumenty:*
    `new_ship (list):` lista krotek z nowo utworzonymi współrzędnymi statku;
* `__update_available_blocks_for_creating_ships(self, new_ship):` 
Usuwa wszystkie klocki zajmowane przez statek i wokół niego z dostępnego zestawu blocków.
    * *Argumenty:*
    `new_ship ([type]):` lista krotek z nowo utworzonymi współrzędnymi statku
* `__populate_grid(self):` Tworzy potrzebną liczbę każdego typu statków, wywołując metodę `create_ship`. Dodaje każdy statek do listy statków, `ship_set` i aktualizuje dostępne bloki.
    * *Zwraca:*
    list: 2ga lista wszystkich statków

---
## Funkcji

    Sekcja strzelania
* `computer_shoots(set_to_shoot_from):`
Losowo wybiera blok z dostępnych do strzału z zestawu.
* `check_hit_or_miss(fired_block, opponents_ships_list, computer_turn, opponents_ships_list_original_copy, opponents_ships_set):`
Sprawdza, czy blok, w który strzelił komputer lub człowiek, jest trafieniem, czy chybieniem.
Aktualizuje zestawy za pomocą kropek (w pominiętych blokach lub w ukośnych blokach wokół trafionego bloku) i „X” (w trafionych blokach).
Usuwa zniszczone statki z listy statków.
* `update_destroyed_ships(ind, computer_turn, opponents_ships_list_original_copy):`
Dodaje bloki przed i za statkiem do `dotted_set`, aby narysować na nich kropki.
Dodaje wszystkie klocki na statku do `hit_blocks` ustawionych na rysowanie „X” w zniszczonym statku.
* `update_around_last_computer_hit(fired_block, computer_hits):`
Aktualizuje `around_last_computer_hit_set` (używany do wyboru komputera, z którego ma strzelać), jeśli uderzył w statek, ale go nie zniszczył. Dodaje do tego zestawu pionowe lub poziome bloki wokół ostatniego trafionego bloku. Następnie usuwa te bloki z tego zestawu, do których strzelano, ale chybiono. `around_last_computer_hit_set` sprawia, że komputer wybiera odpowiednie bloki, aby szybko zniszczyć statek, zamiast tylko losowo strzelać do całkowicie losowych bloków.
* `computer_first_hit(fired_block):`
Dodaje bloki powyżej, poniżej, na prawo i na lewo od bloku trafionego przez komputer do tymczasowego zestawu, z którego komputer może wybrać następny strzał.
* `computer_hits_twice():`
Dodaje bloki przed i po dwóch lub więcej blokach statku do tymczasowej listy, aby komputer mógł szybciej ukończyć statek.
    * *Zwraca:*
    set: tymczasowy zestaw bloków, z których potencjalnie powinien znajdować się ludzki statek, z którego komputer może strzelać
* `update_dotted_and_hit_sets(fired_block, computer_turn, diagonal_only=True):`
Umieszcza kropki na środku przekątnej lub dookoła bloku, który został uderzony (przez człowieka lub komputer). Dodaje wszystkie ukośne bloki lub wybrany blok dookoła do oddzielnego zestawu: hit blok (krotka).
* `add_missed_block_to_dotted_set(fired_block):`
Dodaje `fired_block` do zestawu chybionych strzałów (jeśli `fired_block` - tęsknić), aby następnie narysować na nich kropki.
Potrzebny również komputerowi, aby usunąć te kropkowane bloki z zestawu dostępnych bloków, z których może strzelać.

#
    Sekcja rysowania
* `draw_ships(ships_coordinates_list):`
Rysuje prostokąty wokół bloków zajmowanych przez statek.
* `draw_from_dotted_set(dotted_set_to_draw_from):`
Rysuje kropki na środku wszystkich bloków w `dotted_set`.
* `draw_hit_blocks(hit_blocks_to_draw_from):`
Rysuje „X” w blokach, które zostały pomyślnie trafione przez komputer lub człowieka.
* `show_message_rect_center(text, rect, which_font=font, color=RED):`
Wyświetla komunikat na ekranie w środku danego prostokąta.
   * *Argumenty:*
    `text (str):` Wiadomość do wydrukowania;
    `rect (tuple):`Prostokąt w formacie (x_start, y_start, width, height);
    `which_font (pygame font object, optional):` Jakiej czcionki użyć do wydrukowania wiadomości;
    `color (tuple, optional):` Kolor wiadomości. Domyślnie RED.
* ` ship_is_valid(ship_set, blocks_for_manual_drawing):` Sprawdza, czy statek nie dotyka innych statków.
    * *Argumenty:*
    `ship_set (set):` Zestaw z krotkami nowych współrzędnych statków;
    `blocks_for_manual_drawing (set):` Zestaw ze wszystkimi używanymi blokami dla innych statków, w tym ze wszystkimi blokami wokół statków.
    * *Zwraca:*
    Bool: True, jeśli statki się nie stykają, w przeciwnym razie False.
* `check_ships_numbers(ship, num_ships_list):`
Sprawdza, czy statek o określonej długości (1-4) nie przekracza wymaganej ilości (4-1).
    * *Argumenty:*
    `ship (list):` Lista z nowymi współrzędnymi statków;
    `num_ships_list (list):` Lista z numerami poszczególnych statków na odpowiednich indeksach.
    * *Zwraca:*
    Bool: True, jeśli liczba statków o określonej długości nie jest większa niż potrzebna,
    False, jeśli jest wystarczająco dużo takich statków.