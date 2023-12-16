CREATE TABLE Rodzaj_operacji (
                rodzaj_operacji VARCHAR NOT NULL,
                opis VARCHAR NOT NULL,
                CONSTRAINT rodzaj_operacji_pk PRIMARY KEY (rodzaj_operacji)
);


CREATE SEQUENCE kontrahent_id_firmy_seq;

CREATE TABLE Kontrahent (
                id_firmy VARCHAR NOT NULL DEFAULT nextval('kontrahent_id_firmy_seq'),
                nazwa VARCHAR NOT NULL,
                nip VARCHAR NOT NULL,
                numer_rachunku VARCHAR NOT NULL,
                CONSTRAINT kontrahent_pk PRIMARY KEY (id_firmy)
);


ALTER SEQUENCE kontrahent_id_firmy_seq OWNED BY Kontrahent.id_firmy;

CREATE TABLE Pracownik_stanowisko (
                id_stanowisko VARCHAR NOT NULL,
                opis VARCHAR NOT NULL,
                CONSTRAINT pracownik_stanowisko_pk PRIMARY KEY (id_stanowisko)
);


CREATE SEQUENCE pracownik_id_pracownik_seq;

CREATE TABLE Pracownik (
                id_pracownik INTEGER NOT NULL DEFAULT nextval('pracownik_id_pracownik_seq'),
                imie VARCHAR NOT NULL,
                email VARCHAR NOT NULL,
                nazwisko VARCHAR NOT NULL,
                CONSTRAINT pracownik_pk PRIMARY KEY (id_pracownik)
);


ALTER SEQUENCE pracownik_id_pracownik_seq OWNED BY Pracownik.id_pracownik;

CREATE TABLE Weryfikacja (
                id_pracownik INTEGER NOT NULL,
                login VARCHAR NOT NULL,
                haslo VARCHAR NOT NULL,
                CONSTRAINT weryfikacja_pk PRIMARY KEY (id_pracownik)
);


CREATE TABLE Pracownik_role (
                id_pracownik INTEGER NOT NULL,
                id_stanowisko VARCHAR NOT NULL,
                CONSTRAINT pracownik_role_pk PRIMARY KEY (id_pracownik, id_stanowisko)
);


CREATE SEQUENCE zamowienie_numer_kolejny_seq;

CREATE SEQUENCE zamowienie_id_firmy_seq;

CREATE TABLE Zamowienie (
                numer_kolejny_zamowienia INTEGER NOT NULL DEFAULT nextval('zamowienie_numer_kolejny_seq'),
                id_zamowienia VARCHAR NOT NULL,
                id_magazyn INTEGER NOT NULL,
                data_stworzenia VARCHAR NOT NULL,
                status VARCHAR NOT NULL,
                id_pracownik INTEGER NOT NULL,
                kwota NUMERIC(10,2),
                waluta_zamowienia VARCHAR NOT NULL,
                id_firmy VARCHAR NOT NULL DEFAULT nextval('zamowienie_id_firmy_seq'),
                CONSTRAINT zamowienie_pk PRIMARY KEY (numer_kolejny_zamowienia)
);


ALTER SEQUENCE zamowienie_numer_kolejny_seq OWNED BY Zamowienie.numer_kolejny_zamowienia;

ALTER SEQUENCE zamowienie_id_firmy_seq OWNED BY Zamowienie.id_firmy;

CREATE SEQUENCE zamowienie_szczegoly_id_zamowienie_seq_1;

CREATE TABLE Platnosc (
                numer_kolejny_platnosci INTEGER NOT NULL DEFAULT nextval('zamowienie_szczegoly_id_zamowienie_seq_1'),
                numer_kolejny_zamowienia INTEGER NOT NULL,
                status VARCHAR NOT NULL,
                sposob VARCHAR NOT NULL,
                data_zrealizowania DATE NOT NULL,
                kwota_platnosci NUMERIC NOT NULL,
                waluta_platnosci VARCHAR NOT NULL,
                CONSTRAINT platnosc_pk PRIMARY KEY (numer_kolejny_platnosci)
);


ALTER SEQUENCE zamowienie_szczegoly_id_zamowienie_seq_1 OWNED BY Platnosc.numer_kolejny_platnosci;

CREATE TABLE Magazyn_lokalizacje (
                id_magazyn INTEGER NOT NULL,
                nr_magazynu INTEGER NOT NULL,
                ulica VARCHAR NOT NULL,
                kod_pocztowy VARCHAR(6) NOT NULL,
                miasto VARCHAR NOT NULL,
                CONSTRAINT magazyn_lokalizacje_pk PRIMARY KEY (id_magazyn)
);


CREATE TABLE Kategoria (
                id_kategoria INTEGER NOT NULL,
                nazwa VARCHAR NOT NULL,
                CONSTRAINT kategoria_pk PRIMARY KEY (id_kategoria)
);


CREATE SEQUENCE produkt_id_produkt_seq;

