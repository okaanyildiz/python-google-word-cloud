import sys
import io
import fileupload
from IPython.display import display
from matplotlib import pyplot as plt
import numpy as np
import wordcloud
!pip install wordcloud
!pip install fileupload
!pip install ipywidgets
!jupyter nbextension install - -py - -user fileupload
!jupyter nbextension enable - -py fileupload


# Uploader widget / Upload a .txt

def _upload():

    _upload_widget = fileupload.FileUploadWidget()

    def _cb(change):
        global file_contents
        decoded = io.StringIO(change['owner'].data.decode('utf-8'))
        filename = change['owner'].filename
        print('Uploaded `{}` ({:.2f} kB)'.format(
            filename, len(decoded.read()) / 2 ** 10))
        file_contents = decoded.getvalue()

    _upload_widget.observe(_cb, names='data')
    display(_upload_widget)


_upload()

# Check the uploaded text for the punctuations and uninteresting words, remove all
# Calculate the frequency of the remaining words


def calculate_frequencies(file_contents):
    # Here is a list of punctuations and uninteresting words
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my",
                           "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them",
                           "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being",
                           "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how",
                           "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just"]

    frequencies = {}
    words_storage = []
    for letter in punctuations:
        file_contents = file_contents.replace(letter, '')
    for word in uninteresting_words:
        w = ' '+word+' '
        file_contents = file_contents.replace(w, ' ')
    for word in file_contents.split():
        if word.lower() not in words_storage:
            words_storage.append(word.lower())
            if word not in frequencies:
                frequencies[word] = 1
            else:
                frequencies[word] += 1

    # wordcloud
    cloud = wordcloud.WordCloud()
    cloud.generate_from_frequencies(frequencies)
    return cloud.to_array()


# Display your wordcloud image
myimage = calculate_frequencies(file_contents)
plt.imshow(myimage, interpolation='nearest')
plt.axis('off')
plt.show()
