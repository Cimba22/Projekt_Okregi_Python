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

## Funkcji oraz klasy

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
* `create_start_block(available_blocks):`
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
* `create_ship(number_of_blocks, available_blocks):`
 Tworzy statek o podanej długości (number_of_blocks) zaczynając od bloku początkowego zwróconego przez poprzednią metodę, używając typu statku i kierunku (zmieniając go, jeśli wychodzi poza siatkę) zwróconego przez poprzednią metodę. Sprawdza, czy statek jest ważny (nie sąsiaduje z innymi statkami i znajduje się w siatce) i dodaje go do listy statków;
    * *Argumenty:*
    `number_of_blocks (int):` długość potrzebnego statku;
    `available_blocks (set):` darmowe bloki do tworzenia statków;
    * *Zwraca:*
    list: lista krotek z nowymi współrzędnymi statku;
* `get_new_block_for_ship(self, coor, direction, orientation, ship_coordinates):`
 Sprawdza, czy nowe pojedyncze bloki dodawane do statku w poprzedniej metodzie znajdują się w siatce, w przeciwnym razie zmienia kierunek.
    * *Argumenty:*
    `coor (int):` współrzędna x lub y do zwiększenia/zmniejszenia;
    `direction (int):` 1 albo -1;
    `orientation (int):` 
