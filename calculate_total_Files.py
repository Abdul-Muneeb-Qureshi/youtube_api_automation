import os
import re

main_directory = 'result/2024/September'

youtube_link_pattern = re.compile(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/[^\s]+')

total_links = 0

for root, dirs, files in os.walk(main_directory):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
                # Find all YouTube links in the content
                links = youtube_link_pattern.findall(content)
                total_links += len(links)

print(f'Total YouTube links found: {total_links}')
