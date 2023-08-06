import pickle

import numpy as np
import tensorflow as tf

from ._utils import create_sentiment_analysis_model, preprocess_text

# Resolving parent dependencies
from inspect import getsourcefile
import os
import sys
current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)

RESOURCES_PATH = os.path.join(os.path.dirname(__file__), "resources/")

MODEL_WEIGHTS_LOC = RESOURCES_PATH + "model_weights_except_word_embedding.pickle"
WORD_EMBEDDING_MATRIX_LOC = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'tokenizer/word_embedding.matrix'))
MODEL_LOC = RESOURCES_PATH + "model_weights.hdf5"
TOKENIZER_WORD_LOC = RESOURCES_PATH + "tokenizer_word.pickle"

# Data Processing Config
TEXT_MAX_LEN = 128 # 0.995th quantile of text length in data (post tokenization) is 125, so 128 is inclusive enough
WORD_EMBEDDING_VECTOR_SIZE = 128 # Word2Vec_medium.model
WORD_EMBEDDING_VOCAB_SIZE = 63_992 # Word2Vec_medium.model
# WORD_EMBEDDING_MATRIX and TAG_EMBEDDING MATRIX are initialized as Zeros, will be overwritten when model is loaded.
WORD_EMBEDDING_MATRIX = np.zeros((WORD_EMBEDDING_VOCAB_SIZE, WORD_EMBEDDING_VECTOR_SIZE))
WORD__OOV = '<OOV>'

# Model Config
NUM_RNN_UNITS = 256
NUM_RNN_STACKS = 2
DROPOUT = 0.2


class SentimentAnalyzer:
    """
    Sentiment Analysis class.

    - This is a Deep GRU based Sentiment Analysis classifier implementation.
    - It achieves 0.9345 Accuracy, 0.9230 on F1_macro_score and 0.8935 F1 score (treating class 0 as minority) on test set.
    - For more details about the training procedure and the dataset, see `ReadMe <https://github.com/vngrs-ai/VNLP/blob/main/vnlp/sentiment_analyzer/ReadMe.md>`_.
    """
    def __init__(self):
        self.model = create_sentiment_analysis_model(WORD_EMBEDDING_VOCAB_SIZE, WORD_EMBEDDING_VECTOR_SIZE, WORD_EMBEDDING_MATRIX,
                                                     NUM_RNN_UNITS, NUM_RNN_STACKS, DROPOUT)
        # Load Word embedding matrix
        word_embedding_matrix = np.load(WORD_EMBEDDING_MATRIX_LOC)
        # Load Model weights
        with open(MODEL_WEIGHTS_LOC, 'rb') as fp:
            model_weights = pickle.load(fp)
        # Insert word embedding weights to correct position (0 for Sentiment Analysis model)
        model_weights.insert(0, word_embedding_matrix)
        # Set model weights
        self.model.set_weights(model_weights)

        with open(TOKENIZER_WORD_LOC, 'rb') as handle:
            tokenizer_word = pickle.load(handle)
        self.tokenizer_word = tokenizer_word


    def predict(self, text: str) -> int:
        """
        High level user API for discrete Sentiment Analysis prediction.
        
        1: Positive sentiment.
        
        0: Negative sentiment.

        Args:
            text: 
                Input text.

        Returns:
             Sentiment label of input text.

        Example::

            from vnlp import SentimentAnalyzer
            sentiment_analyzer = SentimentAnalyzer()
            sentiment_analyzer.predict("Sipariş geldiğinde biz karnımızı atıştırmalıklarla doyurmuştuk.")
            
            0
        """

        prob = self.predict_proba(text)

        return 1 if prob > 0.5 else 0


    def predict_proba(self, text: str) -> float:
        """
        High level user API for probability estimation of Sentiment Analysis.

        Args:
            text: 
                Input text.

        Returns:
            Probability that the input text has positive sentiment.

        Example::
        
            from vnlp import SentimentAnalyzer
            sentiment_analyzer = SentimentAnalyzer()
            sentiment_analyzer.predict_proba("Sipariş geldiğinde biz karnımızı atıştırmalıklarla doyurmuştuk.")
            
            0.15
        """
        preprocessed_text = preprocess_text(text)
        integer_tokenized_text = self.tokenizer_word.texts_to_sequences([preprocessed_text])
        
        num_preprocessed_text_tokens = len(preprocessed_text.split())
        num_int_tokens = len(integer_tokenized_text[0])

        # if text is longer than the length the model is trained on
        if num_int_tokens > TEXT_MAX_LEN:
            first_half_of_preprocessed_text = " ".join(preprocessed_text.split()[:num_preprocessed_text_tokens // 2])
            second_half_of_preprocessed_text = " ".join(preprocessed_text.split()[num_preprocessed_text_tokens // 2:])
            prob = (self.predict_proba(first_half_of_preprocessed_text) + self.predict_proba(second_half_of_preprocessed_text)) / 2

        else:
            padded_text = tf.keras.preprocessing.sequence.pad_sequences(integer_tokenized_text, maxlen = TEXT_MAX_LEN, 
                                                padding = 'pre', truncating = 'pre')
            prob = self.model.predict(padded_text)[0][0]

        return prob