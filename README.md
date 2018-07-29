# DRTDemo
EdinburghNLP DRT Demo for internal use only.
## Prerequisites
This demo requires python 2.7 and was only tested on Linux.  Using virtualenv is highly suggested. Here are some addtional tools you may want to install first.
* Flask
* pytorch (0.3.0.post4 CPU only)
* NLTK
* OpenCV for python
* TexLive
## Some data you may need.
Download the following data and put them into the folder named "data".
* The Model from https://drive.google.com/file/d/1jbi080WOWBY7JiZ7uodB6OJg06QAY62h/view?usp=sharing.
* The pretrained embedding from https://drive.google.com/file/d/1vdywO7kAa9SCDW7u9YWnusuwUoMrvBQn/view?usp=sharing.
## Running the tests
You may want to run the following code in python first.
```
  >>> import nltk
  >>> nltk.download('averaged_perceptron_tagger')
  >>> nltk.download('wordnet')
```
Run the following code in the terminal.
```
(venv) $ python app.py
```
Then right click the url in the terminal and open it.
