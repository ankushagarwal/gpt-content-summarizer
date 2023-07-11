#!/bin/bash

#set -x

# Check if a URL was provided
if [ -z "$1" ]; then
    echo "Error: No YouTube video URL was provided."
    echo "Usage: $0 <YouTube_URL>"
    exit 1
fi

title=$(yt-dlp --get-title $1)

# Remove invalid characters from the title
safe_title=$(echo $title | tr -d '\/:*?"<>|')

echo "title = ${safe_title}"

# Define the output file
outfile="tmp/subs/${safe_title}"

# Call yt-dlp with the provided URL
yt-dlp -o "${outfile}" --write-auto-sub --sub-lang en --skip-download $1 --convert-subs=srt

actual_outfile="${outfile}.en.srt"
outfile_fixed="${outfile}.fixed.en.srt"

python srt_fix/srt_fixer_cli.py -o "${outfile_fixed}" "${actual_outfile}"

rm "${outfile}.srt.en.srt"
rm "${actual_outfile}"

python text_file_summarizer.py \
  --input_file "${outfile_fixed}" \
  --output_file "outputs/${title}.summary.txt" \
  --content_type "podcast"