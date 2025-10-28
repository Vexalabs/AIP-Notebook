import pandas as pd
from sklearn.linear_model import LinearRegression

class Model:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, df: pd.DataFrame):
        """
        Trains the model on the given dataframe.
        """
        X = df[['years_of_experience']]
        y = df['salary']
        self.model.fit(X, y)

    def predict(self, data):
        """
        Makes a prediction based on the given data.
        """
        return self.model.predict(data)
