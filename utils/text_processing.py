#  Copyright (C) <2022>  <MontyPython Group>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import nltk
import contractions
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

# Expand English contractions
def expand_english_contractions(row):
    expanded_words = []
    for word in row['text'].split():
        expanded_words.append(contractions.fix(word))
    return ' '.join(expanded_words)


# Tokenize
def tokenize(row):
    return word_tokenize(row['expanded_text'])


# Remove punct
def remove_punct(row):
    return [word for word in row['tokenized_text'] if word.isalpha()]


# Stem
def stem(row):
    return [PorterStemmer().stem(word) for word in row['no_punct_text']]


# Lemmatization
def lemmatize(row):
    return [WordNetLemmatizer().lemmatize(word) for word in row['stemmed_text']]


# Rejoin text after processing
def join_words(row):
    return " ".join(row['lemmatized_text'])


def process_text(data_frame):
    data_frame['expanded_text'] = data_frame.apply(expand_english_contractions, axis=1)
    data_frame['tokenized_text'] = data_frame.apply(tokenize, axis=1)
    data_frame['no_punct_text'] = data_frame.apply(remove_punct, axis=1)
    data_frame['stemmed_text'] = data_frame.apply(stem, axis=1)
    data_frame['lemmatized_text'] = data_frame.apply(lemmatize, axis=1)
    data_frame['processed_text'] = data_frame.apply(join_words, axis=1)
