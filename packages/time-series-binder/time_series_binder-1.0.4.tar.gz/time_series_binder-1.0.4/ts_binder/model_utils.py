import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ts_binder.data_processing import DataPreprocessing

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.statespace.exponential_smoothing import ExponentialSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing as holtwinters_ES
from keras.models import Sequential
from keras.layers import LSTM, Dense, Flatten
from neuralprophet import NeuralProphet

from neuralprophet.utils import set_random_seed
import tensorflow as tf
from tensorflow.keras import layers
import random

from keras.metrics import RootMeanSquaredError, MeanAbsolutePercentageError, MeanAbsoluteError


class Trainer:
    """
    This class provides methods to train the time series forecasting models.
    train_sarimax(show_summary: bool, **kwargs)
    This method trains a SARIMAX model on the preprocessed time series data and returns the trained model object. show_summary flag can be set to True to print the model summary.
    train_lstm(n_steps: int, n_target: int, epochs: int, batch: int, optimizer: str, **kwargs)
    This method trains a Long Short-Term Memory (LSTM) model on the preprocessed time series data and returns the last sequence of input data along with the trained model object. n_steps and n_target represent the number of time steps and input features respectively, epochs and batch are the number of training epochs and batch size, and optimizer is the name of the optimizer to use.
    train_neural_prophet(**kwargs)
    This method trains a NeuralProphet model on the preprocessed time series data and returns the trained model object.
    """
    def __init__(self, data: pd.Series):
        """
        Constructor for TimeSeriesModel class.
        Args:
            data (pd.Series): The time series data to be used for training and prediction.
        """
        self.data = data
    
    def train_sarimax(self, show_summary=True, **kwargs):
        """
        Trains a SARIMAX model on the data.
        Args:
            show_summary (bool, optional): Whether to print a summary of the model after training. Defaults to True.
            **kwargs: Additional arguments to be passed to SARIMAX.
        Returns:
            A trained SARIMAX model.
        """
        model = SARIMAX(self.data, simple_differencing=False, **kwargs).fit(disp=False)
        if show_summary:
            print(model.summary())
        return model
    
    def train_exponential_smoothing(self, model='additive' ,show_summary=True, **kwargs):
        """
        Trains a exponential smoothing model: If model == 'additive' then the model will be built using ExponentialSmoothing from 
        statsmodels.tsa.statespace.exponential_smoothing else if model == 'multiplicative' then the model will be built in 
        statsmodels.tsa.holtwinters.
        #latest update
        """
        
        if model == 'additive':
            model_obj = ExponentialSmoothing(self.data, **kwargs).fit(optimized=True)
            
        elif model == 'multiplicative':
            model_obj = holtwinters_ES(self.data, **kwargs).fit(optimized=True)
            
        else:
            raise ValueError(f"Invalid model: {model}")
        
        if show_summary:
            print(model_obj.summary())
            
        return model_obj

    def train_sequential(self, model_type: str, n_steps: int, n_target: int, epochs=200, batch_size=16, optimizer='adam', neurons=50, activation='relu', show_graph=True, validation_split=0.2, **kwargs):
        """
        Trains a model on the data.
        Args:
            model_type (str): The type of model to train. Either 'lstm' or 'ann'.
            n_steps (int): The number of time steps to use for each input sequence.
            n_target (int): The number of features in each input sequence.
            epochs (int, optional): The number of epochs to train the model for. Defaults to 200.
            batch (int, optional): The batch size for training. If None, the default batch size is used. Defaults to None.
            optimizer (str or optimizer object, optional): The optimizer to use for training. Defaults to 'adam'.
            **kwargs: Additional arguments to be passed to the model.
        Returns:
            last_sequence (np.ndarray): The last input sequence used for training.
            model (keras.models.Sequential): The trained model.
        """
        np.random.seed(143)
        tf.random.set_seed(143)
        random.seed(143)

        sequencer = DataPreprocessing()
        X, y = sequencer.make_sequence(self.data, n_steps)
        last_sequence = X[-1]

        model = Sequential()
        if model_type.lower() == 'lstm':
            model.add(LSTM(neurons, activation=activation, return_sequences=True, input_shape=(n_steps, n_target)))
            model.add(LSTM(neurons, activation=activation))
        elif model_type.lower() == 'ann':
            model.add(Flatten(input_shape=(n_steps, n_target)))
        else:
            raise ValueError("Invalid model_type. Supported types are 'lstm' and 'ann'.")

        model.add(Dense(1))
        metrics = [RootMeanSquaredError(name='rmse'),
                   MeanAbsolutePercentageError(name='mape'), 
                   MeanAbsoluteError(name='mae')]
        model.compile(optimizer=optimizer, loss='mse', metrics=metrics)
        history = model.fit(X, y, batch_size=batch_size, epochs=epochs, validation_split=validation_split, **kwargs)

        result_df = pd.DataFrame(history.history)
        vs = result_df[result_df.columns[result_df.columns.str.contains('val')]]
        ts = result_df[result_df.columns[~result_df.columns.str.contains('val')]]

        if show_graph:
            for v, t in zip(vs, ts):
                plt.figure(figsize=(9, 3))
                plt.plot(vs[v], label="validation")
                plt.plot(ts[t], label="train")
                plt.title(f'{str.upper(t)} per Epoch')
                plt.legend()
                plt.show()

        return last_sequence, model


    def train_prophet(self, **kwargs):
        """
        Trains a NeuralProphet model on the data.
        Args:
            **kwargs: Additional arguments to be passed to NeuralProphet.
        Returns:
            A trained NeuralProphet model.
        """
        
        set_random_seed(143)
        np.random.seed(143)
        random.seed(143)
        
        df = self.data.reset_index()
        df.columns = ['ds', 'y']
        df = df.drop_duplicates(subset=['ds'])
        model = NeuralProphet(**kwargs)
        model.fit(df)
        return model


