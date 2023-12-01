import requests
import difflib
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from textblob import Word


# Function to fetch webpage content
async def fetch_webpage(fetch_url):
    # Sends an HTTP GET request to the specified URL and awaits the response.
    response = requests.get(fetch_url)

    # Returns the text content of the response obtained from the requested URL.
    return response.text


# Function to parse HTML content
async def soup_webpage(content):
    # Creates a BeautifulSoup object, which is a Python library for pulling data out of HTML and XML files.
    soup = BeautifulSoup(content, 'html.parser')

    # Returns the BeautifulSoup object representing the parsed HTML content.
    return soup


# Function to compare new content with old one
async def is_content_changed(old_content, new_content, threshold):
    # Calculates the difference between two sequences, line by line, using the ndiff function from the difflib module.
    diff = difflib.ndiff(old_content, new_content)

    # Counts the number of lines with differences in the ndiff result,
    # where the first character indicates the type of difference.
    diff_count = sum(1 for _ in diff if _[0] != ' ')

    # Calculates the percentage of change by dividing the count of differing lines
    # by the maximum length of the two content sequences.
    change_percentage = diff_count / max(len(old_content), len(new_content))

    # Returns True if the calculated change percentage is greater than
    # the specified threshold, indicating a significant change.
    return change_percentage > threshold


# Parse the HTML code of the page and return the URL of the new page
async def find_page_urls(page_url, soup):
    # Find all links on the page
    links = soup.find_all('a', href=True)

    # Creates empty list of filtered links
    filtered_links = []

    # Creates list of new links on the website
    for link in links:
        # Convert relative URLs to absolute ones
        link_url = urljoin(page_url, link['href'])

        # Extract the domain from base_url
        base_domain = urlparse(page_url).netloc

        # Extract the domain from the link
        link_domain = urlparse(link_url).netloc

        # Checks if the link domain matches the base_url domain
        if link_domain == base_domain:
            # add to filtered_links list
            filtered_links.append(link_url)

    # Remove identical links
    uniq_filtered_links = list(set(filtered_links))

    # return the list of uniq links
    return uniq_filtered_links


# Spell checks the word
async def check_word_spelling(word, message, spell_check_accuracy_float):
    # The word is converted into a Word object.
    word = Word(word)

    # The `spellcheck` method is called on the Word object to check the spelling of the word.
    result = word.spellcheck()

    # An empty list `result_word_check` is initialized to store the results of the spelling check.
    result_word_check = []

    # The condition checks if the original word is not equal to the first suggestion and
    # the confidence of the suggestion is below the specified accuracy.
    if word != result[0][0] and result[0][1] < spell_check_accuracy_float:
        # If the condition is met, messages about the incorrect spelling and
        # the correct suggestion with confidence are appended to `result_word_check`.
        result_word_check.append(f'Spelling of "{word}" is not correct!')
        result_word_check.append(f'Correct spelling of "{word}": "{result[0][0]}" (with {result[0][1]} confidence).')

        # A loop iterates over the elements of `result_word_check` and prints them in pairs.
        for i in range(0, len(result_word_check), 2):
            element1 = result_word_check[i]
            element2 = result_word_check[i + 1] if i + 1 < len(result_word_check) else None

            # Each pair of elements is printed in the format "<b>{element1}\n{element2}</b>".
            print(f"<b>{element1}\n{element2}</b>")

            # The formatted pair of elements is sent as a message using the `await` statement.
            await message.answer(f"<b>{element1}\n{element2}</b>")

        # returns the spell check result list
        return result_word_check


# Spell checks the text
async def check_sentence_spelling(sentence, message, spell_check_accuracy_float):
    # The text is split into a list of words.
    words = sentence.split()

    # All words are converted to lowercase to ensure uniformity in spelling comparison.
    words = [word.lower() for word in words]

    # Non-alphanumeric characters are removed from each word in the list.
    words = [re.sub(r'[^A-Za-z0-9]+', '', word) for word in words]

    # Duplicate words are removed by converting the list to a set and then back to a list.
    words = list(set(words))

    print(words)

    # An empty list `result_sentence_check` is initialized to store the results of word-level spelling checks.
    result_sentence_check = []

    # A loop iterates over each unique word in the text.
    for word in words:
        # The `check_word_spelling` function is called asynchronously to check the spelling of each word.
        # The results of the word-level spelling check are stored in `word_check_result`.
        word_check_result = await check_word_spelling(word, message, spell_check_accuracy_float)

        # If there are spelling errors for the word, the results are added to `result_sentence_check`.
        if word_check_result is not None:
            result_sentence_check.extend(word_check_result)

    # The list of word-level spelling check results is returned.
    return result_sentence_check
# ___________


# Gets initial data from the webpage
async def get_initial_data(url):
    # Fetch initial content
    initial_content = await fetch_webpage(url)

    # Find initial webpage soup
    initial_soup = await soup_webpage(initial_content)

    # Gets list of page URLs on the website
    initial_urls = await find_page_urls(url, initial_soup)

    # Initial content and list of page URLs on the website is returned.
    return initial_content, initial_urls


# Fetch new content
async def get_new_content(url):
    # Fetch new content
    new_content = await fetch_webpage(url)

    # Returns new content
    return new_content


# Finds urls of new posts
async def find_urls_difference(url, initial_urls, new_content):
    # An empty list `urls_difference` is initialized to store the urls of new posts.
    urls_difference = []

    # Find new webpage soup
    new_soup = await soup_webpage(new_content)

    # Gets new list of page URLs on the website
    new_urls = await find_page_urls(url, new_soup)

    # Checks if urls changed
    if new_urls != initial_urls:

        # Creates list of all new posts urls
        urls_difference_any_language = [element for element in new_urls if element not in initial_urls]
        # print("New elements:", urls_difference_any_language)

        # Creates list of new english posts urls
        urls_difference = [url_difference_any_language for url_difference_any_language in urls_difference_any_language
                           if not url_difference_any_language.startswith(f"{url}/ru")
                           and not url_difference_any_language.startswith(f"{url}/uz")]

        # print("English urls")
        # print(urls_difference)

    # List of new posts and updated list of webpage urls is returned.
    return urls_difference, new_urls


# Spell check new post
async def spell_check_new_post(url_difference, message, spell_check_accuracy_float):
    print(url_difference)

    # Fetch initial content
    new_url_content = await fetch_webpage(url_difference)

    # Find initial webpage soup
    new_url_soup = await soup_webpage(new_url_content)

    # Gets all text of the webpage
    # page_text = new_url_soup.get_text()

    # Gets only visible text (without HTML-tags and attributes)
    visible_text = ' '.join(new_url_soup.stripped_strings)

    # Prints visible text
    print(visible_text)

    # Gets the list of word-level spelling check results.
    sentence_check_result = await check_sentence_spelling(visible_text, message, spell_check_accuracy_float)

    # print("sentence_check_result")
    # print(sentence_check_result)

    # The list of word-level spelling check new post results is returned.
    return sentence_check_result
