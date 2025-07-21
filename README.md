# PRRI-RT2025

A RayCasting based FPS game developed by students and the [Artificial Intelligence Laboratory](https://ai.foi.hr/) at the [University of Zagreb Faculty of Organization and Informatics](https://www.foi.unizg.hr/). The game is developed using Python and GamePy. More details available at [itch.io](https://ailab-foi.itch.io/prri-rt2025).

# Credits

This game is based on [Stanislav Petrov's implementation](https://github.com/StanislavPetrovV/DOOM-style-Game) licensed under the MIT license.

# Cyber Hack – FPS igra u Pythonu s Raycasting engineom

## O projektu
Cyber Hack je FPS igra smještena u digitalni svijet. Igrač se kreće kroz zaražene segmente sustava, eliminira viruse i rješava zagonetke kako bi spriječio digitalni kolaps.

## Tehnologije
- Python 3
- Pygame
- Raycasting render engine (baziran na [Doom 1993] vizualnom stilu)

## Tema
- Stil: Cyberpunk / Digitalni svijet
- Inspiracija: Tron, antivirusni softver, glitch estetika

##  Kontrole
- W, A, S, D – Kretanje
- Miš – Ciljanje i pucanje
- ESC – Pauza / Izlaz

## Struktura koda
- `main.py` – Ulazna točka
- `map.py` – Struktura mape
- `raycasting.py` – Engine za prikaz
- `npc.py` – Umjetna inteligencija protivnika
- `weapon.py` – Upravljanje oružjima
- `object_handler.py` – Interaktivni elementi

## Instalacija
```bash
pip install -r requirements.txt
python main.py
