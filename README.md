# 🎬 Movie Recommendation System

This is a content-based Movie Recommendation System built using Python and Pandas. It uses the **TMDB 5000 Movie Dataset**, and applies **text processing** and **cosine similarity** to recommend movies that are similar in content.

---

## 🚀 Features

- Content-based filtering using:
  - Movie **overview**
  - **Genres**
  - **Keywords**
  - **Cast**
  - **Director**
- Text vectorization with **CountVectorizer**
- Similarity measurement using **Cosine Similarity**
- Top 5 similar movie recommendations
- Evaluation logic using **Precision@5**

---

## 🧠 How It Works

1. **Data Cleaning & Merging**:
   - Merges `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` on the title.

2. **Feature Extraction**:
   - Extracts important columns like `overview`, `genres`, `keywords`, `cast`, and `crew`.

3. **Text Preprocessing**:
   - Converts lists of genres, keywords, etc., into a clean format.
   - Combines all into a new column called `tags`.

4. **Vectorization**:
   - Applies `CountVectorizer` to convert text data to numeric vectors.

5. **Similarity Computation**:
   - Uses `cosine_similarity` to compare vectors and find similar movies.

6. **Recommendation**:
   - When a user inputs a movie title, it returns the top 5 most similar movies.

---

## 🧪 Accuracy Checking

The project includes a small benchmarking script to evaluate **Precision@5**, comparing recommendations with known similar movies.

```python
evaluate_precision(test_cases)
