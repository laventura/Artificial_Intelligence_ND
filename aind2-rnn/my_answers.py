import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, Activation
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []

    # add the window_size'd input to X and y
    for ii in range(len(series) - window_size):
        X.append(series[ii: (ii + window_size)])
        y.append(series[(ii + window_size)])

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    ''' Build a simple RNN with 5 hidden units; and a Dense layer with 1 input '''
    model = Sequential()
    model.add(LSTM(5, input_shape=(window_size, 1)))
    model.add(Dense(1))

    return model


### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    import string 

    punctuation = ['!', ',', '.', ':', ';', '?', ' ']
    cleaned_text = []

    OK_text = string.ascii_lowercase + ''.join(punctuation)
    
    # eliminate punctuation
    for ch in text:
        if ch not in OK_text:
            ch = ' '
        cleaned_text.append(ch)

    cleaned_text =  ''.join(cleaned_text)
    print('[clean_text: original text len: {}, cleaned text len:{}]'.
            format(len(text), len(cleaned_text)))
    return cleaned_text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs  = []
    outputs = []

    TL = len(text)
    for ii in range(0, TL - window_size, step_size):
        inputs.append(text[ii: ii + window_size])
        outputs.append(text[ii + window_size])

    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    ''' Returns an LSTM model with:
        - 200 hidden units
        - input shape of (window_size, num_chars)
        - Dense layer of num_chars
        - Softmax activation
    '''
    model = Sequential()
    model.add(LSTM(200, input_shape=(window_size, num_chars)))
    model.add(Dense(num_chars))
    model.add(Activation('softmax'))

    return model
