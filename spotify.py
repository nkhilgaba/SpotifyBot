# export SPOTIPY_CLIENT_ID=''
# export SPOTIPY_CLIENT_SECRET=''
# export SPOTIPY_REDIRECT_URI='http://localhost/'

import time
import sys
import spotipy
import spotipy.util as util


TOKEN = ''
scope = 'user-library-read'
file = open('tracklist.txt', 'a+')
tracks = []

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print ("Usage: %s username" % (sys.argv[0],))
    sys.exit()


def in_tracklist(tr):
    file.seek(0)
    for line in file:
        tracks.append(line.strip())
    if tr in tracks:
        return True
    return False


def get_url(sp, track_id):
    track = sp.track(track_id)
    ext_url = track['external_urls']
    url = ext_url['spotify']
    return url


def add_to_tracklist(tracks_id):
    for track_id in tracks_id:
        file.write(track_id + '\n')


def fetch():
    try:
        token = util.prompt_for_user_token(username, scope,
                                           client_id='',
                                           client_secret='',
                                           redirect_uri='http://localhost/')
        print('Authenticating!')
        if token:
            sp = spotipy.Spotify(auth=token)
            urls = []
            tracks_id = []
            user = sp.me()
            followers = user['followers']

            print('Hi', user['display_name'])
            print(f"You have {followers['total']} followers")
            results = sp.current_user_saved_tracks(limit=10)
            print('\n')
            for r in results['items']:
                track_id = r['track']['id']
                if in_tracklist(track_id):
                    print('Already Sent:', r['track']
                          ['name'], '|', 'ID:', r['track']['id'])
                elif not in_tracklist(track_id):
                    print('Sending Track:',
                          r['track']['name'], '|', 'ID:', r['track']['id'])
                    print(get_url(sp, track_id))
                    urls.append(get_url(sp, track_id))
                    tracks_id.append(track_id)
            return urls, tracks_id
        else:
            print("Can't get token for", username)
    except e:
        print('Error:', e)
