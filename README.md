# 🎬 Movie Recommendation System

## 📌 About this project

I built this project to understand how recommendation systems actually work behind the scenes. The idea is simple — when you like a movie, the system should be able to suggest similar movies you might enjoy.

Instead of using complex user data, this project focuses on **content-based filtering**, meaning it recommends movies based on their features like genre, cast, keywords, etc.

---

## 🚀 What it can do

* Recommend movies similar to the one you enter
* Works instantly inside a notebook
* Uses similarity scores to find related content
* Easy to understand and extend

---

## 🧠 How it works (in simple terms)

Every movie is converted into a set of features (like genre, cast, keywords).

Then:

* These features are combined into a single representation
* A similarity score is calculated between movies
* The system picks the most similar ones and recommends them

So basically, it finds movies that are "close" to each other in terms of content.

---

## 🛠️ Tech used

* Python
* Pandas
* NumPy
* Scikit-learn

---

## ▶️ How to run this project

1. Open the notebook in Google Colab or Jupyter Notebook
2. Run all the cells
3. Enter a movie name when asked
4. You’ll get a list of recommended movies

---

## 📊 Example

Input:

```
Avatar
```

Output (example):

```
Titanic
Guardians of the Galaxy
Avengers
```

---

## ⚠️ Limitations

* Recommendations depend only on the dataset
* No personalization (same input → same output)
* Doesn’t learn from user behavior yet

---

## 🔮 What I plan to improve

* Add collaborative filtering (user-based recommendations)
* Build a simple web app (maybe using Streamlit)
* Improve recommendation quality

---

## 👤 Author

Lakshpreet Kaur<br>
https://github.com/Lakshpreetkaur

---

If you found this useful or interesting, feel free to star the repo ⭐
