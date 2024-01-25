import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os


load_dotenv()


# access_token = "EAAM6hJoE9EEBO4eZArrFLc14cb2zw25duZAZBxPOFBhUSAyoI9ZCfBQ3Rggn7PnA0FwItT5WpxBKt1p7JhLsPIuU6X0wPfpVmu2atcABoXCwbZCHsyknMZBF7HhkLAM82IMlOJpV6cbBnuHnmGsZBQrl6q5aAgrZAdP6rQtinnsoShJTZCwAp9g9DBSd31kvp0nikKDTq1Aq8mRBLbJOg7FHlIUBbCIt44YsZD"

access_token = os.environ['ACCESS_TOKEN']
user_id = os.environ['USER_ID']


# user_id = '17841463128846338'

def get_instagram_username(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            canonical_link = soup.find("link", rel="canonical")
            if canonical_link:
                href = canonical_link['href']
                # Using regular expression to extract the username
                match = re.search(r'instagram\.com/([^/]+)/', href)
                return match.group(1) if match else "Username not found"
            else:
                return "Canonical link not found"
        else:
            return f"Failed to access the page, status code get_instagram_username: {response.status_code}"
    except Exception as e:
        return str(e)

# url = 'https://www.instagram.com/reel/C2Pd40Kyqx_/'
# print(get_instagram_username(url))


# "https://graph.facebook.com/v18.0/ig_hashtag_search?user_id=17841463128846338&q=bluebottle&access_token=EAAM6hJoE9EEBO87c6XIyccUQjcwebq3cfCvr371LZA7VZBcJDallXgzBPV4IyQ9tEt9oL6HyTqdsw0ruvMuI9ZCB1k4bI3nkNrGnLGZCbEZBZAuHEOssspWgjpuOiCgRmq9YdxZCemfIXv98EDL7U9xuVPnb5b3kPnbkcIPgglWE9gN8jw3NxyLIfLpsswGmH4jNLo3ZAS7tUjNZBHZABZBV7ncqUhZAHNcdi8X7oQZDZD"

def get_hashtag_id(hashtag):
    try:
        response = requests.get('https://graph.facebook.com/v18.0/ig_hashtag_search?q=' + hashtag + '&user_id=' + user_id + '&access_token=' + access_token)
        if response.status_code == 200:
            print('hashtag ID --> ', response.json()['data'][0]['id'])
            return response.json()['data'][0]['id']
        else:
            return f"Failed to access the page, status code get_hashtag_id: {response.status_code}"
    except Exception as e:
        return str(e)


# curl -i -X GET \
# #  "https://graph.facebook.com/v18.0/17843857450040591/recent_media?user_id=17841463128846338&fields=id%2Cmedia_type%2Ccomments_count%2Clike_count%2Cpermalink&access_token=EAAM6hJoE9EEBOzW5is7rOLx79Q8yNtXm44q3ICEoxYZAhsqeuH66SPFGFnTO9fauHZCiVita6SQuubHnr6wHpDiRWwMVKu3ZB7qNYj4rOQXeLAIydjad7DUbCakfjGKOMZBOmbJ7TqZCb8b2y7Y9bZCKUGmwlblm1x6ZAX5mIO1VbItJx8FEB4EBry6zlxzQ4KqibXZBFJZAQaWdC4Sdk5ZAnZCIJ16yFiDnxst"


def get_hashtag_posts(hashtag_id):
    try:
        response = requests.get('https://graph.facebook.com/v18.0/' + hashtag_id + '/top_media?user_id=' + user_id + '&fields=id%2Cmedia_type%2Ccomments_count%2Clike_count%2Cpermalink&access_token=' + access_token)
        if response.status_code == 200:
            #log the response
            print('hashtag posts --> ',response.json()['data'])
            return response.json()['data']
        else:
            return f"Failed to access the page, status code get_hashtag_posts: {response.status_code}"
    except Exception as e:
        return str(e)

def get_permalinks(posts):
    permalinks = []
    for post in posts:
        permalinks.append(post['permalink'])
    #log the permalinks
    print('permalinks --> ',permalinks)
    return permalinks

def get_usernames(permalinks):
    usernames = []
    for permalink in permalinks:
        usernames.append(get_instagram_username(permalink))
    #log the usernames
    print('usernames --> ',usernames)
    return usernames


#  "https://graph.facebook.com/v18.0/17841463128846338?fields=business_discovery.username(rebecasegraves_)%7Bfollowers_count%2Cmedia_count%2Cmedia%7Bcomments_count%2Clike_count%7D%7D&access_token=EAAM6hJoE9EEBO6KEm5ZBgN93ijyZBo2z42v9FyXHqSmsEOcygsQProlvXvxiRxUKnRxCC0ElOEeC7TwjeFb6KYtDYJWqkAtEAKtfCFHnGyjwc2kQTt7dADSeI6ov0wf0q2ZAM4FKSdGnDJPdZAvsZAB5GLON5FvD6OpN1ZBzcNyujvLWX4fAfQ1l6TP0kstPTYdZAY1zN9tfgJ4ZClHlmfZBu0e0CMKXLf4EZD"

def calculate_average_likes(posts):
    total_likes = 0
    for post in posts:
        #check if key exists
        if 'like_count' in post:
            total_likes += post['like_count']
    return total_likes / len(posts)

def get_user_info(username):
    try:
        response = requests.get('https://graph.facebook.com/v18.0/' + user_id + '?fields=business_discovery.username(' + username + ')%7Bfollowers_count%2Cmedia_count%2Cmedia%7Bcomments_count%2Clike_count%7D%7D&access_token=' + access_token)
        if response.status_code == 200:
            #log the response
            print('user info --> ',response.json()['business_discovery'])
            return response.json()['business_discovery']
        else:
            return f"Failed to access the page, status code get_user_info: {response.status_code}"
    except Exception as e:
        return str(e)

def calculate_engagement_rate(posts, follower_count):
    total_likes = 0
    total_comments = 0
    for post in posts:
        #check if key exists
        if 'like_count' in post:
            total_likes += post['like_count']
        if 'comments_count' in post:
            total_comments += post['comments_count']
    total_interactions = total_likes + total_comments
    #handle division by zero
    if follower_count == 0:
        return 0
    else:
        return total_interactions / (follower_count * len(posts))


def get_user_infos(usernames):
    user_infos = []
    for username in usernames:
        fetched_user_info = get_user_info(username)
        #check if fetched_user_info is a json object
        if fetched_user_info and isinstance(fetched_user_info, dict):
            fetched_user_info['username'] = username
            user_infos.append(fetched_user_info)
    #log the user_infos
    print('user_infos  --> ',user_infos)
    return user_infos

def check_valid_user_infos(user_infos, min_followers: int =1000, max_followers: int = 10000, engagement_rate: int = 5, average_likes: int = 100):
    valid_user_infos = []
    for user_info in user_infos:
        follower_count = user_info['followers_count']
        avg_likes = calculate_average_likes(user_info['media']['data'])
        engagement_rate = calculate_engagement_rate(user_info['media']['data'], follower_count)
        if user_info['followers_count'] > min_followers and user_info['followers_count'] < max_followers and avg_likes > average_likes and engagement_rate > engagement_rate/100:
            print('follower_count --> ',follower_count)
            print('avg_likes --> ',avg_likes)
            print('engagement_rate --> ',engagement_rate)
            user_data = {
                'username': user_info['username'], 
                'follower_count': user_info['followers_count'],
                'avg_likes': avg_likes,
                'engagement_rate': engagement_rate
            }
            valid_user_infos.append(user_data)
    return valid_user_infos

# hashtag_id = get_hashtag_id('decoration')
# posts = get_hashtag_posts(hashtag_id)
# permalinks = get_permalinks(posts)
# usernames = get_usernames(permalinks)
# print('usernames --> ',len(usernames))
# # user_info = get_user_info(usernames[1])
# user_infos = get_user_infos(usernames)
# print('userinfos --> ',len(user_infos))
# valid_user_infos = check_valid_user_infos(user_infos)
# print('valid_user_infos --> ',len(valid_user_infos))
