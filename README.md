igy futtasd le termuxba 

#!/bin/bash

# Frissítés és csomagok telepítése
pkg update -y
pkg upgrade -y
termux-setup-storage
pkg install -y git python

# Projekt mappa és klónozás
cd $HOME
git clone https://github.com/milan21212/discordbotbymufasza.git
cd discordbotbymufasza

# Virtuális környezet létrehozása és aktiválása
python -m venv venv
source venv/bin/activate

# Pip frissítése és discord.py telepítése
pip install --upgrade pip
pip install discord.py

# Futás
python3 main.py
