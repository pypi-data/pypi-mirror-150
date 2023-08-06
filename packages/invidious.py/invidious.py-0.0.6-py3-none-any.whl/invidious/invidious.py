from .playlist_item import PlaylistItem
from .channel_item import ChannelItem
from .video_item import VideoItem
from .channel import Channel
from .video import Video
import requests

HEADERS = ({
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
        "/75.0.3770.100 Safari/537.36"
    })

def request(url: str):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200: return response.json()

def search(query: str, page=0, sort_by="", duration="", date="", ctype="", feauters=[], region=""):
    """
    Invidious search method. Return list with VideoItem, ChannelItem, PlaylistItem.

    query: your search query.
    page: number of page.
    sort_by: [relevance, rating, upload_date, view_count].
    date: [hour, today, week, month, year].
    duration: [short, long].
    ctype: [video, playlist, channel, all] (default: video).
    feauters: [hd, subtitles, creative_commons, 3d, live, purchased, 4k, 360, location, hdr].
    region: ISO 3166 country code (default: US).
    """
    req = f"https://invidious.snopyta.org/api/v1/search?q={query}"
    if page > 0: req += f"&page={page}"
    if sort_by != "": req += f"&sort_by={sort_by}"
    if duration != "": req += f"&duration={duration}"
    if date != "": req += f"&date={date}"
    if ctype != "": req += f"&type={ctype}"
    if feauters != []:
        req += "&feauters="
        for feauter in feauters:
            req += feauter+","
        req = req[:len(req)-2]
    if region != "": req += f"region={region}"

    jdict = request(req)
    itemsList = []

    for item in jdict:
        citem = None
        if item['type'] == 'channel': citem = ChannelItem()
        elif item['type'] == 'video': citem = VideoItem()
        elif item['type'] == 'playlist': citem = PlaylistItem()
        if citem != None: 
            citem.loadFromDict(item)
            itemsList.append(citem)
    
    return itemsList

def get_video(videoId: str, region=""):
    """
    Invidious get_video method. Return Video by id.
    
    videoId: id of video.
    region: ISO 3166 country code (default: US).
    """
    req = f"https://invidious.snopyta.org/api/v1/videos/{videoId}"
    if region != "": req += f"&region={region}"

    response = request(req)
    if response == None:
        print(f"ERROR: Video with {videoId} id doesn't exists.")
        return None
        
    video = Video()
    video.loadFromDict(response)

    return video

def get_channel(authorId: str, sort_by=""):
    """
    Invidious get_channel method. Return Channel by id.
    
    authorId: id of channel.
    sort_by: sorting channel videos. [newest, oldest, popular] (default: newest).
    """
    req = f"https://invidious.snopyta.org/api/v1/channels/{authorId}"
    if sort_by != "": req += f"&sort_by={sort_by}"

    response = request(req)
    if response == None: 
        print(f"ERROR: Channel with {authorId} id doesn't exists.")
        return None

    channel = Channel()
    channel.loadFromDict(response)

    return channel

if __name__ == "__main__":
    print(get_channel("UCrPw1-nDPppBuh7UCBqu3GQ").author)
    print(get_video("L8Ohygt5UVY").title)
    items = search(query="kuplinov", date="today")
    for item in items:
        if type(item) == VideoItem:
            print(item.title)
