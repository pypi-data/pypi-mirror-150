from logging import raiseExceptions
from scipy.stats.contingency import association
import pandas as pd
import numpy as np
from itertools import combinations


# Class definition
class Association:
    def __init__(self, dataframe, method):
        self.dataframe = dataframe
        self.method = method
        self.matrix = None
        
    def check_df(self):
        if isinstance(self.dataframe, pd.DataFrame):
            self.data = self.dataframe
        else:
            raise TypeError("data frame must be an instance of pd.DataFrame")
        
    def select_variable(self):
        self.obj_columns = self.data.select_dtypes(include = ["object"]).columns
        
        if len(self.obj_columns) == 0:
            raise KeyError("No object variables found")
        
    def pairwise_mat(self):
        self.matrix = pd.DataFrame(
            np.eye(len(self.obj_columns)),
            columns = self.obj_columns,
            index = self.obj_columns
        )
        
    def compute_pair(self):
        n = len(self.obj_columns)
        all_combination = combinations(self.obj_columns, r = 2)
        
        # Iterating through combinations
        for comb in all_combination:
            i = comb[0]
            j = comb[1]
            
            # crosstab calculation
            ctab = pd.crosstab(self.data[i], self.data[j])
            
            val = association(ctab, method = self.method)
            self.matrix[i][j], self.matrix[j][i] = val, val
            
    def fit(self):
        self.check_df()
        self.select_variable()
        self.pairwise_mat()
        self.compute_pair()
        
        return self.matrix