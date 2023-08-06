import invidious as iv

searched = iv.search("distrotube")

channels = []

for item in searched:
    if type(item) == iv.ChannelItem:
        channel = iv.get_channel(item.authorId)
        channels.append(channel)

for channel in channels:
    print(channel.author)