[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

<a href="https://www.tensorflow.org/"><img src="https://img.shields.io/badge/Tensorflow-v2.2.0-orange?style=for-the-badge&logo=tensorflow"></a>
<a href="https://jupyter.org/"><img src="https://img.shields.io/badge/Jupyter%20Notebook-v6.1.3-orange?style=for-the-badge&logo=jupyter"></a>






# <img src="https://github.com/Aditi-Chowdhuri/TutorAI/blob/master/static/images/favicon.png" width="5%">TutorAI
TutorAI is an educational platform and Web App that uses state of the art AI technology to provide personal and effective training in the field of Physical Education. It aims to revolutionalize the quality of learning dance, yoga, martials arts, etc that require precision in the body posture. The main objective is to create an online personal trainer and a common learning platform to bridge the gap between the learners and the trainers. 

### USP

* Pose Comparison and Analysis as an alloy of many state of the art AI and time series algorithms.
* New form of physical education that is at par with the generation.
* Steady Earning and growth opportunities in the current market.


## Implementation:  

A user friendly **Web App** which accepts a training video be it a YouTube link or recorded videos as input. This personalized Application maintains daily progress, pose analysis and scores of the user and ranks them accordingly into Beginner, Intermediate and Expert based on how their performance is. Depending on the video, it provides a set of initial instructions to the user which is obtained using **web scraping**. Every activity is defined by a set of postures obtained from a **Pose Net and segmentations**. A list of pre-recorded activities is stored in the **Firebase Real-Time Database**. 

On starting the exercise, the Website accesses the webcam and shows the motion of the user, superimposed on the original motion. This system provides **visual feedback** in 2D/3D for better learning. After the exercise is over, a **verbal feedback** is provided to the user depending on how well they performed the exercise, their rank and age group. Age group is added to distuinguish the learning ability od different classes of society. A **time series comparison** using DTW  is done to obtain similarity between the original exercise and the one performed by the user. To consider difficulty level of routines based on individuals a **personal LSTM model** is developed using federated learning to analyze movement and give quality feedback. This application also contains a feature by which people can **collaborate** with friends and perform activities together for more enhanced, interactive and fun experience.  

## Technology Stack  

### Web App: 

The frontend of our Web App is handled using **HTML**, **CSS**, **javascript**, **jquery** and **vanta.js**. The data recieved by frontend is sent to the **flask** backend for processing. Data stored in the **FireBase Real_time Database** plays an important role in this section. A complete pipeline is created using these techologies that makes our Web App completly autonomous.

### AI: 

The artificial intelligence of our platform comes into action during the analysis and comparision of the user's video. Pose estimation using **tflite model** extracts the keypoints from the user as well as the tutor frame-by-frame.  Simultaneously TensorFlow **DeepLab v3 image segmentation model** is used to segment the users movement. Our platform uses their combination to visually help the user learn the routines better. 

### Analysis:

The AI models are supported by a **Dyamic Time Warping (DTW)** algorithm which compares the videos to provide feedback on the users accuracy. To avoid  distortions caused by height, weight, and size of a person the poses sequences are converted to vectors using **Pose2Vec**. All the analysis and conclusions are dislayed using gauge progress bars, bar charts and spider plots. 
  

## Prerequisites

The following dependencies should be installed to run the code. There is also a requirements.txt file in the repi

```
pickle
numpy
tensorflow==2.2
glob
pandasflask==1.0.3
Pillow==6.0.0
opencv-python==4.0.0.21
matplotlib
dtaidistance
xtarfile==0.0.3
pyttsx3
gunicorn==20.0.4
itsdangerous==1.1.0
Jinja2==2.10.1
MarkupSafe==1.1.1
Werkzeug==0.15.2

```

## Challanges

During the implementation of our idea we faced issues tackling technology and computaion bounds. The integration of our code also resulted in some errors in the way:
* Reducing the time complexity of Pose Comparison.
* Integrating the AI models to work hand-in-hand
* Providing customized feedback for each user.

## Getting Started

Download a python interpeter preferable a version beyond 3.0. Install the prerequisute libraries given above preferably using the latest version of pip/pip3. Run flask_app.py to start the flask backend. Open the link given to see the website. 

```
$final_app.py

```

## Future Aspects

We aim to build an application where more people learn things that they think cannot be done without trainers by providing a personal trainer in their hands and take this project on large scale where this application will not just be a learning platform but also a place where people can spend their quality time in other interactive and healthy activities. We want to build a social training platform where people can connect with each other and a feed system where people can write blogs and articles on health, exercises and fitness and also associate NGOs and awareness camps which work towards these activities.

## Authors


* [**Shaashwat Agrawal**](https://github.com/Shaashwat05) 
* [**Sagnik Sarkar**](https://github.com/sagnik106) 
* [**Aditi Chowdhuri**](https://github.com/Aditi-Chowdhuri)
* [**Shobhit Tulshain**](https://github.com/Shobhit2000) 




