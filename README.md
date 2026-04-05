igy futtasd le termuxba 

pkg update -y
pkg upgrade -y
termux-setup-storage
pkg install -y git python
pkg install python3

cd $HOME
git clone https://github.com/milan21212/discordbotbymufasza.git
cd discordbotbymufasza

python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install discord.py

python3 main.py

holnap frissitem
