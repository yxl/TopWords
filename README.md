TopWords
========

List the top english words used in documents.

## Install ##
1) Install NLTK

   http://nltk.org/install.html
   
   If you use Ubuntu 12.x/13.x as me, use the following commands simply:

    sudo apt-get install python-setuptools
    sudo easy_install pip
    sudo pip install -U pyyaml nltk

2) Download wordnet and punkt modules for NLTK

    sudo python -m nltk.downloader wordnet punkt

   or use nltk interactive installer

    python
    >>>import nltk
    >>>nltk.download()
 
## Run ##

Run the following command under the root directory of the source code to get the top words for the sample emails:

 python count.py SampleData/messages SampleData/freq.csv
