import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    Base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, 
                                    covariance_type="diag", 
                                    n_iter=1000,
                                    random_state=self.random_state, 
                                    verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    
    BIC maximizes the likelihood of data, and penalizes complex models
    - avoids cross validation by using a penalty term
    - scores model topologies by balancing fit / complexity in training set for each word

    BIC = -2 * logL  + p * logN
    where:
    - logL = log likelihood of fitted model
    - p = number of free params in model (i.e. measure of model complexity)
    - N = number of data points 

    Lower the BIC score, better is the model. The first term (-2 * LogL) decreases with higher p; 
    the second term (p * logN) increases with higher p. 

    Algo: 
    - loop thru min_components, max_components
    - find model with lowest BIC score

 
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        best_model = self.base_model(self.min_n_components)
        best_score = float('inf')

        for m in range(self.min_n_components, self.max_n_components + 1):
            try:
                model   = self.base_model(m)
                logL    = model.score(self.X, self.lengths)
                # get log(num of observations)
                logN    = np.log(self.X.shape[0])
                # p = num_states ^ 2 + 2 * num_features * num_states - 1
                p       = m ** 2 + 2 * self.X.shape[1] * m - 1
                score   = -2 * logL + p * logN

                # find the least score so far...
                if score < best_score:
                    best_score, best_model = score, model

            except:  # ValueError as v:
                # print("SelectorBic: ", v)
                # score = float('inf')
                pass

        return best_model



class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to HMM topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf

    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))

    DIC tries to find the number of components where the difference is largest. 
    DIC attempts to find a model that has high likelihood (small -ve number) for the original word,
    and low likelihood (large -ve number) to all other words, thus discriminating the original word.abs

    To run DIC and find an optimal model, we run a model on every word, and compare scores against all other words.abs

    DIC = log(P(X(i)) - 1/(M-1) * sum(log(P(X(all but i))))
        = log likelihood of data belonging to model - avg of anti log likehood of data X and model M
        = log(P(original word)) - average(log(P(all_other_words)))

    Higher the DIC score, better is the model

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        best_model  = self.base_model(self.min_n_components)
        best_score  = float('-inf')

        # go thru every component and find the best score/model
        for m in range(self.min_n_components, self.max_n_components + 1):
            try:
                model   = self.base_model(m)
                logL    = model.score(self.X, self.lengths)
                scores  = [model.score(x, length) for word, (x, length) in self.hwords.items() if word != self.this_word]
                score   = logL - np.mean(scores)

                # find highest score
                if score > best_score:
                    best_score, best_model = score, model

            except: # ValueError as v:
                # print("SelectorDIC: ", v)
                # score = float('-inf')
                pass

        return best_model
        


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    SelectorCV uses cross-validation to find optimal models. 
    It uses K-folds to fold dataset, rotating one left out fold for validation, which is considered 
    proxy for unseen data.

    Higher the CV score, better is the model. 

    Algo:
    - loop thru min_components to max_components
    - score each model
    - select the best model that has highest score on avg loglikelihood on the folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        kfold = KFold(n_splits=3)
        log_likelihoods = []
        scores_models = []

        for components in range(self.min_n_components, self.max_n_components + 1):
            try:
                # see if enough data to split using KFold
                if len(self.sequences) > 2:
                    # CV loop: get train/test indices
                    for ix_train, ix_test in kfold.split(self.sequences):
                        # training sequence
                        self.X, self.lengths = combine_sequences(ix_train, self.sequences)
                        # test sequence
                        X_test, len_test = combine_sequences(ix_test, self.sequences)

                        hmm_model = self.base_model(components)
                        log_likelihood = hmm_model.score(X_test, len_test)
                
                else:
                    # not enough data to split
                    hmm_model = self.base_model(components)
                    log_likelihood = hmm_model.score(self.X, self.lengths)

                log_likelihoods.append(log_likelihood)

                # get avg logL
                mean_score = np.mean(log_likelihoods)
                scores_models.append(tuple([mean_score, hmm_model]))

            except Exception as e:
                # print("SelectorCV: exc: ", e)
                pass
        
        # return hmm model corresponding to the max score
        if scores_models:
            maxx = max(scores_models, key = lambda x: x[0])
            return maxx[1]  # the hmm model corresponding to the max score
        else:
            return None

