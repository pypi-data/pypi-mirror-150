<p align="center">
    <a href="https://katonic.ai/">
      <img src="docs/assets/katonic_logo.png" width="550">
    </a>
</p>
<br />

[![Docs Latest](https://img.shields.io/badge/docs-latest-blue.svg)](https://docs.katonic.ai/)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/katonic-dev/katonic-sdk/blob/master/LICENSE)

# Katonic Python SDK

The document guides data scientists and developers to build ML applications on the Katonic MLOps platform. Katonic SDK is a repository of abstract python classes and libraries. The Katonic Python SDK was developed in Python and is designed to help data scientists and developers interact with Katonic from their code, experiments and models. Through the SDK, you can create experiments, manage models, automate your machine learning pipeline and more.


The topics in this page:

- Connectors
- Feature Store
- Experiment Operations
- Registry Operation
- Pipelines = KFP Pipeline SDK = Pipeline Operations + create pipeline
- Drift

### Connectors 

A typical AI model life cycle starts with loading the data into your workspace and analyzing it to discover useful insights. for that you can use Katonic's SDK, there are several connectors inside it you can use to load the data and put it where ever you want to work with. Ex. Azure blob, MySql, Postgres etc. 

### Feature Store

Once you loaded all the necessary data that you want to work with. You'll do the preprocessing of it. Which consists of Handling the missing values, Removing the Outliers, Scaling the Data and Encoding the features etc. Once you've finished preprocessing the data. You need to ingest the data into a Feature store. 

By uploading the clean data to a feature store, you can share it across the organization. So that other teams and data scientist working on the same problem can make use of it. By this way you can achieve Feature Reusability.

Apart from that, Machine Learning models are completely dependent on the data that was provided by the Data Scientist. So if there was a change in the Infrastructure of the data, it may lead to break the ML models. So The transformations and Logics that used for training data will also implies for the serving data, For that we can retrieve the processed features from an existing feature store for serving purpose. This will improve the consistency between the training data and serving data otherwise it will lead to training-serving skew.

### Experiment Operations 

Experiment Operations includes all the Data science activities like loading the data, performing the Exploratory Data Analysis, Model training and Tracking the metrices. All of these actions can be done by the Auto ML component inside the Katonic SDK. You can train the models with in few lines codes with out explicitly writing the code. Even all the metrics for Classification and Regression will get catalouged using SDK. Available Metrices are Accuracy score, F-1 score, Precison, Recall, Log loss etc for Classificaiton and Mean Squared Error, Mean Absolute Error and Root Mean Squared Error for Regression usecases.

### Registry Operations

Once you finished training the models with your data. Katonic's SDK will keep track of all the models and store the Model metadata and metrices inside the Experiment Registry. From there you can choose the best model and send it into Model Registy.

In Model Registy you can store the Best models according to your performance Metrices. By using the model registy you can tag the models with `staging` or `production`. The models that are with the tag `production` can be Deployed to the production and the models with `staging` tag can get a review check from the QA team and get to the further stages.

### Pipeline

No Data Scientist want to do the same thing again and again, instead of that Data Scientist want to use the previous work that he had done for the future purposes. We can do the same thing inside an AI Model Life Cycle. Once we are done with model training and registering the best model to model registry. We can convert all the work that we had done till now into a Scalable Pipeline. For that you can use the Pipelines component inside the Katonic SDK. By using this you can convert all your data science work into pipeline with in few lines of code. If you want to do the same operations with the different data, you just need to change the data source and run the pipeline. Every thing will get done automatically in a scalable manner.

### Drift

An AI model life cycle will not end with the model deployment. You need to monitor the model's performance continuously in order to detect the model detoriation or model degradation. Drift component from Katonic's SDK will help you to find the Drift inside your data. It will perform certain statistical analysis upon the data in order to check if the upcoming data has any Outliers or the data is abnormal it will let you know through a Visual representaion.
