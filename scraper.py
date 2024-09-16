from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time


def extract_tweets(containers):
    # Lists to store users and tweets
    users = []
    tweets = []
    print(f"Extracting {len(containers)} tweets")
    # Loop through each container and extract the tweet text and user
    for container in containers:
        print("=====================================")
        print(container)
        print("=====================================")
        try:
            # Extract the username
            user = container.find_element(
                By.XPATH, './/div[@data-testid="User-Name"]//span').text

            # Extract the tweet text
            tweet = container.find_element(
                By.XPATH, './/div[@data-testid="tweetText"]').text

            # Add to the lists
            print(f"User: {user}")
            print(f"Tweet: {tweet}")
            users.append(user)
            tweets.append(tweet)
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

# open the file in write mode
with open("tweets.csv", "w") as file:
    # write the header
    file.write("User,Tweet\n")
    # write the data
    for i, tweet in enumerate(tweets):
        print(f"Tweet: {tweet}  \nUser: {users[i]}\n =====================\n")
        file.write(f"{users[i]},{tweet}\n")

# Close the browser
driver.quit()

print("Data extracted and saved to tweets.csv")
