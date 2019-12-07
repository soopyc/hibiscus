echo "Starting bot..."
echo "Installing modules..."
python3 -m pip install -r requirements.txt
echo "Running Decoder"
python3 tokenhelper.py
echo "Running Bot..."
while :;do python3 bot.py;done