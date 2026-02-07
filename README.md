# YouTube Mood Ring 💍📊

A Python-based data science tool that performs automated sentiment analysis on YouTube comments. It extracts user data via the YouTube Data API v3, processes natural language using NLTK (VADER), and visualizes the "vibe" of a community over time.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## 🚀 Features

* **Automated Fetching:** Retrieves thousands of comments using YouTube API pagination to avoid recency bias.
* **Sentiment Engine:** Classifies comments as **Positive**, **Neutral**, or **Negative** using VADER (Valence Aware Dictionary and sEntiment Reasoner).
* **Time Series Analysis:** Tracks how audience sentiment shifts over months or years.
* **Engagement Correlation:** Analyzes if "hate-watching" (negative sentiment + high likes) is driving engagement.
* **Visual Dashboard:** Generates a professional dashboard with:
    * **Pie Chart:** Overall mood distribution.
    * **Bar Chart:** Comment volume by sentiment.
    * **Scatter Plot:** Sentiment vs. Like Count.
    * **Time Series Line:** Average mood over time.
    * **Word Cloud:** Most frequent topics discussed.

## 🛠️ Tech Stack

* **Python 3.x**
* **Pandas:** Data manipulation and CSV export.
* **NLTK:** Natural Language Processing (VADER).
* **Matplotlib:** Data visualization and dashboard generation.
* **WordCloud:** Text visualization.
* **Google Client Library:** API interaction.

## ⚙️ Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ananyajoshi-cseai/YouTube-Mood-Ring-Ananya.git](https://github.com/ananyajoshi-cseai/YouTube-Mood-Ring-Ananya.git)
    cd YouTube-Mood-Ring-Ananya
    ```

2.  **Set up the environment:**
    ```bash
    python -m venv venv
    # For Windows:
    .\venv\Scripts\activate
    # For Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure API Key:**
   * 🔑 **Need a key?** Go to the [Google Cloud Console](https://console.cloud.google.com/), create a project, enable "YouTube Data API v3", and generate an API Key.
   * Create a file named `.env` in the root folder.
   * Add your key like this:
     ```
     YOUTUBE_API_KEY=your_api_key_here
     ```

5.  **Run the analysis:**
    * Open `mood_ring.py` and paste the YouTube Video URL you want to analyze.
    * Run the script:
        ```bash
        python mood_ring.py
        ```
     * **Tip:** Don't have an API key? You can check the ([comments_VIDEO-ID.csv](./comments_ERCMXc8x7mc.csv)) file included in this repo to see what the raw data looks like!

## 📈 Output

The script saves a CSV file ([comments_VIDEO-ID.csv](./comments_ERCMXc8x7mc.csv)) with the raw data...
---

## 🧠 How It Works: The Sentiment Logic

The core of this project uses the **VADER (Valence Aware Dictionary and sEntiment Reasoner)** model. Unlike standard classifiers, VADER is specifically attuned to social media nuances.

---

## 📈 Analysis Output & Insights

| 📄 Data Generation | 🧠 Sentiment Logic |
| :--- | :--- |
| **Raw Data:** The script exports a comprehensive `comments_VIDEO-ID.csv` file containing timestamps, raw text, and individual sentiment scores. | **VADER Model:** This project utilizes the *Valence Aware Dictionary and sEntiment Reasoner* to decode social media nuances like emojis and slang. |
| **Visuals:** It automatically renders a high-resolution dashboard (`dashboard.png`) and a topic-based word cloud. | **Thresholds:** Comments are classified based on a compound score where: <br> • **Pos:** $\geq 0.05$ <br> • **Neu:** $(-0.05, 0.05)$ <br> • **Neg:** $\leq -0.05$ |

### 🔍 Analysis Pipeline
1. **Preprocessing:** The script cleans raw YouTube comments by removing extra whitespace and handling character encoding.
2. **Polarity Scoring:** VADER assigns scores based on a specialized sentiment lexicon.
3. **Contextual Scaling:** The engine accounts for intensity (e.g., "EXCITED"), negations ("not happy"), and contrastive conjunctions ("but").

---
### 📐 The Compound Score
The tool calculates a **Compound Score** for every comment, normalized between `-1` (Most Negative) and `+1` (Most Positive):

$$Compound \ Score \geq 0.05 \rightarrow \text{Positive}$$
$$-0.05 < Compound \ Score < 0.05 \rightarrow \text{Neutral}$$
$$Compound \ Score \leq -0.05 \rightarrow \text{Negative}$$

---
## 📸 Screenshots

### Sentiment Dashboard
![Dashboard](example_dashboard.png)

### Word Cloud
![Word Cloud](example_wordcloud.png)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
