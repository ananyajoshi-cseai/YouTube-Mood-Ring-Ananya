import os
import re
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# --- Feature: WordCloud ---
try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    print("Note: 'wordcloud' library not found. Skipping that chart.")

# --- SETUP & SECURITY ---
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("CRITICAL: API Key not found. Please check your .env file.")

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

analyzer = SentimentIntensityAnalyzer()

# --- HELPER: EXTRACT ID FROM URL ---
def extract_video_id(url_or_id):
    # Regex to find the 11-character ID
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url_or_id)
    if match:
        return match.group(1)
    return url_or_id

# --- PART 2: THE FETCH ---
def get_video_comments(video_id, max_comments=1000):
    print(f"--- Fetching up to {max_comments} comments for video: {video_id} ---")
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    comments_data = []
    next_page_token = None
    
    try:
        while len(comments_data) < max_comments:
            request = youtube.commentThreads().list(
                part="snippet", videoId=video_id, maxResults=100,
                textFormat="plainText", pageToken=next_page_token, order="relevance"
            )
            response = request.execute()
            
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments_data.append({
                    'text': comment['textDisplay'],
                    'likes': comment['likeCount'],
                    'author': comment['authorDisplayName'],
                    'date': comment['publishedAt']
                })
            
            next_page_token = response.get('nextPageToken')
            print(f"Fetched {len(comments_data)} comments...")
            if not next_page_token: break 
                
    except HttpError as e:
        if e.resp.status == 403: print("Error: Comments disabled.")
        elif e.resp.status == 404: print("Error: Video not found.")
        else: print(f"API Error: {e}")
            
    return pd.DataFrame(comments_data)

# --- PART 3: THE JUDGE ---
def analyze_sentiment(df):
    if df.empty: return df
    print("--- Judging Sentiment (VADER) ---")
    
    df['compound_score'] = df['text'].apply(lambda x: analyzer.polarity_scores(str(x))['compound'])
    
    def categorize(score):
        if score >= 0.05: return 'Positive'
        elif score <= -0.05: return 'Negative'
        else: return 'Neutral'
        
    df['category'] = df['compound_score'].apply(categorize)
    return df

# --- PART 4: WORD CLOUD ---
def show_wordcloud(df):
    if not WORDCLOUD_AVAILABLE or df.empty: return
    
    print("--- Generating Word Cloud ---")
    text = " ".join(comment for comment in df.text.astype(str))
    
    # Create cloud
    wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title("Most Frequent Words")
    plt.show()

# --- PART 5: DASHBOARD ---
def visualize_dashboard(df):
    if df.empty: return

    print("--- Generating Dashboard ---")
    color_map = {'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
    
    # Create a larger canvas for 4 charts
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('YouTube Mood Ring: Time Series Edition', fontsize=20)

    # 1. Pie Chart
    ax1 = plt.subplot(2, 2, 1)
    counts = df['category'].value_counts()
    ax1.pie(counts, labels=counts.index, autopct='%1.1f%%', 
            colors=[color_map.get(key, '#333333') for key in counts.index], 
            startangle=90, explode=[0.05]*len(counts))
    ax1.set_title('Sentiment Distribution')

    # 2. Bar Chart
    ax2 = plt.subplot(2, 2, 2)
    counts.plot(kind='bar', color=[color_map.get(key, '#333333') for key in counts.index], ax=ax2)
    ax2.set_title('Comment Volume by Sentiment')
    ax2.grid(axis='y', alpha=0.3)

    # 3. Scatter Plot
    ax3 = plt.subplot(2, 2, 3)
    scatter_colors = df['category'].map(color_map)
    ax3.scatter(df['compound_score'], df['likes'], c=scatter_colors, alpha=0.6, s=50, edgecolors='white')
    ax3.set_title('Engagement vs Sentiment')
    ax3.set_xlabel('Sentiment Score')
    ax3.set_ylabel('Likes')
    ax3.axvline(0, color='grey', linestyle='--')

    # 4. Time Series Analysis
    ax4 = plt.subplot(2, 2, 4)
    df['dt'] = pd.to_datetime(df['date'])
    sentiment_over_time = df.set_index('dt').resample('M')['compound_score'].mean()
    
    sentiment_over_time.plot(ax=ax4, color='blue', marker='o', linestyle='-')
    ax4.set_title('Average Mood Over Time (Monthly)')
    ax4.set_ylabel('Avg Sentiment (-1 to +1)')
    ax4.axhline(0, color='grey', linestyle='--', linewidth=1)
    ax4.grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    
    # Replace with your video ID or Link
    VIDEO_URL = "https://www.youtube.com/watch?v=ERCMXc8x7mc" 
    
    video_id = extract_video_id(VIDEO_URL)
    
    df = get_video_comments(video_id, max_comments=1000)
    df = analyze_sentiment(df)
    
    if not df.empty:
        try:
            df.to_csv(f"comments_{video_id}.csv", index=False)
            print(f"Saved CSV.")
        except: pass

        # 1. Show Word Cloud First
        show_wordcloud(df)
        
        # 2. Then Show Dashboard
        visualize_dashboard(df)

