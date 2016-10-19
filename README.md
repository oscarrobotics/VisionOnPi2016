# VisionOnPi2016
FRC Vision Processing on Raspberry Pi 3 using [OpenCV], [pynetworktables] and [imutils]
[pynetworktables]: https://github.com/robotpy/pynetworktables
[OpenCV]: https://github.com/opencv/opencv
[imutils]: https://github.com/jrosebr1/imutils

Installation of OpenCV
----------------------
To run this you first need to compile and install OpenCV on your Raspi 3 using the instructions on [this site], making sure to follow it to the letter, and use Python3 in the virtualenv setup.
[this site]: http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/
In these instructions you also install one of the 3 necessary libraries, 'numpy'

Installation of necessary Python libraries
------------------------------------------
Install imutils  
`pip install imutils`  
Install pynetworktables  
`pip install pynetworktables`  

Before you run
--------------
In the instructions, it has you set up a virtual environment for Python. If you choose to do this, you MUST run  
`source ~/.profile` and  
`workon cv`  
EVERY TIME you want to run the code.  
I will later add a Bash script that handles automatically running everything on boot.  
If enough people want it, I'll also create an image to flash-and-go for quick setup (and to handle the inevitable SD card corruption from killing power 30~ times a competition day)
