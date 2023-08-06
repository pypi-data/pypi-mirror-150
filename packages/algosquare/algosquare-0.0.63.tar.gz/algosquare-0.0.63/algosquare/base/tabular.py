"""Tabular algos and auxiliary functions."""

from abc import ABC, abstractmethod
from .algo import Algo
from .predictor import Predictor
from .types import Metatype

INPUT_METATYPES = {Metatype.NUMERICAL, Metatype.CATEGORICAL, Metatype.BINARY,
            Metatype.DATETIME, Metatype.TIMESTAMP, Metatype.DELIM_PIPE, Metatype.DELIM_SEMICOLON}

class TabularClassifier(Predictor, ABC):
    """
    Base class for tabular classification model.

    Note:
        'predict_proba' and 'decision_function' are optional, but should be implemented if possible.
    """
    @abstractmethod
    def predict(self, X):
        """
        Makes prediction for given data.
        
        Args:
            X: DataFrame with shape (n_samples, n_features).

        Returns:
            DataFrame with index of X and columns of y.
        """
        pass

    def predict_proba(self, X):
        """
        Outputs class probabilities for given data.
        
        Args:
            X: DataFrame with shape (n_samples, n_features).

        Returns:
            DataFrame with index of X and columns of classes in y, or list thereof for multivariate problems.

        Raises:
            NotImplementedError.
        """
        raise NotImplementedError

    def decision_function(self, X):
        """
        Outputs decision function for given data.
        
        Args:
            X: DataFrame with shape (n_samples, n_features).

        Returns:
            DataFrame with index of X and columns of classes in y, or list thereof for multivariate problems.
        
        Raises:
            NotImplementedError.
        """
        return self.predict_proba(X)

class TabularClassificationAutoML(Algo, TabularClassifier, ABC):
    """Base class for tabular classification learning algorithm."""
    @abstractmethod
    def fit(self, timeout, metric, X, y, X_metatypes, y_metatypes, X_unlabelled = None):
        """
        Fits model on data.

        Args:
            timeout: time in seconds to fit the model.
            metric: Metric.
            X: DataFrame with shape (n_samples, n_features) and dtype=str.
            y: DataFrame with shape (n_samples, n_outputs) and dtype=str.
            X_metatypes: list of n_features Metatypes.
            y_metatypes: list of n_outputs Metatypes.
            X_unlabelled: DataFrame with shape (n_samples_unlabelled, n_features).
        """
        pass

    @abstractmethod
    def input_metatypes(self):
        """
        Describes the X_metatypes that the algo supports.
        
        Returns: 
            Set of Metatypes.
        """
        pass

    @abstractmethod
    def target_metatype(self):
        """
        Describes the y_metatype that the algo supports.
        
        Returns: 
            Metatype.
        """
        pass

    @abstractmethod
    def is_multioutput(self):
        """
        Returns true if the algo supports mulitple outputs.
        
        Returns: 
            Boolean.
        """
        pass

class TabularRegressor(Predictor, ABC):
    """Base class for tabular regression model."""
    @abstractmethod
    def predict(self, X):
        """
        Makes prediction for given data.
        
        Args:
            X: DataFrame with shape (n_samples, n_features).

        Returns:
            DataFrame with index of X and columns of y.
        """
        pass

class TabularRegressionAutoML(Algo, TabularRegressor, ABC):
    """Base class for tabular regression learning algorithm."""
    @abstractmethod
    def fit(self, timeout, metric, X, y, X_metatypes, y_metatypes, X_unlabelled = None):
        """
        Fits model on data.

        Args:
            timeout: time in seconds to fit the model.
            metric: Metric.
            X: DataFrame with shape (n_samples, n_features) and dtype=str.
            y: DataFrame with shape (n_samples, n_outputs) and dtype=str.
            X_metatypes: list of n_features Metatypes.
            y_metatypes: list of n_outputs Metatypes.
            X_unlabelled: DataFrame with shape (n_samples_unlabelled, n_features).
        """
        pass

    @abstractmethod
    def input_metatypes(self):
        """
        Describes the X_metatypes that the algo supports.
        
        Returns: 
            Set of Metatypes.
        """
        pass

    @abstractmethod
    def is_multioutput(self):
        """
        Returns true if the algo supports mulitple outputs.
        
        Returns: 
            Boolean.
        """
        pass

def is_input_metatype(metatype, strict = False):
    """Checks if metatype is valid input metatype.

    Args:
        metatype: Metatype or int.
        strict: checks if metatype is Metatype.

    Returns: 
        bool.
    """
    if strict and not isinstance(metatype, Metatype):
        return False

    try:
        metatype = Metatype(metatype)
        return metatype in INPUT_METATYPES
    except ValueError:
        return False

