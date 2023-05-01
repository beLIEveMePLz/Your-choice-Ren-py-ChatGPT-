# LE 5.1.3

import json
import os


class LocationTemplate:
    # szablon dla lokacji, definiujący pola, które powinna posiadać każda instancja klasy Location
    template = {
        "loc_id": "",  # identyfikator lokacji
        "name": "",  # nazwa lokacji
        "attributes": {
            "typo": "",  # typ lokacji (indoor lub outdoor)
            "group": "",  # grupa lokacji (np. dom jednorodzinny gracza)
            "floor": {
                "level": "",  # nazwa piętra
                "above": {"state": "none"},  # opis tego, co jest nad piętrem (domyślnie brak)
                "under": {"state": "none"}  # opis tego, co jest pod piętrem (domyślnie brak)
            },
            "category": ""  # kategoria lokacji (np. pokój, kuchnia, łazienka)
        },
        "cells": {  # słownik opisujący komórki (np. drzwi, okno, mebel) w lokacji
            "cell_id": {
                "name": "",  # nazwa komórki
                "description": "",  # opis komórki
                "type": "",  # typ komórki (np. door, window, wall, furniture)
                "upper": {"state": "none"},  # opis tego, co jest nad cellem (domyślnie brak)
                "lower": {"state": "none"},  # opis tego, co jest pod cellem (domyślnie brak)
                "connections": {  # słownik opisujący połączenia pomiędzy komórkami
                    "direction": {
                        "cell_id": "",  # identyfikator komórki, do której prowadzi połączenie
                        "type": "",  # typ połączenia (np. open, closed, locked)
                        "key": ""  # klucz do odblokowania połączenia (opcjonalnie)
                    }
                }
            }
        },
        "connected_to": {  # słownik opisujący połączenia pomiędzy lokacjami
            "loc_id": {
                "direction": "",  # kierunek połączenia (np. north, east, up, down)
                "description": "",  # opis połączenia
                "type": "",  # typ połączenia (locked, unlocked, hidden, visible)
                "key": ""  # klucz do odblokowania połączenia (opcjonalnie)
            }
        }
    }

    def __init__(self):
        for key, value in self.template.items():
            if isinstance(value, dict):
                setattr(self, key, type(value)())
                for k, v in value.items():
                    if isinstance(v, dict):
                        setattr(getattr(self, key), k, type(v)())
                        for k2, v2 in v.items():
                            setattr(getattr(getattr(self, key), k), k2, v2)



class LocationFileManager:
    FILENAME = 'locations.txt'
    DEFAULT_DATA = {'locations': []}

    @classmethod
    def read_location_file(cls):
        try:
            with open(cls.FILENAME, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"{cls.FILENAME} not found. Creating new file with default data.")
            cls.write_location_file(cls.DEFAULT_DATA)
            data = cls.DEFAULT_DATA
        return data

    @classmethod
    def write_location_file(cls, data):
        with open(cls.FILENAME, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def update_location_file(cls, data):
        cls.write_location_file(data)

    @classmethod
    def delete_location_file(cls):
        try:
            os.remove(cls.FILENAME)
            print(f"{cls.FILENAME} deleted.")
        except FileNotFoundError:
            print(f"{cls.FILENAME} not found.")

class LocationEditor:
    OPTIONS = {
        'typo': ['0. Create new type'],
        'group': ['0. Create new group'],
        'floor': ['0. Create new floor'],
        'category': ['0. Create new category'],
    }

    @classmethod
    def create_location(cls):
        data = LocationFileManager.read_location_file()

        # Dodanie istniejących wartości do listy opcji
        for location in data['locations']:
            for key in cls.OPTIONS.keys():
                value = location.get(key)
                if value is not None and value not in cls.OPTIONS[key]:
                    cls.OPTIONS[key].append(value)


    @staticmethod
    def edit_location():
        pass
        # Reszta kodu do edycji lokacji
        # ...

    @staticmethod
    def delete_location():
        pass
        # Reszta kodu do usuwania lokacji
        # ...

    @staticmethod
    def list_locations():
        try:
            with open(LocationFileManager.FILENAME, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Nie znaleziono pliku z lokacjami")
            return

        print("Lista lokacji:")
        for location in data['locations']:
            print(location['name'])

editor = LocationEditor()

while True:
    print("Menu:")
    print("1. Dodaj nową lokację")
    print("2. Wyświetl listę lokacji")
    print("3. Wyjście")

    choice = input("Wybierz opcję: ")

    if choice == "1":
        editor.create_location()
        print("Nowa lokacja została dodana!")
    elif choice == "2":
        print("Lista lokacji:")
        print(editor.list_locations())
    elif choice == "3":
        break
    else:
        print("Niepoprawna opcja. Spróbuj jeszcze raz.")
