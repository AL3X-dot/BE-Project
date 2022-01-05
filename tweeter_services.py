import time
import tweepy
import json
from itertools import islice


#Twitter API credentials
consumer_key = "4wS7aRcSzzQDGUu8Bhj0WsJA6"
consumer_secret = "lntpDiSRlhs2b6GFFW4Jeaa2w7jTghCfCH4QDVBnpslpvN8z10"
access_key = "1182512372381962245-xxsuukPMm17Nuv80EbMrewUzX5KfLL"
access_secret = "0oURPmkPM4t1EAHWJq00YaQvbi4mQxSRaYXKFRlzP7HWM"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
# tweeter_id = "@DhruvitWaghela"
class Final_Tweet:
    travel_related = -1
    travel_category = ""
    sentiment = ""
    def __init__(self , tweet , tweet_score , screen_name):
        self.tweet = tweet
        self.tweet_score = tweet_score
        self.screen_name = screen_name

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def retweet(zoo , restaurant , museum , largest):
    final_tweet = zoo + restaurant + museum
    travel_count = {}
    for single_tweet in final_tweet:
        if single_tweet.screen_name not in travel_count:
            travel_count[single_tweet.screen_name] = 0
        travel_count[single_tweet.screen_name] += 1
    for key in travel_count:
        if travel_count[key] > 1:
            try:
                api.update_status("Heeyyyy @"+key+" I sugeest you to visit "+largest+" nearby. It is of same interest as that of you friends")
                print("Tweeted to @" + key)
            except:
                print("!!!!!!!----Already tweeted to @" + key +"----!!!!!!!")
    # travel_count = sorted(travel_count.items(), key=lambda item: item[1] , reverse = True)
    # top_screen_name = take(5, travel_count.iteritems())
    # print("]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    # print((travel_count))

def get_followers_following(tweeter_id):
    user_ids = []
    user_follower_ids = []

    # Following
    try:
        for page in tweepy.Cursor(api.friends_ids, screen_name = tweeter_id, count=5000).pages():
            user_ids.extend(page)

    except tweepy.RateLimitError:
        print("RateLimitError...waiting 1000 seconds to continue")
        time.sleep(1000)
        for page in tweepy.Cursor(api.friends_ids, screen_name = tweeter_id , count=5000).pages():
            user_ids.extend(page)

    #Followers
    try:
        for page in tweepy.Cursor(api.followers_ids, screen_name = tweeter_id, count=5000).pages():
            user_follower_ids.extend(page)

    except tweepy.RateLimitError:
        print("RateLimitError...waiting 1000 seconds to continue")
        time.sleep(1000)
        for page in tweepy.Cursor(api.followers_ids, screen_name = tweeter_id , count=5000).pages():
            user_follower_ids.extend(page)
    followings = []
    followers = []

    for start in range(0, min(4000, len(user_ids)), 100):
        end = start + 100

        #FOllowing
        try:
            followings.extend(api.lookup_users(user_ids[start:end]))

        except tweepy.RateLimitError:
            print("RateLimitError...waiting 1000 seconds to continue")
            time.sleep(1000)
            followings.extend(api.lookup_users(user_ids[start:end]))
        
        #Followers
        try:
            followers.extend(api.lookup_users(user_follower_ids[start:end]))

        except tweepy.RateLimitError:
            print("RateLimitError...waiting 1000 seconds to continue")
            time.sleep(1000)
            followers.extend(api.lookup_users(user_follower_ids[start:end]))
    user_data = {}
    user_data['user_screen_name'] = tweeter_id
    user_data['following'] = [following.screen_name for following in followings]
    user_data['followers'] = [follower.screen_name for follower in followers]
    with open('user_data/'+tweeter_id+'.json', 'w') as outfile:
        json.dump(user_data, outfile)

    # print(json_data)
    # for following in followings:

def get_tweets(username,no): 
          
        # Authorization to consumer key and consumer secret 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
        # Access to user's access key and access secret 
        auth.set_access_token(access_key, access_secret) 
  
        # Calling api 
        api = tweepy.API(auth) 
  
        # 200 tweets to be extracted 
        number_of_tweets=no
        tweets = api.user_timeline(screen_name= username , count = no ) 
  
        # Empty Array 
        tweet_list=[]  
        # print(tweets.__dict__.keys())
        # create array of tweet information: username,  
        # tweet id, date/time, text 
        tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created  
        i=0
        for j in tweets: 
            if j.lang == "en":
                retweet_count = j.retweet_count
                favorite_count = j.favorite_count
                hashtag_count = len(j.entities['hashtags'])
                url_count = len(j.entities['urls'])
                mention_count = len(j.entities['user_mentions'])
                try:
                    media_count = len(j.entities['media'])
                except:
                    media_count = 0
                tweet_length = len(j.text)

                tweet_score = (retweet_count/100) + (favorite_count/100) + hashtag_count*0.3 + url_count * 0.4 + mention_count * 0.3 + media_count * 0.6 + tweet_length/280
                
                single_tweet = Final_Tweet(j.text , tweet_score , j.user.screen_name) 
                # Appending tweets to the empty array tweet_list 
                tweet_list.append(single_tweet)  
  
        # Printing the tweets

        return tweet_list

def get_all_tweets(tweeter_id):
    with open('user_data/'+tweeter_id+'.json', 'r') as user_data:
        json_data = json.load(user_data)
    final_tweets = []
    for follow_screen_name in json_data['following']:
        final_tweets.extend(get_tweets(follow_screen_name , 20))
        
    for follow_screen_name in json_data['followers']:
        final_tweets.extend(get_tweets(follow_screen_name , 20))
            
    # for tweets in final_tweets:
    #     print(tweets.tweet)
    #     print(tweets.tweet_score)
    #     print("======================================================")
    # print(final_tweets[0].tweet)
    return final_tweets
if __name__ == "__main__":
    get_all_tweets("@sayliveg")
    
