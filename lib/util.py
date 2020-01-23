
def get_channel_names(guild):
    names = []
    for v in guild.by_category():
        category = v[0]
        channels = v[1]
        indent = "   "
        if category is None:
            indent = ""
        else:
            names.append((category, ">" + category.name))

        for chan in channels:
            names.append((chan, indent + "#" + chan.name))

    return names


