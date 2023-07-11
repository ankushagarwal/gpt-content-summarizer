import openai
import os
import sys
import argparse

# check if openai_key is set in environment variable
if os.environ.get("OPENAI_API_KEY"):
  openai.api_key = os.environ.get("OPENAI_API_KEY")
else:
  # exit the program
  print("Please set the OPENAI_API_KEY environment variable.")
  exit()

total_tokens_used = 0

def summarize(podcast_title, text):
    global total_tokens_used
    system_content = f"""
You are a brilliant podcast summarizer. You are given the following section from a podcast titled "{podcast_title}".
Can you provide a comprehensive summary of the given text?
The summary should cover all the key points and mainideas presented in the original text, while also condensing the information into a concise and easy-to-understand format.
Please ensure that the summary includes relevant details and examples that support the main ideas, while avoiding any unnecessary information or repetition.
The length of the summary should be appropriate for the length and complexity of the original text, providing a clear and accurate overview without omitting any important information.
The summary should be in a markdown bullet(*) list format
"""

    user_content = f"""
    Here is the section within triple angle brackets : <<< {text} >>>
    Detailed Summary:
    """

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
    )
    total_tokens_used += response['usage']['total_tokens']
    print(f"Response:\n{response['choices'][0]['message']['content']}")


def chunk_text(text, chunk_size_words, overlap_bw_chunks):
  """
  Splits a given text into chunks of a specified size, with a specified overlap between the chunks.

  Parameters:
    - text (str): The text to be chunked.
    - chunk_size_words (int): The number of words in each chunk.
    - overlap_bw_chunks (int): The number of words overlapping between each chunk.
  """
  words = text.split()
  m = overlap_bw_chunks
  n = chunk_size_words
  chunked_words = [words[i:i+n] for i in range(0, len(words), n-m)]
  return [" ".join(chunked_words[i]) for i in range(len(chunked_words))]

def summarize_content(content_title, text, max_words):

  chunks = chunk_text(text, max_words, max_words // 10)

  print(f"Split the text into {len(chunks)} chunks of {max_words} words.")

  # go over the chunks and print them
  print("AI Summary and Ideas List\n")
  for i, chunk in enumerate(chunks):
    print(f"Part {i+1}/{len(chunks)}:\n")
    print("Summary (Key-ideas in this section): \n")
    print(summarize(content_title, chunk))
    # print("\nDetailed Notes from this section: \n")
    # print(idea_list(content_title, chunk))
    print("\n--------\n")

# write the main function

def get_title_from_file_path(filepath):
  base = os.path.basename(filepath)
  # Split the extension
  return os.path.splitext(base)[0]

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_file', type=str)
  parser.add_argument('--context_type', type=str, choices=['book_chapter', 'general_text', 'blog_post', 'podcast'])
  args = parser.parse_args()


  # check if the file exists and is valid
  if not os.path.isfile(args.input_file):
    print(f"File '{args.input_file}' does not exist or is not accessible.")
    return

  output_filename = f"{args.input_file}.summary.txt"
  # read the file into a string
  with open(args.input_file, 'r') as f:
    text = f.read()

  summarize_content(get_title_from_file_path(args.input_file), text, 1500)
  print(f"Estimated cost = {round(total_tokens_used * 0.0015 * 0.001, 3)} USD")



if __name__ == "__main__":
  main()
