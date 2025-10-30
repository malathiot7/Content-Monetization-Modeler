# Content-Monetization-Modeler
Project Overview
In the rapidly evolving creator economy, understanding how different factors influence YouTube ad revenue is vital for content creators and media companies.
This project focuses on building a Linear Regression-based predictive model that estimates YouTube ad revenue for individual videos based on various performance and contextual metrics.
The model will be integrated into a Streamlit web application, allowing users to interactively input video metrics and predict expected ad revenue
Objectives
•	Predict ad_revenue_usd using regression techniques.
•	Understand which factors most strongly influence revenue.
•	Build a Streamlit app for interactive predictions and insights visualization.
•	Provide data-driven recommendations for content strategy optimization and revenue forecasting.

Dataset Information
Format: CSV
Size: ~122,000 rows
Source: Synthetic (for educational purposes)
Target Variable: ad_revenue_usd

Columns Overview
Column	Description
video_id	Unique video identifier
date	Upload/reporting date
views	Total views
likes	Total likes
comments	Total comments
watch_time_minutes	Total watch time in minutes
video_length_minutes	Length of the video
subscribers	Channel’s subscriber count
category	Video category (e.g., Entertainment, Education)
device	Device type (e.g., Mobile, Desktop)
country	Viewer’s country
ad_revenue_usd	Ad revenue in USD (Target)

Exploratory Data Analysis (EDA)
Perform a comprehensive EDA to uncover patterns and insights.
Key Analyses
•	Distribution of target variable ad_revenue_usd.
•	Correlation heatmap to identify relationships.
•	Boxplots and scatterplots for detecting outliers.
•	Category-wise revenue comparison (e.g., revenue by category, country, or device).

Model Building
Models to Experiment With
1.	Linear Regression
2.	Ridge Regression
3.	Lasso Regression
4.	Random Forest Regressor
5.	Gradient Boosting Regressor
Workflow
1.	Split data into train/test sets (e.g., 80/20).
2.	Train each model and tune hyperparameters.
3.	Evaluate performance using:
o	R² Score
o	RMSE (Root Mean Squared Error)

Insights and Interpretation
•	Views and Watch Time are the strongest predictors of revenue.
•	Engagement Rate positively correlates with higher ad revenue.
•	Certain categories (like Technology, Entertainment) yield better monetization rates.
•	Country and device types also affect revenue due to ad pricing differences

Streamlit Web App
Features
•	Input fields for user metrics (views, likes, comments, etc.).
•	Predicts expected ad_revenue_usd using trained model.
•	Displays model insights and feature importance.
•	Includes basic EDA visualizations.

Example Layout
|---------------------------------------|
| YouTube Ad Revenue Predictor          |
|---------------------------------------|
| [Enter Views]                         |
| [Enter Likes]                         |
| [Enter Comments]                      |
| [Enter Watch Time]                    |
| [Select Category / Device / Country]  |
| [Predict Button]                      |
| Predicted Revenue: $XXX.XX            |
|---------------------------------------|
| [Visualizations Section]              |
|---------------------------------------|

