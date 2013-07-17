#finagle script access
import sys
import os
from os.path import dirname
mydir = sys.path[0]
sys.path.append(dirname(mydir))
sys.path.append(dirname(dirname(mydir)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rb.settings'

import rb
from rb.songs.models import Song
from django.utils.encoding import force_unicode
import time
import urllib2
import re
from BeautifulSoup import BeautifulSoup, MinimalSoup

def get_number_for_diff(diff):
    if diff.count("No stars"):
        return 0
    elif diff.count("One star"):
        return 1
    elif diff.count("Two stars"):
        return 2
    elif diff.count("Three stars"):
        return 3
    elif diff.count("Four stars"):
        return 4
    elif diff.count("Five stars"):
        return 5
    elif diff.count("Devil"):
        return 6
    elif diff.count("* "):
        return diff.count("* ")+1
    print stars
    raise Exception

def get_diff_fragment(diff):
    diff = str(diff).replace("\n","")
    if diff.count("Guitar"):
        instrument = "Guitar"
    elif diff.count("Bass"):
        instrument = "Bass"
    elif diff.count("Vocals"):
        instrument = "Vocals"
    elif diff.count("Drums"):
        instrument = "Drums"
    stars = get_number_for_diff(diff)
    try:
        return (instrument, stars)
    except:
        return (False,False)

def get_instrument_diffs(song_link):
    url = "http://www.rockband.com/%s" % song_link
    print url
    response = urllib2.urlopen(url=url)
    try:
        pool = BeautifulSoup(response.read())
    except:
        print response
        print dir(response)
        print response.read()
        raise
    sidebar = pool.find("div", attrs={"class":"page-sidebar"})
    if sidebar is None:
        for item in pool:
            print item
        raise Exception, "foo"
    try:
        diffs = sidebar.findAll('p')
    except:
        print sidebar
        raise
    instrument_diffs = {}
    for diff in diffs:
        (instrument, difficulty) = get_diff_fragment(diff)
        if instrument:
            instrument_diffs[instrument] = difficulty
    return instrument_diffs

def make_song(row):
    parts = row.findAll('td', text=True)
    songparts = []
    for part in parts:
        if part != u"\n" and part != u" ":
            songparts.append(part)
    try:
        name = songparts[0]
        band = songparts[1]
        if band == "(Cover version)":
            name += band
            band = songparts[2]
            songparts = songparts[1:]

        #check for song already exists; if so, bail
        song_check = Song.objects.filter(band=band.encode("utf-8")).filter(name=name.encode("utf-8")).count()
        if song_check:
            return False
        year = int(songparts[2])
        genre = songparts[3]
        stars = songparts[4]
        band_diff = get_number_for_diff(stars)
        source = songparts[5]
        release = songparts[6]

        #get instrument difficulties
        link = row.find('td').find('a')['href']
        try:
            instrument_diffs = get_instrument_diffs(link)
        except:
            print link
            print "Can't make this song?"
            return

        #we made it, we've got a new song
        new_song = Song(name=name.encode("utf-8"),
                        band=band.encode("utf-8"),
                        year=int(year),
                        band_diff=int(band_diff),
                        guitar_diff=int(instrument_diffs['Guitar']),
                        bass_diff=int(instrument_diffs['Bass']),
                        vocals_diff=int(instrument_diffs['Vocals']),
                        drums_diff=int(instrument_diffs['Drums']),
                        source=source.encode("utf-8"),
                        release=time.strftime("%Y-%m-%d", time.strptime(release, "%m/%d/%y"))
                        )
        return new_song
    except:
        print songparts
        raise
    
if __name__ == "__main__":
    start_url = "http://www.rockband.com/music/getSearchResultsTable_Ajax?search_terms=%22%22&sort_on=songs.NAME"
    response = urllib2.urlopen(url=start_url)
    pool = BeautifulSoup(response)
    list = pool.findAll('div', attrs={'class': 'wide-page-body'})
    body = list[0]
    rows = body.findAll('tr')
    for row in rows:
        song = make_song(row)
        try:
            if song:
                song.save()
        except:
            print song
            raise
