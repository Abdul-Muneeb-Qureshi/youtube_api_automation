import requests
import json
import os
from datetime import datetime
import re
import isodate
from tqdm import tqdm
import time

API_KEY = ''
url = 'https://www.googleapis.com/youtube/v3/playlistItems'


def filter_videos_by_date(videos, date_str):
    """
    Filters videos that were published after the given date.
    
    :param videos: List of video dictionaries containing 'publish_date' and 'url'.
    :param date_str: Date string in the format 'DD Month YYYY' (e.g., '2 June 2024').
    :return: List of video URLs published after the given date.
    """
    
    target_date = datetime.strptime(date_str, "%d %B %Y")
    
    filtered_videos = [video for video in videos if datetime.strptime(video['publish_date'], "%Y-%m-%dT%H:%M:%SZ") > target_date]
    
    return filtered_videos

def extract_month_year(publish_date):
    date_object = datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%SZ")
    month = date_object.strftime("%B")
    year = date_object.year
    return month, year

def get_video_duration(video_id):
    video_id = "icI1z52tKwM"
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={API_KEY}"
    
    for attempt in range(5):  # Retry up to 5 times
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            # print(data)
            

            # Check for errors in the response
            if 'error' in data:
                print(f"Error fetching duration for {video_id}: {data['error']['message']}")
                return None
            
            if 'items' in data and len(data['items']) > 0:
                try:
                    duration_iso = data['items'][0]['contentDetails']['duration']
                    return isodate.parse_duration(duration_iso).total_seconds()
                except:
                    print(video_id , data)
            else:
                print(video_id , "sdgh")

                return None
        except requests.exceptions.RequestException as e:
            print(video_id)
            print(f"Attempt {attempt + 1}: {e}")
            time.sleep(2)  # Wait before retrying

    return None  # Return None if all attempts fail

def extract_video_id(url):
    regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def filter_videos_by_duration(videos):
    updated_videos = []
    
    for video in tqdm(videos, desc="Filtering Videos by Duration"):
        video_id = extract_video_id(video['url'])
        if video_id:
            duration = get_video_duration(video_id)
            if duration and 1500 <= duration <= 2400:
                updated_videos.append(video)
        else:
            updated_videos.append(video)
    
    return updated_videos

def append_link_to_file(file_name, link):
    try:
        with open(file_name, 'r') as file:
            links = file.readlines()
        if link + '\n' in links:
            return
    except FileNotFoundError:
        print(f"{file_name} not found. Creating new file.")

    with open(file_name, 'a') as file:
        file.write(link + '\n')
        print("Link is appending:", link)

def store_videos(videos, channel_name, playlist_name):
    for video in videos:
        month, year = extract_month_year(video['publish_date'])
        os.makedirs(f"result1/{year}", exist_ok=True)
        os.makedirs(f"result1/{year}/{month}", exist_ok=True)
        file_name = f"result1/{year}/{month}/{channel_name}_{month}_{year}_{playlist_name}.txt"
        append_link_to_file(file_name, video['url'])

def checkPlaylistOrder(playlist_id):
    params = {
        'part': 'snippet',
        'playlistId': playlist_id,
        'maxResults': 20,
        'key': API_KEY,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None

    playlist_data = response.json()
    dates = []

    for item in playlist_data['items']:
        dates.append(item['snippet']['publishedAt'])
    
    publish_date = datetime.strptime(dates[0], "%Y-%m-%dT%H:%M:%SZ")
    comparison_date = datetime.strptime(dates[8], "%Y-%m-%dT%H:%M:%SZ")
    difference = publish_date - comparison_date

    if difference.total_seconds() > 0:
        print("Increase")
        return "increase"
    elif difference.total_seconds() < 0:
        print("Decrease")
        return "decrease"
    else:
        print("No difference in time")
        return None

def load_data():
    with open('src.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def fetch_all_playlist_items(playlist_id, order):

    videos = []
    next_page_token = None

    while True:
        params = {
            'part': 'snippet',
            'playlistId': playlist_id,
            'maxResults': 50,
            'key': API_KEY,
            'pageToken': next_page_token
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        playlist_data = response.json()

        for item in playlist_data['items']:
            video_data = {
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}",
                'publish_date': item['snippet']['publishedAt'],
                'channel_name': item['snippet']['channelTitle']
            }
            videos.append(video_data)

        next_page_token = playlist_data.get('nextPageToken')


        
        # if order == "increase":
        #     break
        # if order == "decrease":
        #     print("decrease")
        #     if(len(videos)>=80):
        #         videos = []
        
        if not next_page_token:
            break

       
    
    return videos

def processing(data):
    for channel in tqdm(data, desc="Processing Channels"):
        channel_name = channel['channel']
        
       
      
        for playlist in tqdm(channel['playlists'], desc=f"Processing Playlists for {channel_name}", leave=False):
           
            print(f"  Playlist Id: {playlist['playlist_id']}")
            print(f"  Playlist Name: {playlist['playlist_name']}")

            playlist_id = playlist['playlist_id']
            playlist_name = playlist['playlist_name']

            order = checkPlaylistOrder(playlist_id)

            if order != 'increase':
                print(i)
                i=i+1
                continue
            
            all_videos = fetch_all_playlist_items(playlist_id, order)

            print(f"Total videos retrieved without any filter: {len(all_videos)}")

            all_videos = filter_videos_by_date(all_videos , '1 April 2024')

            print(f"Total videos retrieved with date filter: {len(all_videos)}")

            all_videos = filter_videos_by_duration(all_videos)

            print(f"Total videos retrieved: {len(all_videos)}")
            store_videos(all_videos, channel_name, playlist_name)
        

def main():
    data = load_data()

    # videos = fetch_all_playlist_items("PLe0pMWFRlLIzx_Obf4RrFwIU_VofrkWpU" , "decrease")
    # print(len(videos))
    # print(videos[0])
    # print(get_video_duration("kFFya5_-x3I"))

    processing(data)

if __name__ == "__main__":
    main()