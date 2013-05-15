TopWords
========

List the top english words used in documents.

## Install ##

If you use Ubuntu 12.x/13.x as me:

1) Install NLTK

   http://nltk.org/install.html

2) Download wordnet and punkt modules for NLTK

    python
    >>>import nltk
    >>>nltk.download()
 
## Run ##

Run the following command under the root directory of the source code to get the top words for the sample emails:

 python count.py SampleData/messages SampleData/freq.csv
