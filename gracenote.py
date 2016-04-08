import sys, pygn, json, pprint

clientID = '1819536053-3AFF3925E00EE6762C465C9D5F92FF3C'
userID = '27680222405868105-7FDEC129F7C2D66326D1A13CE391976C'

pp = pprint.PrettyPrinter(indent=4)

artists = ['ABBA', 'Eminem', 'Bon Jovi', 'Bon Iver', 'Ke$ha', 'alt-J', 'Killers', 'Grouplove', 'Beach Boys', 'Green Day', 'OutKast', 'Weezer', 'Kanye West', 'Justin Bieber', 'Matt and Kim', 'Muse']
artist_info_list = []

for a in artists:
    result = pygn.search(clientID=clientID, userID=userID, artist=a) 
    artist_info_list.append(result)

song_list = []
for artist in artist_info_list:
    for song in artist['tracks']:
        song_list.append((song['track_title'], artist['album_artist_name']))

album_list = []
track_info_list = []
for song in song_list:
    result = pygn.search(clientID=clientID, userID=userID, track=song[0], artist=song[1])
    track_info_list.append(result)
    album = result['album_title']
    if not album in album_list:
        album_list.append(album)


artist_info_list
album_list
track_info_list


pp.pprint(track_info_list)



# with open('artist_info.json', 'w') as fp:
#     json.dump(artist_info_list, fp)

with open('album_info.json', 'w') as fp:
    json.dump(album_list, fp)

# with open('track_info.json', 'w') as fp:
#     json.dump(track_info_list, fp)