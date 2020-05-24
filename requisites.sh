sudo usermod -aG i2c $USER
sudo apt-get update
sudo apt-get install nano -y
sudo -H apt install python3-pip python3-pil
sudo pip3 install cython
sudo pip3 install --upgrade numpy 
echo "numpy and python 3 pip installed"
##optional libraries for the jupyter notebook
sudo apt install nodejs npm
sudo pip3 install jupyter jupyterlab
sudo jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter lab --generate-config
jupyter notebook password
##libraries for the peripherals
sudo pip3 install Adafruit-SSD1306
echo "Oled library installed"
sudo pip3 install pyserial adafruit-circuitpython-gps
sudo pip3 install --upgrade adafruit_blinka
sudo apt autoremove
echo "GPS library installed"
