printf "Installation will start in 10 seconds. \n"
sleep 10

printf "Installing pynput and numpy \n"
sleep 2
python2 -m pip install pynput numpy

printf "Creating ~/LeapMouse"
sleep 2
mkdir ~/LeapMouse
cd ~/LeapMouse

printf "Opening Firefox to SDK download page \n"
printf "Please download version 2.3.1 of the SDK, and save it to ~/LeapMouse \n"
printf "Note that a Leap Motion account is required to download. \n"
printf "Then press Enter to continue. \n"
sleep 2
firefox https://developer-archive.leapmotion.com/downloads/external/skeletal-beta/linux?version=2.3.1.31549
read

printf "Extracting SDK \n"
sleep 2
tar -xzf Leap_Motion_SDK_Linux_2.3.1.tgz


printf "Installing the Leap software \n"
sleep 2
cd LeapDeveloperKit_2.3.1+31549_linux
sudo dpkg -i Leap-2.3.1+31549-x64.deb

printf "Adding leapd to ~/.profile \n"
sleep 2
#cat 'sudo leapd &' ~/.profile
echo "sudo leapd &" >> ~/.profile
printf "Copying libraries \n"
sleep 2
cd LeapSDK/lib
cp Leap.py x64/LeapPython.so x64/libLeap.so ~/LeapMouse

printf "Downloading LeapMouse \n"
sleep 2
cd ~/LeapMouse
wget https://github.com/sciboy12/LeapMouse/raw/master/LeapMouse.py

printf "Creating launch script in /usr/bin \n"
sleep 2
cd /usr/bin
sudo wget https://github.com/sciboy12/LeapMouse/raw/master/leapmouse
sudo chmod +x leapmouse


printf "Done. \n"
printf "To run, type "'leapmouse'" in any directory. \n"
