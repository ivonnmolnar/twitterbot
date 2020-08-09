import tweepy, time, random
from datetime import datetime
from keys import *
import codecs

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Need these four functions to save the current state in case the programme stops running
#Else it would have the original state, ex. without the already-used names/compliments/facts being removed

def resource_read(file_name):
    return_list = []
    with open(file_name,encoding="utf8") as f:
        for line in f:
            return_list.append(line.strip())
    return return_list

def resource_write(file_name,rlist):
    with codecs.open(file_name,'w',encoding="utf8") as f:
        for item in rlist:
            f.write(item)
            f.write('\n')

def date_read(file_name):
    temp = []
    with open(file_name,encoding="utf8") as f:
        for line in f:
            temp.append(int(line.strip()))
    return_tuple = tuple(temp)
    return return_tuple

def date_write(file_name,date_tuple):
    with codecs.open(file_name,'w',encoding="utf8") as f:
        for item in date_tuple:
            f.write(str(item))
            f.write('\n')

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def update_friends(): #creates the updates list of friends
    updated_friends = {}
    iterable_friends = api.friends("friendsowo")

    for friend in iterable_friends:
        updated_friends[friend._json['screen_name']] = friend._json['name']

    return updated_friends

def daily_fact():
    for friend_idname,friend_name in friends.items():
        if len(facts) == 0:
            api.update_status("Yo {0} this (facts) is empty!!! yEET".format(TWITTER_HANDLE))
            return None

        try:
            fact = random.choice(facts)
            facts.remove(fact)
            print(fact)
            resource_write("facts.txt",facts)
            api.update_status("@{0} Hey {1} did you know that: {2}".format(friend_idname,friend_name,fact))

        except:
            api.update_status("@{0} Hey {1} so it seems like the og tweet was too long so no fact for u today :c but next time!!!".format(friend_idname,friend_name))

def nice_reply():
    #if there are no names or compliments left, it tweets me to do something about it
    if len(compliments) == 0 or len(names) == 0:
        api.update_status("Yo {0} this (comp or names) is empty!!! yEET".format(TWITTER_HANDLE))
        return None

    last_seen_id = retrieve_last_seen_id('last_seen_id.txt')
    mentions = api.mentions_timeline(last_seen_id)

    for mention in reversed(mentions): #for each mention since the last it replies with a silly name and a compliment (both are random) c:
        print(str(mention.id) + ' - ' + mention.text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, 'last_seen_id.txt')

        try:
            name, compliment = random.choice(names), random.choice(compliments)
            print(name, compliment)
            #removes the used one to avoid repetitiveness
            names.remove(name)
            compliments.remove(compliment)
            resource_write("names.txt",names)
            resource_write("compliments.txt",compliments)

            api.update_status("@{0} Hey {1}, {2}".format(mention.user.screen_name,name,compliment),mention.id)

        except:
            api.update_status("@{0} Hey {1} so it seems like the og tweet was too long so here's the sample compliment: ur v egg-citing!!!".format(mention.user.screen_name,name),mention.id)

names = resource_read("names.txt")
compliments = resource_read("compliments.txt")
facts = resource_read("facts.txt")
last_date = tuple(date_read("last_date.txt"))
friends = {}

#MAIN PROGRAMME
while True:
    try:
        current_date = (datetime.now().year,datetime.now().month,datetime.now().day)
        if current_date != last_date: #daily updates - updates the friends list and uploads the daily fact
            friends = update_friends()
            daily_fact()
            last_date = current_date
            date_write("last_date.txt",last_date)
        nice_reply()

    except tweepy.TweepError:
        time.sleep(60 * 15)
        continue