CREATE TABLE Produkt (
                id_produkt INTEGER NOT NULL DEFAULT nextval('produkt_id_produkt_seq'),
                opis VARCHAR NOT NULL,
                id_kategoria INTEGER NOT NULL,
                CONSTRAINT produkt_pk PRIMARY KEY (id_produkt)
);


ALTER SEQUENCE produkt_id_produkt_seq OWNED BY Produkt.id_produkt;

CREATE TABLE Zamowienie_szczegoly (
                numer_kolejny_zamowienia INTEGER NOT NULL,
                id_produkt INTEGER NOT NULL,
                ilosc INTEGER NOT NULL,
                waluta VARCHAR(10) NOT NULL,
                cena NUMERIC(10,2) NOT NULL,
                CONSTRAINT zamowienie_szczegoly_pk PRIMARY KEY (numer_kolejny_zamowienia, id_produkt)
);


CREATE TABLE Magazyn_stan (
                id_produkt INTEGER NOT NULL,
                id_magazyn INTEGER NOT NULL,
                ilosc INTEGER NOT NULL,
                CONSTRAINT magazyn_stan_pk PRIMARY KEY (id_produkt, id_magazyn)
);


CREATE SEQUENCE magazyn_operacje_id_operacji_seq;

CREATE TABLE Magazyn_operacje (
                id_operacji INTEGER NOT NULL DEFAULT nextval('magazyn_operacje_id_operacji_seq'),
                id_produkt INTEGER NOT NULL,
                numer_kolejny_zamowienia INTEGER,
                data_operacji DATE NOT NULL,
                ilosc INTEGER NOT NULL,
                rodzaj_operacji VARCHAR NOT NULL,
                id_magazyn INTEGER NOT NULL,
                id_pracownik INTEGER NOT NULL,
                CONSTRAINT magazyn_operacje_pk PRIMARY KEY (id_operacji)
);


ALTER SEQUENCE magazyn_operacje_id_operacji_seq OWNED BY Magazyn_operacje.id_operacji;

ALTER TABLE Magazyn_operacje ADD CONSTRAINT rodzaj_operacji_magazyn_operacje_fk
FOREIGN KEY (rodzaj_operacji)
REFERENCES Rodzaj_operacji (rodzaj_operacji)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Zamowienie ADD CONSTRAINT kontrahent_zamowienie_fk
FOREIGN KEY (id_firmy)
REFERENCES Kontrahent (id_firmy)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Pracownik_role ADD CONSTRAINT pracownik_stanowisko_pracownik_role_fk
FOREIGN KEY (id_stanowisko)
REFERENCES Pracownik_stanowisko (id_stanowisko)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Zamowienie ADD CONSTRAINT pracownik_zamowienie_fk
FOREIGN KEY (id_pracownik)
REFERENCES Pracownik (id_pracownik)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Pracownik_role ADD CONSTRAINT pracownik_pracownik_role_fk
FOREIGN KEY (id_pracownik)
REFERENCES Pracownik (id_pracownik)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Weryfikacja ADD CONSTRAINT pracownik_weryfikacja_fk
FOREIGN KEY (id_pracownik)
REFERENCES Pracownik (id_pracownik)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Magazyn_operacje ADD CONSTRAINT pracownik_magazyn_operacje_fk
FOREIGN KEY (id_pracownik)
REFERENCES Pracownik (id_pracownik)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Zamowienie_szczegoly ADD CONSTRAINT zamowienie_zamowienie_szczegoly_fk
FOREIGN KEY (numer_kolejny_zamowienia)
REFERENCES Zamowienie (numer_kolejny_zamowienia)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Platnosc ADD CONSTRAINT zamowienie_platnosc_fk
FOREIGN KEY (numer_kolejny_zamowienia)
REFERENCES Zamowienie (numer_kolejny_zamowienia)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Magazyn_operacje ADD CONSTRAINT zamowienie_magazyn_operacje_fk
FOREIGN KEY (numer_kolejny_zamowienia)
REFERENCES Zamowienie (numer_kolejny_zamowienia)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Magazyn_stan ADD CONSTRAINT magazyn_magazyn_stan_fk
FOREIGN KEY (id_magazyn)
REFERENCES Magazyn_lokalizacje (id_magazyn)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Produkt ADD CONSTRAINT new_tablekategoria_produkt_fk
FOREIGN KEY (id_kategoria)
REFERENCES Kategoria (id_kategoria)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Magazyn_stan ADD CONSTRAINT produkt_magazyn_stan_fk
FOREIGN KEY (id_produkt)
REFERENCES Produkt (id_produkt)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Zamowienie_szczegoly ADD CONSTRAINT produkt_zamowienie_szczegoly_fk
FOREIGN KEY (id_produkt)
REFERENCES Produkt (id_produkt)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Magazyn_operacje ADD CONSTRAINT magazyn_stan_magazyn_operacje_fk
FOREIGN KEY (id_produkt, id_magazyn)
REFERENCES Magazyn_stan (id_produkt, id_magazyn)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;