import feedparser
import socket
from multiprocessing import Process, Manager

socket.setdefaulttimeout(5) # Default timeout for accessing feeds

# List of rss feeds to scan
rss_feeds = [
    "https://news.xbox.com/en-us/feed/",
    "https://www.reddit.com/r/gamers/.rss",
    "http://www.polygon.com/rss/index.xml",
    "https://majornelson.com/feed/",
    "https://www.vg247.com/feed/",
    "http://www.eurogamer.net/?format=rss",
    "https://mynintendonews.com/feed/",
    "https://blog.us.playstation.com/feed/",
    "https://www.pcgamer.com/rss/"
]

# Thread worker function for scanning a feed
def worker(rss_feed, thread_id, thread_results):
    feed = feedparser.parse(rss_feed)
    for entry in feed.entries:
        if "free" in entry.title.lower():
            thread_results[thread_id].append((entry.title, entry.link))
    print("%s: DONE" % rss_feeds[thread_id])

# Scan all the feeds and add the results to a list
def getFreeGames():
    rss_threads = []
    thread_id = 0
    manager = Manager()

    thread_results = manager.dict()
    for i in range(len(rss_feeds)):
        thread_results[i] = manager.list()

    for rss_feed in rss_feeds:
        p = Process(target=worker, args=(rss_feed, thread_id, thread_results))
        p.start()
        rss_threads.append(p)
        thread_id += 1

    for thread in rss_threads:
        thread.join()

    free_game_articles = []
    for i in range(thread_id):
        for result in thread_results[i]:
            free_game_articles.append(result)
    
    return free_game_articles

if __name__ == "__main__":
    games = getFreeGames()
    print("\nGAMES:")
    for game in games:
        print("%s\t%s" % (game[0], game[1]))