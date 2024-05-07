# Personalized Book Recommendation System

## Introduction

Personalized recommendations are crucial for companies to maximize revenue. While revenue generation primarily relies on user subscriptions and inventory listing fees, personalized recommendations play a pivotal role. This project aims to investigate and enhance recommendation models to deliver more tailored suggestions to users.

### Objective

The primary objective is to offer users more personalized recommendations, thereby aiding e-commerce giants in making informed decisions. Additionally, this system can assist companies in assessing the significance of various variables in recommendations and facilitating informed decisions for future development.

## Research Questions

- What evaluation metrics are used for recommendation systems, and how is personalization quantified?
- Which recommendation models are most effective in providing personalized suggestions?
- What factors are essential for enhancing recommendations without compromising key metrics such as the revenue of the giants?

## Data Overview

- **Main Data Columns**: `reviewerID`, `asin`, `reviewerName`, `overall`, `combined_text`, `category`, `description`, `title`, `brand`, `rank`, `main_cat`, `price`
- **Potential Columns**: `asin`, `reviewerID`, `overall`, `combined_text`, `category`, `avg_rating` (calculated), `num_reviews` (calculated)

## Data Preparation

### Core Filtering

- Applied 2-Core filtering technique to the cleaned merged Data Frame.
- Train – Test Split: Identified unique users and split interactions into training and testing sets.
- Unique Users: 13652, Unique Books: 2758

## Evaluation Metrics

- **NDCG@5**: Normalized Discounted Cumulative Gain
- **Recall@5**: Measures the proportion of relevant items recommended among the top 5 suggestions.

### Model Results

#### Content-Based Model (TFIDF + Cosine Similarity)

- Mean Recall@5: 0.0218
- Mean NDCG@5: 0.0144

#### User-Based Collaborative Filtering (KNN)

- Mean Recall@5: 0.00092
- Mean NDCG@5: 0.00060

#### Matrix Factorization

- Mean Recall@5: 0.0147
- Mean NDCG@5: 0.0107

#### Item-Based Collaborative Filtering (Cosine Similarity, Pearson Similarity)

| Model             | Recall@5 | NDCG@5 |
|-------------------|----------|--------|
| Cosine Similarity | 0.18     | 0.17   |
| Pearson Similarity| 0.1798   | 0.1732 |

## Data Enhancement and Filtering

- Derived crucial metrics: `avg_rating` and `num_reviews`.
- Filtered interactions dataframe based on `num_reviews` threshold.

## Impact Analysis

- 3% of books drive 50% of engagement.
- Enriched data modeling boosts personalized recommendations (40% recall, high NDCG), cutting inventory costs.
- Recommender model as a product: Balance personalization with revenue by maintaining diverse inventory.

## Category Analysis

- Utilized the `Category` column for in-depth analysis.
- Generated a JSON file containing top 5 books from each category.

