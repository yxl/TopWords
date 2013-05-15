import re
import sys
import os
import os.path
import nltk

# Count how many times each words appears in a text file, such as email.
# Called the file like this:
#
#   python count.py Input_File_Or_Folder Output_Frequency_File.csv
#

def readFiles(lines, path):
  if os.path.isfile(path):
    f = open(path, 'r')
    lines.extend(f.readlines())
    f.close
  else:
    for child in os.listdir(path):
      readFiles(lines, os.path.join(path, child))

lines = []

readFiles(lines, sys.argv[1])
 
# Convert the word with the first character capitalzied to lowercase
def formatWord(word):
  if word.isupper():
    return word
  else:
    return word.lower()

# Check if the given string is a word.
# A word should only contains alphanumeric character and has more than more character.
def isWord(word):
  n = len(word)
  if n <= 1 or n >= 30:
    return False
  return word[0].isalpha() and word.isalnum()

prefixesToSkip = ('Subject:', 'From:', 'Date:', 'To:', 'CC:', 'Cc:', 'Message-ID:', 'Content-Type:', 'Message:')
surfixesToSkip = (' wrote:',)
# '[>\-_]+' - Skip quoted replies of the email, whose lines start with one or more '>'s.
patternsToSkip = (re.compile('[>\-_]+'),)

# Skip the line that does not belong to the email body.
def canSkip(line):
  for prefix in prefixesToSkip:
    if line.startswith(prefix):
      return True
  for surfix in surfixesToSkip:
    if line.endswith(surfix):
      return True
  for p in patternsToSkip:
    if p.match(line) != None:
      return True
  return False

# Count the word frequency
finalCount={}
sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
for line in lines:
  line = line.strip()
  if canSkip(line):
    continue
  #print(line + '\n')
  for sentence in sent_tokenizer.tokenize(line):
    for word in nltk.word_tokenize(sentence):
      if not isWord(word):
        continue  
      finalCount[word] = finalCount.get(word,0)+1

def mergeWord(dest, src):
  if dest in finalCount:
    finalCount[dest] += finalCount[src]
    finalCount.pop(src)
    return True
  return False

# The capitalized word and lowercase word are treated as different words when counting
# their frequency in the previous step. We will merge their frequency.
for word in finalCount.keys():
  formatted = formatWord(word)
  # Use lowercase word if exits
  if formatted != word:
    mergeWord(formatted, word)

# Stem words. Strip off any affixes
wnl = nltk.WordNetLemmatizer()
for word in finalCount.keys():
  if word.endswith('ies') or word.endswith('ied'):
    stemmed = word[:-3] + 'y'
    if mergeWord(stemmed, word):
      continue
  if word.endswith('es') or word.endswith('ed'):
    stemmed = word[:-1]
    if mergeWord(stemmed, word):
      continue
    stemmed = word[:-2]
    if mergeWord(stemmed, word):
      continue
  if word.endswith('ing'):
    stemmed = word[:-3]
    if mergeWord(stemmed, word):
      continue
    stemmed += 'e'
    if mergeWord(stemmed, word):
      continue
    if len(word) > 5 and word[-4] == word[-5]:
      stemmed = word[:-4]
    if mergeWord(stemmed, word):
      continue    
  stemmed = wnl.lemmatize(word)
  if stemmed != word:
    mergeWord(stemmed, word)

f = open(sys.argv[2],'w')
for (count, word) in sorted([(count,word) for (word,count) in finalCount.items()],  reverse=True):
  if count > 1:
    print('%s\t%s' % (count, word))
    f.write('%s,%s\n' % (count, word))

f.close()
