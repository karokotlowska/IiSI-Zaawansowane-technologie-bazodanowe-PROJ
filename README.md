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


