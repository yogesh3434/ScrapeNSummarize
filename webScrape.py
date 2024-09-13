import requests
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def summarize_content(content):
    """Uses OpenAI to summarize the provided content."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please summarize the following content:\n\n{content}"}
            ]
        )
        summary = response.choices[0].message['content'].strip()
        return summary
    except openai.OpenAIError as e:
        print(f"OpenAI API request failed: {e}")
        return None

def main():

    user_input = input("Enter the URL to be used as a query parameter: ")

    # API URL for Web Scraper
    target_url = 'https://taras-scrape2md.web.val.run/'


    params = {'url': user_input}


    try:
        response = requests.get(target_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        print(f"Failed to retrieve data: {e}")
        return

    # Check if the request was successful
    if response.status_code == 200:
        print("Response received successfully:")
        content = response.text

        # Summarize the content
        summary = summarize_content(content)
        if summary:
            print("\nSummary:")
            print(summary)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
