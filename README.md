## Simple RF-DETR app

A simple GUI application that tests out Roboflows new SOTA object detector RF-DETR.
Use it with either a live feed or a recording (in an OpenCV valid format) which can easily be chosen in the application.

## Setup
```console
# clone the repo
git clone https://github.com/RikardFridsenSkogsberg/Simple-RF-DETR-App.git

# change the working directory to RF-DETR
cd Simple-RF-DETR-App

# install the requirements
pip3 install -r requirements.txt
```

Make sure to have CUDA available if you can or detector will be slow. If you run into an issue, PyTorch versions is likely the cause of it.
## TODO
- Make the GUI prettier
- Add so model (.pth) file can be loaded in GUI
- When canceling the feed, remove the last frame shown

Beware this is mostly just made as an excuse to test out the RF-DETR model and learn a bit about PyQt/threading a video feed, so quality and possible updates is not guaranteed, but if you find it fun to play around with, enjoy :D
