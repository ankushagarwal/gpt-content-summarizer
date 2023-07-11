#!/bin/bash

#!/bin/bash

# Check if a URL was provided
if [ -z "$1" ]; then
    echo "Error: No YouTube video URL was provided."
    echo "Usage: $0 <YouTube_URL>"
    exit 1
fi

# Check if OPENAI_KEY is set
if [ -z "$OPENAI_KEY" ]; then
    echo "Error: OPENAI_KEY is not set."
    exit 1
fi

# Call yt-dlp with the provided URL
yt-dlp -o 'subs/%(title)s.%(ext)s' --write-auto-sub --sub-lang en --skip-download $1 --convert-subs=srt

python srt_fix/srt_fixer_cli.py -idir 'subs' -odir 'subs-fixed'
