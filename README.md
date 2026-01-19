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
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
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
     ```    ```

5.  **Run the analysis:**
    * Open `mood_ring.py` and paste the YouTube Video URL you want to analyze.
    * Run the script:
        ```bash
        python mood_ring.py
        ```
     * **Tip:** Don't have an API key? You can check the `comments_ERCMXc8x7mc.csv` file included in this repo to see what the raw data looks like!

## 📈 Output

The script saves a CSV file (`comments_VIDEO-ID.csv`) with the raw data and opens an interactive dashboard window.

## 📸 Screenshots

### Sentiment Dashboard
![Dashboard](example_dashboard.png)

### Word Cloud
![Word Cloud](example_wordcloud.png)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