class Forecaster:
    """
    Forecaster class
    This class provides methods to make forecasts using the trained models.
    forecast_sarimax(model: SARIMAX) -> pd.Series
    This method uses the given SARIMAX model to make future predictions for a fixed number of time steps and returns the predicted values as a Pandas series.
    forecast_lstm(model: Sequential, last_sequence: np.ndarray, n_features: int) -> pd.Series
    This method uses the given LSTM model to make future predictions for a fixed number of time steps using the last sequence of input data, and returns the predicted values as a Pandas series.
    forecast_neural_prophet(model, df_future) -> pd.DataFrame
    This method uses the given NeuralProphet model to make future predictions and returns the predicted values along with their associated uncertainty intervals as a Pandas dataframe. The df_future argument is a Pandas dataframe that specifies the future time steps for which predictions are to be made.
    """
    def __init__(self, time_steps: int):
        """
        Initialize a Forecaster object.
        Args:
            time_steps: The number of time steps to forecast.
        """
        self.time_steps = time_steps
    
    def forecast_sarimax(self, model: SARIMAX) -> pd.Series:
        """
        Generate forecasts using a fitted SARIMAX model.
        Args:
            model: A fitted SARIMAX model object.
        Returns:
            A pandas Series containing the forecast values.
        """
        return model.forecast(self.time_steps).reset_index(drop=True)
    
    def forecast_exponential_smoothing(self, model: ExponentialSmoothing) -> pd.Series:
        """
        Generate forecasts using a fitted Exponential Smoothing model.
        
        Args:
            model: a fitted ExponentialSmoothing model object.
        
        Returns:
            A pandas Series containing the forecast values.
        """
        return model.forecast(self.time_steps).reset_index(drop=True)

    def forecast_sequential(self, model: Sequential, last_sequence: np.ndarray, n_target: int) -> pd.Series:
        """
        Generate forecasts using a fitted LSTM model.
        Args:
            model: A fitted LSTM model object.
            last_sequence: The last sequence of the input data used to fit the model.
            n_target: The number of features in the input data.
        Returns:
            A pandas Series containing the forecast values.
        """
        n_steps = last_sequence.shape[0]
        temp_input = list(last_sequence.reshape(-1))
        lst_output = []
        i = 0
        while i < self.time_steps:
            if len(temp_input) > n_steps * n_target:
                x_input = np.array(temp_input[-n_steps * n_target:]).reshape((1, n_steps, n_target))
                yhat = model.predict(x_input, verbose=0)
                temp_input.append(yhat[0][0])
                lst_output.append(yhat[0][0])
                i += 1
            else:
                x_input = np.array(temp_input[-n_steps * n_target:]).reshape((1, n_steps, n_target))
                yhat = model.predict(x_input, verbose=0)
                temp_input.append(yhat[0][0])
                lst_output.append(yhat[0][0])
                i += 1
        return pd.Series(lst_output)

    def forecast_prophet(self, model: NeuralProphet, data: pd.DataFrame) -> pd.Series:
        """
        Generate forecasts using a fitted NeuralProphet model.
        Args:
            model: A fitted NeuralProphet model object.
            data: The input data used to fit the model as a pandas DataFrame.
        Returns:
            A pandas Series containing the forecast values.
        """
        df = data.reset_index()
        df.columns = ['ds', 'y']
        df = df.drop_duplicates(subset=['ds'])

        future = model.make_future_dataframe(df, periods=self.time_steps)
        forecast = model.predict(future)
        forecast_values = forecast['yhat1'].tail(self.time_steps)
        return forecast_values


def evaluate_forecast(y_test, y_pred):
    """
    Evaluate a time series forecast using common metrics.
    
    Parameters:
    y_test (numpy.ndarray): Array of true values with shape (n_samples,).
    y_pred (numpy.ndarray): Array of predicted values with shape (n_samples,).
    
    Returns:
    dict: Dictionary containing metrics and their values.
    """
    # Calculate metrics
    mse = np.mean((y_test - y_pred)**2)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((y_test - y_pred) / y_test))
    mae = np.mean(np.abs(y_test - y_pred))
    mase = np.mean(np.abs(y_test - y_pred)) / np.mean(np.abs(np.diff(y_test)))
    
    # Store metrics in dictionary
    metrics = {'MSE': mse, 'RMSE': rmse, 'MAPE': mape, 'MAE': mae, 'MASE': mase}
    
    return metrics