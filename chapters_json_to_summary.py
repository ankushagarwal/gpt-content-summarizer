import os
import argparse
import json
import subprocess

def get_title_from_file_path(filepath):
  base = os.path.basename(filepath)
  # Split the extension
  return os.path.splitext(base)[0]

def truncate_first_line(s, max_length=150):
    # Split the string into lines
    lines = s.splitlines()

    # Get the first line
    first_line = lines[0] if lines else ""

    # Truncate the first line if necessary
    if len(first_line) > max_length:
        first_line = first_line[:max_length]

    return first_line

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_json_file', type=str)
  parser.add_argument('--output_folder_name', default='', type=str)
  args = parser.parse_args()

  output_prefix = "outputs"
  if not args.output_folder_name == '':
     output_prefix = f"outputs/{args.output_folder_name}"

  if not os.path.exists(output_prefix):
      os.makedirs(output_prefix)

  with open(args.input_json_file, 'r') as f:
      book_data = json.load(f)

  title = get_title_from_file_path(args.input_json_file)

  for chapter in book_data:
    chapter_name = truncate_first_line(chapter)
    print(f"Summarizing Chapter Name: {chapter_name}")
    chapter_output_file = f"tmp/{chapter_name}.txt"
    chapter_summary_file = f"{output_prefix}/{chapter_name} Summary.txt"

    with open(chapter_output_file, 'w') as f:
      f.write(chapter)

    subprocess.run(["python", "text_file_summarizer.py", "--input_file", chapter_output_file, "--output_file", chapter_summary_file, "--content_type", "book_chapter"])




if __name__ == "__main__":
  main()
