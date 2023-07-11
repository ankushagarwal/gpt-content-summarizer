#!/bin/bash

#set -x

# Check if a URL was provided
if [ -z "$1" ]; then
    echo "Error: No YouTube playlist URL was provided."
    echo "Usage: $0 <YouTube_playlist_URL>"
    exit 1
fi

video_ids=$(yt-dlp --flat-playlist --get-id $1)

video_urls=$(echo "$video_ids" | sed 's_^_https://www.youtube.com/watch?v=_')

# Convert the video_urls to an array
IFS=$'\n' read -d '' -r -a video_array <<< "$video_urls"

# Get the total number of URLs
total=${#video_array[@]}

# Iterate over the URLs
for i in "${!video_array[@]}"; do
  url="${video_array[i]}"
  echo "Summarizing $(($i+1))/$total $url..."
  bash summarize_yt_video.sh "$url"
  echo "------------------------------"
  echo
done
