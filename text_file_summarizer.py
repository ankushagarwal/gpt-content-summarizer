import os
from openai import OpenAI
import argparse
import time

total_tokens_used = 0

# check if openai_key is set in environment variable
if not os.environ.get("OPENAI_API_KEY"):
    # exit the program
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def summarize(content_title, text, content_type):
    global total_tokens_used
    system_content = f"""
You are a brilliant content summarizer. You are given the following section from a content titled "{content_title}". The content type is {content_type}.
Can you provide a comprehensive summary of the given content?
The summary should cover all the key points and main ideas presented in the original text, while also condensing the information into a concise and easy-to-understand format.
Please ensure that the summary includes relevant details and examples that support the main ideas, while avoiding any unnecessary information or repetition.
The length of the summary should be appropriate for the length and complexity of the original text, providing a clear and accurate overview without omitting any important information.
The summary should be in a markdown list format using hyphens (-) as list delimiters.
"""

    user_content = f"""
    Here is the section within triple angle brackets : <<< {text} >>>
    Detailed Summary:
    """
    attempts = 5
    for attempt in range(attempts):
        try:
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content}
                ])
            break
        except Exception as e:
            print(f"OpenAI ChatCompletion failed: {e}. Trying again.")
            if attempt < attempts - 1:  # i.e., if it's not the last attempt
                time.sleep(5)  # Wait for 5 seconds before next attempt
                continue
            else:
                raise  # Re-raise the last exception if all attempts fail

    total_tokens_used += response.usage.total_tokens
    return response.choices[0].message.content


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


def summarize_content(content_title, text, max_words, content_type, output_filename):

    chunks = chunk_text(text, max_words, max_words // 10)

    print(f"Split the text into {len(chunks)} chunks of {max_words} words.")

    # open the output file_name and write the summary to it
    print(f"Writing to {output_filename}")
    for i, chunk in enumerate(chunks):
        with open(output_filename, 'a') as f:
            print(f"Processing chunk {i+1}/{len(chunks)}")
            f.write(f"Part {i+1}/{len(chunks)}:\n\n")
            f.write(f"{summarize(content_title, chunk, content_type)}\n\n")


def get_title_from_file_path(filepath):
    base = os.path.basename(filepath)
    # Split the extension
    return os.path.splitext(base)[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str)
    parser.add_argument('--output_file', type=str)
    parser.add_argument('--content_type', type=str,
                        choices=['book_chapter', 'general_text', 'blog_post', 'podcast'])
    args = parser.parse_args()

    # check if the file exists and is valid
    if not os.path.isfile(args.input_file):
        print(f"File '{args.input_file}' does not exist or is not accessible.")
        return

    # read the file into a string
    with open(args.input_file, 'r') as f:
        text = f.read()

    summarize_content(get_title_from_file_path(args.input_file),
                      text, 2000, args.content_type, args.output_file)
    COST_PER_TOKEN = 0.01 * 0.001  # 0.01 USD per 1000 tokens
    print(
        f"Estimated cost = {round(total_tokens_used * COST_PER_TOKEN, 3)} USD")


if __name__ == "__main__":
    main()
