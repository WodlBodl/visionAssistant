Assistant for the visually impaired
===================================

Run the following commands for setup:
---
```
sudo pip install -r backend/requiremenst.txt
```

Installing OpenCV 2
---
For os-x:
```
brew tap homebrew/science
brew install opencv
export PYTHONPATH=/usr/local/lib/python2.7/site-packages:$PYTHONPATH
```
Linux:
```
sudo apt-get install python-opencv
```
For everything else:
```
http://opencv.org/downloads.html
```
Installing Sci-kit Learn
---
Mac os-x:
```
sudo pip install -U numpy scipy scikit-learn
```
Linux:
```
sudo apt-get install build-essential python-dev python-setuptools \
                     python-numpy python-scipy \
                     libatlas-dev libatlas3gf-base
```
Extra:
---
Must use this for cv2 on mac every time you open a new terminal window for now...
```
export PYTHONPATH="/usr/local/lib/python2.7/site-packages:$PYTHONPATH"
```
