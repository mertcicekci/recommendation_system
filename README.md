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
In fact, we can say that it is a cart page-based recommendation method.
Thus, recommendations are presented to the new cart pages, which are similar to the choices of other users.

## Popularity Based

Date weighting is done according to the dates in the events data.
The total number of events of the products is calculated.
Then these total numbers are multiplied by the weighting values
The most selected products in recent days are assumed to be more popular, thus generating popularity scores.

## Hybrid Approaches

After weighting the results of all these approaches(Content-Based,Collaborative,Popularity), the final recommendations are reached.

# User Guide

