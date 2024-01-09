# Projekt "Opis i wizualizacja baz danych" z przedmiotu Zaawansowane technologie bazodanowe

Przygotuj rozwiązanie, które na podstawie istniejącej, działającej bazy danych:

przygotuje graficzną reprezentację jej schematu,
wygeneruje tekstowy opis jej tabel oraz atrybutów.
Opis powinien próbować odgadnąć semantykę, wykorzystując nazwy tabel i kolumn, oraz uwzględniać dodatkowe informacje,
takie jak komentarze, ograniczenia i związki.

Możliwe jest wykorzystanie zewnętrznych narzędzi. Przykładowo, wizualizacja może być wykonana przez dedykowany do tego
program (najlepiej open source). Można także wykorzystać API chatbotów AI do generowania tekstowych opisów bazy danych.

Efektem uruchomienia programu na istniejącej bazie danych powinien być plik Markdown zawierający opis i dołączone pliki
graficzne z diagramami. Diagramy mogą również być osadzone w postaci kodu wewnątrz pliku Markdown (na przykład za pomocą
Mermaid), ale proszę wtedy dołączyć instrukcje dotyczące instalacji niezbędnych zależności. Listę ciekawych narzędzi,
które mogą być potencjalnie przydatne znajdą Państwu np. na stronie programu Kroki.

# Dokumentacja projektu

## Instrukcja uruchomienia

1. Pobierz repozytorium
    ```bash
    git clone https://github.com/karokotlowska/IiSI-Zaawansowane-technologie-bazodanowe-PROJ.git
    ```
2. Przejdź do katalogu projektu
   ```bash
   cd IiSI-Zaawansowane-technologie-bazodanowe-PROJ
   ```
