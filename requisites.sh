sudo apt-get update
sudo -H apt install python3-pip python3-pil
sudo apt-get install nano -y
sudo usermod -aG i2c $USER


pip3 install Adafruit-SSD1306
sudo pip3 install pyserial adafruit-circuitpython-gps
sudo pip3 install --upgrade adafruit_blinka
sudo apt autoremove
