from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm  # Progress bar library
import time

def wait_for_manual_authentication(driver):
    """Pauses the script and waits for the user to manually complete authentication."""
    print("Authentication required. Please complete the verification in the browser.")
    input("Press Enter after completing authentication...")

def scrape_lyrics_with_titles(driver, urls):
    lyrics_collection = {}

    for url in tqdm(urls, desc="Scraping Progress"):
        driver.get(url)
        time.sleep(0.5)  # Wait for the page to load

        # Check for the presence of the authentication message
        try:
            auth_message = driver.find_element(
                By.XPATH, "//h1[contains(text(), \"Let's confirm you are human\")]"
            )
            if auth_message:
                wait_for_manual_authentication(driver)
        except Exception:
            # No authentication message, continue
            pass

        try:
            # Extract the song title
            title_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="lyric.title"]')
            title = title_element.text.strip()

            # Extract the lyrics
            lyrics_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="lyrics.lyricLine"]')
            lyrics = [elem.text for elem in lyrics_elements if elem.text]

            # Combine the title and lyrics
            lyrics_collection[title] = "\n".join(lyrics)

        except Exception as e:
            lyrics_collection[url] = f"Failed to scrape: {e}"

    return lyrics_collection

if __name__ == "__main__":
    # List of URLs to scrape
    urls = [
  "https://lyrics.lyricfind.com/lyrics/ink-waruntorn-phob-rak",
  "https://lyrics.lyricfind.com/lyrics/boyd-kosiyabong-rak-khun-kao-laew",
  "https://lyrics.lyricfind.com/lyrics/risa-narisa-my-daisy",
  "https://lyrics.lyricfind.com/lyrics/pang-nakarin-kon-mee-sanay",
  "https://lyrics.lyricfind.com/lyrics/lula-rak-pa-ti-han",
  "https://lyrics.lyricfind.com/lyrics/whal-dolph-jai-daew",
  "https://lyrics.lyricfind.com/lyrics/jetseter-choob",
  "https://lyrics.lyricfind.com/lyrics/basketband-khon-narak-mak-jai-raiy",
  "https://lyrics.lyricfind.com/lyrics/earth-patravee-you-you-you",
  "https://lyrics.lyricfind.com/lyrics/violette-wautier-tang-tae-mee-ther-chan-mee-khwam-suk-this-time",
  "https://lyrics.lyricfind.com/lyrics/no-one-else-tor-jak-nee-pleng-rak-took-pleng-ja-pen-khong-ter-tao-nun",
  "https://lyrics.lyricfind.com/lyrics/three-man-down-khang-kan",
  "https://lyrics.lyricfind.com/lyrics/pause-kae-dai-pen-kon-sud-tai-tee-ter-kidtheung",
]
    

    # Set up Selenium with Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Scrape lyrics and titles
        lyrics_collection = scrape_lyrics_with_titles(driver, urls)

        # Save titles and lyrics to a file
        with open("lyrics_output.txt", "w", encoding="utf-8") as file:
            for title, lyrics in lyrics_collection.items():
                file.write(f"Title: {title}\n")
                file.write(lyrics)
                file.write("\n-------------------\n")

        print("Lyrics and titles have been saved to 'lyrics_output.txt'.")

    finally:
        # Close the browser
        driver.quit()