3. Zainstaluj wymagane zależności
    1. Wykorzystując środowisko poetry

        - Zainstaluj środowisko [Poetry](https://python-poetry.org/)
           ```bash
           curl -sSL https://install.python-poetry.org | python3 -
           ```
        - Zainstaluj zależności w wewnętrznym środowisku
           ```bash
           poetry install
           ```
        - Uruchom wirtualne środowisko
           ```bash
           poetry shell
           ```
    2. Wykorzystując lokalnego pythona
        - Środwisko było testowane na pythonie w wersji 3.9, dlatego zalecanie jest stosowanie tej wersji lub wyższej.
        - Zainstaluj zależności z pliku requirements.txt
            ```bash
            pip install -r requirements.txt
            ```
4. (Punkt nie wymagany) Konfiguracja zmiennych środowiskowych
    - Utworzenie pliku ze zmiennymi środowiskowymi
        ```bash
        cp .env.dist .env
        ```
    - Podmień zmienną OPENAI_API_KEY na własny klucz OpenAI
        ```
        OPENAI_API_KEY="XXX"
        ```
5. Uruchomienie programu z wymaganymi parametrami
    - Lista parametrów
    ```bash
      python main.py --help
    ```
   ![help_preview](doc/help_preview.png)
    - Uruchomienie programu
   ```bash
    python main.py --uri=postgresql://root:password@localhost:5432/dvdrental --lang=pl --gpt-version=gpt-4-1106-preview --tokens=4096
   ```

## Podręcznik Użytkownika

### Wymagania wstepne

- Wykonanie kroków z punktu **Instrukcja uruchomienia**
- Dostęp do Internetu
- Aktywny token OpenAI

**Aplikacja wspiera tylko i wyłącznie silnik bazodonowy PostgreSQL.**
W katalogu projektu *db_examples* znajdują się przykładowe bazy danych, które można wykorzystać do testów.

W celu wygenerowania opisu należy wykonać poniższe polecenie z poprawnymi argumentami.
Lista argumentów dostepna jest pod komendą `python main.py --help`.

![help_preview](doc/help_preview.png)

Wymagane jest podanie argumentu `--uri`, który powinien zawierać poprany adres URI dla silnika PostgreSQL.
Powyższy argument może zostać zastąpiony przez sekwencje argumentów `-user, --port, --host, --password`.
Argumenty z grupy GPT służą do manipulacji wersją API GPT, z której chcemy skorzystać.
Są to argumenty opcjonalne, domyślne aplikacja korzysta z darmowej wersji `gpt3.5-turbo`
oraz z maksymalnej liczby tokenów dla tego modelu jaką jest `2048`.
Liste dostępnych, płatnych modeli oraz ich ograniczenia można znaleźć na oficjalniej
stronie [OpenAI](https://platform.openai.com/docs/models).
Argument `--api-key` jest wymagalny tylko w przypadku gdy zmienna środowiskowa `OPEANAI_API_KEY` nie została
zdefiniowana na maszynie.
Aplikacja generuje opisy w dwóch wersjach językowych, Anglielskim, który jest językiem domyślnym oraz Polskim.
Parametr `--lang` przyjmuje wartości w postaci ISO 639(en, pl).

```bash
python main.py --uri=postgresql://root:password@localhost:5432/shopping_db --lang=pl --gpt-version=gpt-4 --tokens=4000
```
![app_run](doc/app_run.gif)

W trakcie trawnia programu na wejście logowane są wszystkie zdarzenia, również te związane z API Kroki oraz OpenAI w
celu lepszej weryfikacji działania oraz szybszego wykrycia błedów.
Logi API można wyłączyć zmieniając zmieniając argument w pliku `main.py`
z `logging.root.setLevel(logging.NOTSET)` na `logging.root.setLevel(logging.INFO)`

Po zakończeniu działania w katalogu projektu pojawi się katalog *output*, który zawiera plik markdown wraz z opisem oraz dołączone do niego pliki multimedialne.

![output_directory](doc/output_directory.png)

*Przykład treści pliku description.md dla powyższego polecenia*

![description_preview](doc/description_preview.gif)


**Pamietaj o zapisaniu wyników w innym miejscu przed ponownym uruchomieniem programu, ponieważ zostaną one nadpisane!**

### Błędy
W przypadku błędów związanych z OpenAI użytkownik dostaje na wyjście stosowny komunikat informujący jakie kroki powinien podjąć.

*Przykład prezentujący przypadek gdy ilość tokenów potrzebnych do wygenerowania opisu dla bazy danych nie mieści się w darmowym zakresie modelu `gtp-turbo-3.5`*
![error_presentation](doc/error_presentation.gif)


## Opis założeń

Projekt miał na celu stworzenie rozwiązania umożliwiającego analizę i prezentację istniejących baz danych relacyjnch - postgreSQL. Projekt powinien uwzględniać bazy danych z wieloma schematami. Kluczowe założenia projektu obejmują:

- Graficzna reprezentacja schematu bazy danych. Rozwiązanie jest w stanie generować wyraźne i czytelne diagramy, przedstawiające strukturę bazy danych, włącznie z tabelami, ich atrybutami, oraz związkami między nimi. Na wykresie powinny być osobno zaznaczone klucze główne oraz klucze obce. 

- Generowanie tekstowego opisu tabel i atrybutów. System oferuje funkcjonalność tworzenia szczegółowych opisów składników bazy danych, w tym tabel i ich atrybutów. Opis ten opiera się na analizie semantycznej nazw, uwzględniając dodatkowe informacje takie jak komentarze, ograniczenia, funkcje, widoki, indeksy.

- Tworzenie dokumentacji w formacie Markdown. Efektem końcowym działania programu jest plik Markdown, zawierający zarówno tekstowe opisy, jak i graficzne reprezentacje schematów baz danych. Projekt zakłada również dostarczenie instrukcji instalacji niezbędnych zależności, aby ułatwić użytkownikom korzystanie z rozwiązania.

Celem projektu jest stworzenie narzędzia, które w sposób kompleksowy i zrozumiały dla użytkownika przedstawi strukturę oraz semantykę analizowanej bazy danych, wykorzystując przy tym przyjazne użytkownikom metody prezentacji danych.


## Algorytmy

### Wyciąganie danych z bazy danych

Do tego zadania wykorzystaliśmy bibliotekę SQLalchemy, która udostępnia wiele metod pozwialających na wyciągnięcie danych z bazy. Program zakłada istnienie baz danych z wieloma schematami, natomiast konieczne było pominięcie niektórych schematów istniejących domyślnie w bazie:

```
SCHEMAS_TO_IGNORE = ['information_schema', 'pg_catalog', 'pg_toast', 'pg_temp_1', 'pg_toast_temp_1', 'pg_catalog']
```

Do wyciągnięcia informacji o związkach między tabelami, iterowaliśmy po każdej tabeli i dla niej sprawdzaliśmy istnieje związku 1 do 1 oraz 1 do wielu. Przypadek związku wiele do wielu zilustrowaliśmy jako 1 do wielu oraz 1 do wielu.

### Algorytm znajdowania relacji 1 do 1

Algorytm znajdowania relacji jeden do jeden (one-to-one) w bazie danych opiera się na analizie kluczy obcych (foreign keys), kluczy głównych (primary keys) oraz ograniczeń unikalności (unique constraints). W celu znalezienie relacji należy przeszukać tabele względem połączeń klucz główny (tabela 1) oraz unikalny klucz obcy (tabela 2). Proces ten jest kluczowy w zrozumieniu, jak dane są powiązane między różnymi tabelami w bazie danych. Oto kroki algorytmu:

1. Iteracja po kluczach wszystkich kluczach obcych w schemacie

2. Sprawdzenie czy kolumna, na którą wskazuje klucz obcyma powiązanie z aktualną tabelą. oraz jest częścią jakiegokolwiek ograniczenia unikalności (UNIQUE) w tabeli, do której się odnosi. Jeśli tak - oznacza to relację 1 do 1.

3. Jeśli tabela odniesienia (referred table) różni się od aktualnie iterowanej tabeli, algorytm identyfikuje to jako relację jeden do jednego. W takim przypadku, stosuje symbol "1--1" do reprezentowania tej relacji.

### Algorytm znajdowania relacji 1 do wielu

Algorytm do identyfikowania relacji jeden do wielu (one-to-many) w bazie danych analizuje powiązania między kluczami głównymi (primary keys) różnych tabel. Ten typ relacji jest powszechny w schematach baz danych, gdzie jedna tabela (nazywana tabelą rodzica) może być powiązana z wieloma rekordami w innej tabeli (nazywanej tabelą potomną). Oto kroki algorytmu:

1. Iteracja po kluczach wszystkich kluczach obcych w schemacie, gdzie każdy jest rozpatrywany pod kątem jego potencjalnego powiązania z innymi tabelami.

2. Sprawdzenie czy tabela zawierający dany klucz obcy ma powiązanie z aktualną tabelą. Jeśli tak - oznacza to relację 1 do wielu.

3. Przed dodaniem nowego opisu relacji, algorytm sprawdza, czy ta konkretna relacja (lub jej odwrotność) nie została już wcześniej zidentyfikowana i dodana do opisu - symbol "*--1". To zapobiega powtarzaniu się tych samych informacji.


*Przykład wygenerowanego diagramu*

![description_preview](doc/diagram_kroki_example.png)

### Wielowątkowość

## Wady i Strategie Ich Przyszłego Rozwiązania

### Wady zapropowanego rozwiązania

1. **Wykresy dla dużych baz danych mogą być nieczytelne**: Przy dużych bazach danych, wygenerowane wykresy mogą być nieczytelne i zbyt złożone, co może utrudnić zrozumienie struktury bazy.

2. **Niestabilność działania bota**: W niektórych przypadkach wykorzystywane api, używane do generowania opisów nie odpowiada zgodnie z przygotowanym przez nas wzorcem odpowiedzi, co prowadzi do niepoprawnego parsowania danych z odpowiedzi.

3. **Czas trwania odpowiedzi zapytania**: Przy dużych bazach danych czas oczekiwania na odpowiedź od bota lub wygenerowanie wykresu może być długi. Mimo użytej wielowątkowości w zapytaniach do czata, czas oczekiwania na odpowiedzi może być uciążliwy dla użytkownika korzystającego z programu.

4. **Brak interfejsu graficznego**: Aplikacja działa w linii poleceń, co może być barierą dla niektórych użytkowników, zwłaszcza tych mniej doświadczonych w pracy z takim środowiskiem.

5. **Brak uwzględnienie związków między relacjami pochodzącymi z dwóch różnych schematów**: System nie zakłada poprawnego działania w sytuacji, kiedy istnieje związek między dwoma relacjami, będącymi w różnych schematach.

### Strategie rozwiązania

1. **Ulepszenie wizualizacji dla dużych baz danych**: Można rozważyć użycie bardziej zaawansowanych narzędzi do wizualizacji, które lepiej radzą sobie z dużymi strukturami, np. oferujące funkcje grupowania lub ukrywania niektórych elementów dla lepszej czytelności. Możliwe byłoby również wykorzystanie interaktywnych narzędzi ilustrujących wykresy - umożliwiające zaawansowane funkcje przybliżania oraz oddalania.

2. **Stabilizacja działania bota**: Niestety nieprzewidywalność czata jest nie do rozwiązania na ten moment. Rozważyć można implementację zapytań do innego api, które może okazać się działać lepiej.

3. **Optymalizacja czasu odpowiedzi**: Analiza i optymalizacja procesów przetwarzających duże zbiory danych może przynieść znaczną poprawę.

4. **Tworzenie interfejsu graficznego**: Rozwój aplikacji o interfejs użytkownika bazujący na GUI znacznie ułatwiłby korzystanie z programu.

5. **Uwzględnienie związków między relacjami pochodzącymi z dwóch różnych schematów**: System powinien zakładać istnienie związku między dwoma relacjami, będącymi w różnych schematach.


