from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time


def extract_tweets(containers):
    # Lists to store users and tweets
    users = []
    tweets = []
    print(f"Extracting {len(containers)} tweets")
    # Loop through each container and extract the tweet text and user
    for container in containers:
        try:
            # Extract the username
            user = container.find_element(
                By.XPATH, './/div[@data-testid="User-Name"]//span').text

            # Extract the tweet text
            tweet_texts = container.find_element(
                By.XPATH, './/div[@data-testid="tweetText"]')

            tweet = ""
            for text in tweet_texts.find_elements(By.XPATH, './/span'):
                tweet += text.text+" "

            # remvoe new lines and tabs from the tweet
            tweet = tweet.replace("\n", " ").replace("\t", " ")
            print("=====================================")
            print(f"User: {user}")
            print(f"Tweet: {tweet}")
            print("=====================================")
            # open file in append mode
            with open("tweets.csv", "a") as file:
                file.write(f"{user}\t{tweet}\n")
        except Exception as e:
            print(f"Error extracting data: {e}")
            continue
        # if no errors, print the user and tweet
    return users, tweets


# Path to geckodriver
# Replace with the path to your geckodriver
geckodriver_path = "./geckodriver"

# Firefox browser configuration
options = webdriver.FirefoxOptions()
# Optional: run Firefox in headless mode (without graphical interface)
# options.add_argument('--headless')
service = Service(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=service, options=options)

# Search URL on X (Twitter)
search_url = "https://x.com/search?q=trump&src=typed_query&f=live"

# Open the page
driver.get(search_url)

# Wait a moment for the page to load (you can adjust the time)

# ask the user for input: "continue?[Y/n]"
input = input("Continue?[Y/n]")
if input == "n":
    driver.quit()
    print("Exiting program")
    exit()
# Lists to store users and tweets
users = []
tweets = []

scroll_count = 15
for i in range(scroll_count):
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait for the page to load more tweets
    time.sleep(40)  # Adjust the delay if needed

    # Extract tweet containers
    tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
    print(f"Extracted {len(tweets)} new tweets")
    # Extract the users and tweets
    new_users, new_tweets = extract_tweets(tweets)
    # Add to the lists
    users.extend(new_users)
    tweets.extend(new_tweets)

# Close the browser
driver.quit()

print("Data extracted and saved to tweets.csv")
