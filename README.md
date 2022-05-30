# Recommendation System
Product recommendation system for e-commerce with a hybrid method.

## Description
This API provides a "Related Products" recommendation for the shopping cart page of the e-commerce site.

Four different recommendation methods were used:
  - Content-Based Filtering
  - Collaborative Filtering
  - Popularity Based
  - Hybrid Approaches

## Content-Based Filtering

In this method, the name, brand, category and subcategory information in the metadata of the products is used.
Category, brand and subcategory information has been combined.
With these combinations, the similarity matrix of the products was calculated.
In addition, a similarity matrix was calculated according to the product name information.
These matrices were then aggregated with the weighting parameters.

## Collaborative Filtering

In this method, the cart page of other sessions that match the products is examined.
The products selected by each session during the day were assumed to be the cart page.
The products selected together on the previous cart pages are matched.
Thus, recommendations are presented to the new cart pages, which are similar to the choices of other users.
In fact, we can say that it is a cart page-based recommendation method.
People's cart pages will help other people buy products.

## Popularity Based

Date weighting is done according to the dates in the events data.
The total number of events of the products is calculated.
Then these total numbers are multiplied by the weighting values
The most selected products in recent days are assumed to be more popular, thus generating popularity scores.

## Hybrid Approaches

After weighting the results of all these approaches(Content-Based,Collaborative,Popularity), the final recommendations are reached.

# User Guide


Meta and event data should be put in the data folder in the main directory or the path should be defined with settings.py.

Api.py must be run.


It is ready to use when the text below appears.

Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


Let's Try


The program runs when you go to the address below in your browser.

 http://127.0.0.1:5000/tables


If the program is run for the first time, it extracts the necessary files to the db folder.
This process can take up to 30 seconds.


Recommendations for a randomly generated cart page will appear on the browser screen.
![exp_ss](https://user-images.githubusercontent.com/106500758/170994387-81bee443-dab1-4045-b40c-f319e0657f1b.png)

Note: If you want to create your own cart page, you can write an address like below.

http://127.0.0.1:5000/tables?id=["HBV00000LMKWX","HBV00000NG8KC"]

HBV00000LMKWX and HBV00000NG8KC in the list are the product ids.

