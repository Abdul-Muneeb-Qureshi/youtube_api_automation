# YouTube Playlist Video Fetcher

This project retrieves videos from specified YouTube playlists, filters them by duration, and organizes them into folders based on their upload dates. Utilizing the YouTube Data API to gather information, this tool categorizes and stores video data efficiently.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [Setting up YouTube Data API](#setting-up-youtube-data-api)
- [Code Explanation](#code-explanation)
- [Directory Structure](#directory-structure)
- [Instructions for Filtering and Processing YouTube Playlist Videos](#instructions-for-filtering-and-processing-youTube-playlist-videos)


---


## Getting Started

1. **Clone the Repository**  
   Clone the project to your local machine and navigate into the project directory:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up Virtual Environment**  
   Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate     # On macOS/Linux
   .\env\Scripts\activate      # On Windows
   ```

3. **Install Dependencies**  
   Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Requirements

Dependencies for this project are listed in `requirements.txt`. Some key libraries include:

- **certifi**: Ensures SSL certificates for secure HTTP connections.
- **charset-normalizer**: Handles character encoding issues.
- **colorama**: Adds colored text output to the terminal.
- **idna**: Supports Unicode in URLs.
- **isodate**: Parses and formats ISO 8601 date and duration strings.
- **requests**: Simplifies API interactions.
- **tqdm**: Adds progress bars to loops.
- **urllib3**: Manages HTTP connections for `requests`.

Install these dependencies by running:
```bash
pip install -r requirements.txt
```

## How to Run

1. **Activate the Virtual Environment**  
   ```bash
   source env/bin/activate     # On macOS/Linux
   .\env\Scripts\activate      # On Windows
   ```

2. **Add Your API Key**  
   Update the `API_KEY` variable in `main.py` with your YouTube Data API key.

3. **Run the Application**  
   Execute the main script:
   ```bash
   python main.py
   ```

The application will process playlists listed in `src.json`, organize videos by upload date, and save them in `result/` folders.

---

## Setting up YouTube Data API

To set up the YouTube Data API in Google Cloud Console:

1. **Sign In**  
   Go to the [Google Cloud Console](https://console.cloud.google.com/) and log in.

2. **Create a New Project**  
   - Click the **Project** dropdown at the top-left and select **New Project**.
   - Name your project (e.g., "YouTube Data API Project") and click **Create**.

3. **Enable the YouTube Data API**  
   - Navigate to **API & Services** > **Library**.
   - Search for **YouTube Data API v3**, select it, and click **Enable**.

4. **Generate API Credentials**  
   - Go to **API & Services** > **Credentials**.
   - Click **Create Credentials** > **API Key** for simple access.
   - Copy your API Key.

5. **Optional: Quotas and Monitoring**  
   - Monitor API usage in **API & Services** > **Dashboard**.
   - Set limits under **Quotas** as needed.

Refer to the [YouTube Data API documentation](https://developers.google.com/youtube/v3) for usage details.

---

## Code Explanation

### Code Structure

- **`extract_month_year(publish_date)`**  
  Converts the publication date to a month and year format.

- **`get_video_duration(video_id)`**  
  Retrieves the video duration from the YouTube API using the video ID, with retry logic in case of errors.

- **`extract_video_id(url)`**  
  Extracts the video ID from a YouTube URL using regular expressions.

- **`filter_videos_by_duration(videos)`**  
  Filters videos with durations between 1500 and 3000 seconds.

- **`append_link_to_file(file_name, link)`**  
  Saves a video link in a text file, creating the file if it doesn’t exist and avoiding duplicates.

- **`store_videos(videos, channel_name, playlist_name)`**  
  Organizes videos into folders by month and year, saving URLs in formatted text files.

- **`checkPlaylistOrder(playlist_id)`**  
  Checks the chronological order of playlist videos by comparing the publication dates of the first and ninth videos.

- **`load_data()`**  
  Loads channel and playlist data from `src.json`.

- **`fetch_all_playlist_items(playlist_id, order)`**  
  Retrieves videos from a playlist based on its ID and order.

- **`processing(data)`**  
  Main function that processes channels and playlists, checks playlist order, fetches videos, filters by duration, and organizes them into folders.

- **`main()`**  
  Loads data and runs all core functionalities of the script.

---


## Instructions for Filtering and Processing YouTube Playlist Videos

1. **Determine Playlist Order:**  
   - The function `checkPlaylistOrder(playlist_id)` checks whether videos in a playlist are ordered as `"increase"` (oldest to newest) or `"decrease"` (newest to oldest).  
   - This is based on the difference between the first and ninth video's publish dates:  
     - **Positive difference → "increase"** (chronological order).  
     - **Negative difference → "decrease"** (reverse order).  

2. **Process Only "Increase" Order Playlists:**  
   - If the playlist order is **not** `"increase"`, it is skipped using `continue`.  
   - Only playlists with `"increase"` order proceed to further processing.  

3. **Fetch and Filter Videos:**  
   - Retrieve all videos from the playlist.  
   - Apply a date filter using `filter_videos_by_date(all_videos, '1 April 2024')`.  
   - Apply a duration filter using `filter_videos_by_duration(all_videos)`.  

4. **Store Processed Videos:**  
   - The final list of videos is stored along with channel and playlist details.


## Directory Structure

After running the script, videos are organized by year and month in the following structure:
```
result/
├── 2023/
│   ├── October/
│   │   ├── channelName_October_2023_playlistName.txt
│   │   └── ...
│   └── ...
└── 2024/
    └── ...
```

