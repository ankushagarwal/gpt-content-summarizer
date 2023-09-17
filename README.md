# GPT Content Summarizer

This project can take youtube videos or youtube playlists, and convert them into notes and summaries using GPT


## Requirements

* yt-dlp, ffmpeg (brew install yt-dlp ffmpeg)
* python 3
* pip install openai epub2txt
* OPENAI_API_KEY as env variable
  * export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxx"

## Summarize youtube videos

You can use the `summarize_yt_video.sh`. This uses yt-dlp to download the subtitles
It cleans up the subtitles using a package called srt_fix. A copy of that package is here. It then calls text_file_summarizer.py to summarize the output

Example Invocation

```
./summarize_yt_video.sh 'https://www.youtube.com/watch?v=zRtdikFQ-Pg'

...
Writing to outputs/Dr. Peter Attia — His Rules for Alcohol Consumption (How Much, When, and More).summary.txt
...
```

## Summarize youtube playlists

You can use the `summarize_yt_playlist.sh` script. This uses `yt-dlp` and the `summarize_yt_video.sh` script. It extracts all videos from
the youtube playlist and calls `summarize_yt_video.sh` one by one




Example Invocation

```
./summarize_yt_playlist.sh 'https://www.youtube.com/playlist?list=PL2D5A39CA456F09D7'

...
Summarizing 1/22 https://www.youtube.com/watch?v=M-129JLTjkQ...
title = The Basics of Non Violent Communication 1.1
...
```

## Summarize books

You need to download the epub format of the book. You can use https://annas-archive.org/ to download it. See https://hn.algolia.com/?q=annas-archive.org or https://www.reddit.com/r/Annas_Archive/ for alternate sources


### Step 1 Extract Chapters from the ebook

We will use the `epub_book_to_chapters.py` script. This will create a json file.

The json file is a list of "chapters" in the epub ebook. You need to manually remove the first few and the last few entries from the
json file manually. This leaves you with a json file which only contains the actual chapters of the book.

After cleaning up the book, save the json file.

Example invocation

```
python epub_book_to_chapters.py --input_epub_file Outlive.epub

<Manual Cleanup>
```

### Step 2 Summarize the book using the json file

We will use the `chapters_json_to_summary.py` file to summarize the book. This reads the
json file and goes over chapter by chapter and writes the summary to a single file per chapter. Internally, it uses text_file_summarizer.py.

Example invocation

```
python chapters_json_to_summary.py \
  --output_folder_name outlive \
  --input_json_file outputs/Outlive.json
```
