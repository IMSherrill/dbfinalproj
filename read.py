import json
from pprint import pprint

with open('song_data_final.json') as data_file:    
    data = json.load(data_file)


# tempos = []
# for song in data:
#     for genredict in song['tempo'].values():
#         for k, value in genredict.iteritems():
#             if k == 'TEXT' and not value in tempos:
#                 tempos.append(value)



pprint(data[0])


# pprint([x['track_title'] for x in data])






# with open('tempo_data_final.json', 'w') as fp:
#     json.dump(tempos, fp)

