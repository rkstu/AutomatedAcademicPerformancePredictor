import sys
from dataclasses import dataclass
import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

class DataTransformationConfig:
  preprocessor_obj_file_path = os.path.join('artifacts', 'preprcessor.pkl')

class DataTransformation:
  def __init__(self):
    self.data_transformation_config = DataTransformationConfig()

  def get_data_transformer_object(self):
    '''
    This function is responsible for data transformation
    '''
    try:
      numerical_columns = ["writing_score", "reading_score"]
      categorical_columns = [
          "gender",
          "race_ethnicity",
          "parental_level_of_education",
          "lunch",
          "test_preparation_course",
      ]
      num_pipeline = Pipeline(
        steps=[
          ("imputer", SimpleImputer(strategy='median'),
          ("scaler", StandardScaler()))
        ]
      )
      cat_pipeline = Pipeline(
        steps=[
          ("imputer", SimpleImputer(strategy='most_frequent')),
          ("one_hot_ecoder", OneHotEncoder()),
          ("scalar", StandardScaler())
        ]
      )

      logging.info("Numerical columns standard scaling completed")
      logging.info("Categorical columns encoding completed")

      logging.info(f"Categorical columns: {categorical_columns}")
      logging.info(f"Numerical columns: {numerical_columns}")
      
      preprcessor = ColumnTransformer(
        [
          ("num_pipeline", num_pipeline, numerical_columns),
          ("cat_pipelines", cat_pipeline, categorical_columns)
        ]
      )

      return preprcessor
  
    except Exception as e:
      raise CustomException(e, sys)


  def initiate_data_transformation(self, train_path, test_path):

    try:
      train_df = pd.read_csv(train_path)
      test_path = pd.read_csv(test_path)

      logging.info("Read train and test data completed")

      logging.info("Obtaining preprocessing object")

      preprocessor_obj = self.get_data_transformer_object()

      target_column_name="math_score"
      numerical_columns = ["writing_score", "reading_score"]


      input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)

      logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )
      # input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
      # input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

      # train_arr = np.c_[
      #     input_feature_train_arr, np.array(target_feature_train_df)
      # ]
      # test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

      logging.info(f"Saved preprocessing object.")
      save_object(
        file_path = self.data_transformation_config.preprocessor_obj_file_path,
        obj = preprocessor_obj
      )

    except Exception as e:
      raise CustomException(e, sys)