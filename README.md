# YouTube Playlist Video Fetcher

This project retrieves videos from specified YouTube playlists, filters them by duration, and organizes them into folders based on the upload date. It utilizes the YouTube Data API to gather data, making it simple to categorize and store video information.

## Table of Contents
- [Getting Started](#getting-started)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [Code Explanation](#code-explanation)

---

## Getting Started

1. Clone the repository to your local machine.
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate     # On macOS/Linux
   .\env\Scripts\activate      # On Windows
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Requirements

Dependencies for this project are listed in `requirements.txt`. Below are the main libraries required, along with their uses:

- **certifi**: Provides SSL certificates for secure HTTP connections.
- **charset-normalizer**: Handles various character encodings in text processing.
- **colorama**: Enables colored terminal text output.
- **idna**: Supports Unicode domain names in URLs.
- **isodate**: Parses and formats ISO 8601 date and duration strings.
- **requests**: Simplifies HTTP requests to interact with APIs.
- **six**: Ensures compatibility between Python 2 and 3.
- **tqdm**: Adds progress bars to loops.
- **urllib3**: Manages HTTP connections for `requests`.

Install these dependencies using:
```bash
pip install -r requirements.txt
```

## How to Run

1. **Activate the virtual environment**:
   ```bash
   source env/bin/activate     # On macOS/Linux
   .\env\Scripts\activate      # On Windows
   ```

2. **Enter your API key**: 
   Update the `API_KEY` variable in `main.py` with your YouTube Data API key.

3. **Run the application**:
   ```bash
   python main.py
   ```

The script will process the playlists specified in `src.json`, organize videos by date, and store them in `result/` folders.

## Code Explanation

### Code Structure

- **`extract_month_year(publish_date)`**: Converts a video’s publication date to a readable month and year format.
  
- **`get_video_duration(video_id)`**: Retrieves video duration in seconds from the YouTube API using the video’s ID, with retries if any request fails.
  
- **`extract_video_id(url)`**: Extracts the unique video ID from a YouTube URL using a regular expression.
  
- **`filter_videos_by_duration(videos)`**: Filters videos with durations between 1500 and 3000 seconds.

- **`append_link_to_file(file_name, link)`**: Saves a video link in a text file, creating the file if it doesn’t exist and avoiding duplicate entries.
  
- **`store_videos(videos, channel_name, playlist_name)`**: Organizes videos into folders based on upload month and year and saves URLs in formatted files.

- **`checkPlaylistOrder(playlist_id)`**: Checks the chronological order of videos in a playlist, determining if they’re in increasing or decreasing order by comparing the first and ninth video dates.
  
- **`load_data()`**: Loads channel and playlist information from `src.json`, which includes playlists to be processed.

- **`fetch_all_playlist_items(playlist_id, order)`**: Retrieves videos from a playlist based on its ID and the playlist order, stopping once certain conditions are met.

- **`processing(data)`**: Main function that iterates over channels and playlists, checks playlist order, fetches videos, filters them by duration, and stores them in the appropriate directory.

- **`main()`**: Loads the data, processes the playlists, and runs all core functionalities of the script.

---

### Example Directory Structure
After running the script, files are organized in the following structure:
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

This structure categorizes videos by year and month, making it easier to access video links organized by upload date.


