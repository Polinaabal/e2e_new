# GitHub PyCharm project

The final goal of our project is to **predict rental prices** in Saint-Petersburg based on the dataset provided. Initially we had data on the real estate listings from Yandex.Realty classifieds for the period *from 2016 till the middle of August 2018*. 

We applied machine learning algorithms to predict the rental prices.  

## Analyzing the dataset

We looked at our target variable "Last_price". To clean the data from the outliers we removed from the set extreme records where price per sq m was substantially different from the median of the building. 

  

     rent_df_cleaned = rent_df_spb[~((rent_df_spb.price_per_sq_m/rent_df_spb.house_price_sqm_median) > 5)]
        rent_df_cleaned = rent_df_cleaned[rent_df_cleaned.last_price < 1000000]
        rent_df_cleaned = rent_df_cleaned[~((rent_df_cleaned.price_per_sq_m > 3000) 
                                             & ((rent_df_cleaned.house_price_sqm_median < 1000) 
                                                | (rent_df_cleaned.house_price_sqm_median == rent_df_cleaned.price_per_sq_m)))]
        rent_df_cleaned = rent_df_cleaned[~((rent_df_cleaned.price_per_sq_m < 250) 
                                       & (rent_df_cleaned.house_price_sqm_median/rent_df_cleaned.price_per_sq_m >= 2))]
        rent_df_cleaned = rent_df_cleaned[~((rent_df_cleaned.price_per_sq_m < 200) 
                                                  & (rent_df_cleaned.price_per_sq_m == rent_df_cleaned.house_price_sqm_median))]e`

Looking at the target variable histogram, we see that it has right-skewed distribution. 
![enter image description here](https://github.com/Polinaabal/e2e_new/blob/main/Pictures/histogram.png?raw=true)
The chart below shows how many missing values we had in the data source for several features. We replaced them with the house median values.
![enter image description here](https://github.com/Polinaabal/e2e_new/blob/main/Pictures/missing.png?raw=true)
## Building prediction model

Step 1. In order to build a good model we had to preprocess our initial dataset:
-  we took into account only apartments in St.-Pet., and not in the oblast'
- we calculated price per 1 sq m for each record
- we excluded outlier records from the dataset
- we calculated  the median price for a building 


Step 2. We had to create  train and test datasets that would be differentiated by the time period. 

 - train dataset: 1/1/2018 -3/31/2018
 - test dataset: 4/1/2018 - 6/1/2018

Step 3. We drop unnecessary columns that would not be useful in our model construction. We did not include renovation factor since it is more impactful in analysing selling prices. Yet, we included house median price as usually, the price for a apartment is correlated with the prices for already exposed apartments in the building. In our case the final train and test datasets contained the following headers:
![enter image description here](https://sun9-53.userapi.com/s/v1/ig2/rj00vqL_mSBI84Bk6jQMbMGyAScMrvdRM20Sg-WOSZPiUdXNp2iBkeVdVUPGbhqsbsRUgj4CHl7XbyckBLOgQLWZ.jpg?size=972x364&quality=96&type=album)
Step 4.  Among different models 2 showed superior results: Random forest (with Gridsearch) and Catboost regressor. Their performance metrics are close to each other. Yet, RF showed a bit better results (see the table below).
|  | Random Forest |Catboost
|--|--|--|--
MAE	| 0.22 | 0.23 |
MSE	| 0.16 | 0.18 |
RMSE| 0.40 | 0.43 |

Models' performance comparison:

|  | Random Forest |Catboost
|--|--|--|--
Average Error	| 0.7884 degrees | 0.7890 degrees` |
Accuracy	| 181.58%	 | 180.79% |

Random forest visualised results (predictions vs. validation values)
![enter image description here](https://github.com/Polinaabal/e2e_new/blob/main/Pictures/RF.png?raw=true)

Catboost regressor visualised results (predictions vs. validation values)
![enter image description here](https://github.com/Polinaabal/e2e_new/blob/main/Pictures/catboost.png?raw=true)


## How to install instructions and run your app with virtual environment

To run the app w/o a docker in a virtual environment, one should enable the VM and create venv there using the following commands: 

    sudo apt install python3.8-venv
    python3 -m venv env
    source env/bin/activate	
Then one should pull the git repository with the app to the venv. The rep should contain files: model.pkl, model2.pkl, scaler_x.pkl, scaler_y.pkl and app.py.

    git clone git@github.com:Polinaabal/e2e_new

Then one should install all the required libraries mentioned in the requirements.txt file. 	Afterwards Port 5441 should be enabled using the code:

    sudo ufw allow 5441
After that the app could be launched in the Postman using the public Ipv4 of the VM and port - or simply in the browser address line. 	The request should contain all the required parameters (floor, number of rooms, area, house_median_price, model_version). Otherwise, the 500 error will be returned. 	

## Information about Dockerfile and describe its content

Our Dockerfile contains the following code with all the necessary pip installations with the command to run the app: 

    from ubuntu:20.04  
    MAINTAINER Polina Abalakova  
    RUN apt-get update -y  
    COPY . /opt/gsom_predictor  
    WORKDIR /opt/gsom_predictor  
    RUN apt install -y python3-pip  
    RUN pip3 install -r requirements.txt
    CMD python3 app.py

## How to run app using docker and which port it uses

In order to run an app using docker, you need to pull the app from Docker Hub and run it:

    docker pull abalakova2/gsom_predictor:v.0.4
    docker run --network host -d abalakova2/gsom_predictor:v.0.4
Port 5441 is used here, so to run the app one should enter the public IPv4 of the VM and port 5441 in Postman. 


