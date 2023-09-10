import feedparser

from models.model_messages import RssFeed

MAX_LENGTH = 900  # TODO сделать единую константу в коде


def get_rss_text(rss_feed_item: RssFeed) -> str:
    feed = feedparser.parse(rss_feed_item.feed_link)
    if feed:
        rss_text = ''
        separator = ' *** '
        for feed_entry in feed.entries:
            if len(rss_text) + len(feed_entry.title) + len(separator) < MAX_LENGTH:
                rss_text += f'{feed_entry.title}{separator}'
            else:
                break
        return rss_text
