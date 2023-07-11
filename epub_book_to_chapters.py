import os
import argparse
from epub2txt import epub2txt
import json

def get_title_from_file_path(filepath):
  base = os.path.basename(filepath)
  # Split the extension
  return os.path.splitext(base)[0]

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_epub_file', type=str)
  args = parser.parse_args()

  ch_list = epub2txt(args.input_epub_file, outputlist=True)

  title = get_title_from_file_path(args.input_epub_file)

  output_file = f'outputs/{title}.json'

  # convert ch_list to json and print it
  with open(output_file, 'w') as f:
    json.dump(ch_list, f, indent=4)

  print(f"Wrote to {output_file}. Please review and remove non-chapters.")

if __name__ == "__main__":
  main()
