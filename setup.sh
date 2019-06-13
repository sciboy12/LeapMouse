printf "Installation will start in 10 seconds. \n"
#sleep 10
mkdir ~/LeapMouse
cd ~/LeapMouse
printf "Opening Firefox to SDK download page \n"
printf "Please download version 2.3.1 of the SDK, and save it to ~/LeapMouse \n"
printf "Then press enter to continue.\n"
sleep 1
firefox https://developer-archive.leapmotion.com/downloads/external/skeletal-beta/linux?version=2.3.1.31549
read

printf "Extracting SDK \n"
tar -xzf Leap_Motion_SDK_Linux_2.3.1.tgz

printf "Installing the Leap software \n"
sudo dpkg -i Leap-2.3.1+31549-x64.deb

printf "Copying libraries \n"
cd LeapDeveloperKit_2.3.1+31549_linux/LeapSDK/lib
cp Leap.py x64/LeapPython.so x64/libLeap.so ~/LeapMouse


printf "Downloading LeapMouse \n"
wget https://github.com/sciboy12/LeapMouse/raw/master/LeapMouse.py

printf "Creating a Symlink in /usr/bin \n"
sudo ln -s ~/LeapMouse/LeapMouse.py /usr/bin/leapmouse
