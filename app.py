import warnings
warnings.filterwarnings('ignore')
import pandas as pd 
import numpy as np 
import sys
import json
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import zipfile
test_df = pd.read_csv('test_df.csv', index_col=0)
with zipfile.ZipFile('z.zip', 'r') as zip_ref:
    csv_file = zip_ref.open('train_df1.csv')  # Assuming the CSV file is named 'data.csv'
    train_df = pd.read_csv(csv_file)  # Read the CSV data
    # ... use df ...


def get_top_item_recommendations(user_id, train_df, top_k=20):
    # Creating the item-user matrix
    item_user_matrix = train_df.pivot_table(index='asin', columns='reviewerID', values='overall').fillna(0)

    # Fill missing values with zeros
    item_user_matrix.fillna(0, inplace=True)

    # Normalize user-item matrix
    matrix_norm = item_user_matrix.subtract(item_user_matrix.mean(axis=1), axis=0)

    # Fill missing values with zeros
    matrix_norm.fillna(0, inplace=True)

    # Calculate Cosine Similarity
    item_similarity_matrix = pd.DataFrame(cosine_similarity(matrix_norm),
                                           index=item_user_matrix.index,
                                           columns=item_user_matrix.index)

    # Get items rated by the user
    user_items = train_df[train_df['reviewerID'] == user_id]['asin'].unique()

    # Initialize an empty Series to store summed similarity scores
    similar_items_scores = pd.Series(dtype=float)

    for item in user_items:
        # Check if the item exists in the item_similarity_matrix to avoid KeyError
        if item in item_similarity_matrix.index:
            # Drop the items already rated by the user and sum similarity scores
            item_scores = item_similarity_matrix.loc[item].drop(index=user_items, errors='ignore')
            similar_items_scores = similar_items_scores.add(item_scores, fill_value=0)

    # Sort the items based on their summed similarity scores
    top_k_items_asin = similar_items_scores.sort_values(ascending=False).head(top_k).index.tolist()

    recommendations_count = 0
    recommendations = []
    for asin in top_k_items_asin:
        book_title = train_df[train_df['asin'] == asin]['title'].iloc[0]
        rating = train_df[train_df['asin'] == asin]['avg_rating'].iloc[0]
        if not pd.isna(book_title):
            recommendations.append((book_title, rating))
            recommendations_count += 1
            if recommendations_count >= 5:
                break
    return recommendations


def user_exists(user_id, test_df):
    return user_id in test_df['reviewerID'].unique()

def main(train_df):
    st.set_page_config(layout="wide")
    st.title("Book Recommendation System")


    # Customize the sidebar
    markdown = """
    Used Item Based Collaborative Filtering Method Using Cosine Similarity
    """
    logo = "https://miro.medium.com/v2/resize:fit:1100/format:webp/0*kd1E9mKjRrCZ4K6B.jpg"
    st.sidebar.image(logo)
    st.sidebar.info(markdown)

    # Load category books data
    with open('category_books.json', 'r') as f:
        category_books_dict = json.load(f)

    # List of top categories
    top_categories = [
        'Fantasy', 'Fiction',
        'Mystery', 'Biographies', 
        'Cookbooks', 'Contemporary', 'History', 
        "Children's Books", 'Arts', 'Social Sciences'
    ]
    st.write("Try using existing user IDs:")
    st.write(", ".join(["A1FEFGP7QVQVDK", "AHXMDCU0N15TN", "A3T6R1GAFRP1I9", "ALRBLOW3ETCY1",
           "A8GZ7Z7MHX2DU"]))


    user_input = st.text_input("Please enter your user ID:")

    if user_input:
        if user_exists(user_input, test_df):
            recommendations = get_top_item_recommendations(user_input,train_df)
            show_button = st.button("Proceed")
            if show_button:
                st.subheader(f"Top 5 book recommendations for User {user_input}:")
                for i, (book_title, rating) in enumerate(recommendations, 1):
                    st.write(f"{i}. {book_title}, Rating: {rating}")      
        else:
            st.write("You seem to be a new user.")
            selected_category = st.selectbox("Please choose a category from the following:", top_categories)
            show_button = st.button("show recommendations")
            if show_button:
                if selected_category:
                    st.subheader(f"Top 5 books in {selected_category}:")
                    count = 1
                    for num in category_books_dict[selected_category]:
                        book_title, rating = num[0], num[1]
                        st.write(f"{count}.{book_title}, Rating: {rating}")
                        count += 1
                    
if __name__ == "__main__":
    main(train_df)
    sys.exit()
