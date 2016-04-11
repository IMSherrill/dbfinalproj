#!/usr/bin/env python 

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import ForeignKey
from sqlalchemy import desc
from sqlalchemy.orm import relationship
from pprint import pprint
import json
import random
import sys
import pygn

# pygn settings
clientID = '1819536053-3AFF3925E00EE6762C465C9D5F92FF3C'
userID = '27680222405868105-7FDEC129F7C2D66326D1A13CE391976C'


# Connection settings
settings = {
    'userName': 'root',
    'password': '',
    'serverName': "localhost",
    'portNumber': 3306,
    'dbName': "final",
}

conn = create_engine('mysql://{0[userName]}:{0[password]}@{0[serverName]}:{0[portNumber]}/{0[dbName]}'.format(settings))
Session = sessionmaker(bind=conn)
Base = declarative_base()
session = Session()

class Artist(Base):
    __tablename__ = "Artist"
    artistid = Column(Integer, nullable=False, unique=True, primary_key=True)
    name = Column(String)
    era = Column(String)

class Album(Base):
    __tablename__ = "Album"
    albumid = Column(Integer, primary_key=True)
    albumtitle = Column(String)
    artistid = Column(Integer, ForeignKey(Artist.artistid))
    artist = relationship("Artist", foreign_keys={artistid})


class Song(Base):
    __tablename__ = 'Song'
    songid = Column(Integer, primary_key=True)
    songtitle = Column(String)
    artistid = Column(Integer, ForeignKey(Artist.artistid))
    albumid = Column(Integer, ForeignKey(Album.albumid))

    artist = relationship("Artist", foreign_keys={artistid})
    album = relationship("Album", foreign_keys={albumid})

class Tempo(Base):
    __tablename__ = "Tempo"
    tempoid = Column(Integer, primary_key=True)
    name = Column(String)

class Mood(Base):
    __tablename__ = "Mood"
    moodid = Column(Integer, primary_key=True)
    name = Column(String)

class Genre(Base):
    __tablename__ = "Genre"
    genreid = Column(Integer, primary_key=True)
    name = Column(String)

class Playlist(Base):
    __tablename__ = "Playlist"
    playlistid = Column(Integer, primary_key=True)
    name = Column(String)

class SongGenre(Base):
    __tablename__ = "SongGenre"
    Songgenreid = Column(Integer, primary_key=True)
    songid = Column(Integer, ForeignKey(Song.songid))
    genreid = Column(Integer, ForeignKey(Genre.genreid))

    song = relationship("Song", foreign_keys={songid})
    genre = relationship("Genre", foreign_keys={genreid})

class SongTempo(Base):
    __tablename__ = "SongTempo"
    songtempoid = Column(Integer, primary_key=True)
    songid = Column(Integer, ForeignKey(Song.songid))
    tempoid = Column(Integer, ForeignKey(Tempo.tempoid))

    song = relationship("Song", foreign_keys={songid})
    tempo = relationship("Tempo", foreign_keys={tempoid})

class SongMood(Base):
    __tablename__ = "SongMood"
    songmoodid = Column(Integer, primary_key=True)
    songid = Column(Integer, ForeignKey(Song.songid))
    moodid = Column(Integer, ForeignKey(Mood.moodid))

    song = relationship("Song", foreign_keys={songid})
    mood = relationship("Mood", foreign_keys={moodid})

class SongPlaylist(Base):
    __tablename__ = "songplaylist"
    songplaylistid = Column(Integer, primary_key=True)
    songid = Column(Integer, ForeignKey(Song.songid))
    playlistid = Column(Integer, ForeignKey(Playlist.playlistid))

    song = relationship("Song", foreign_keys={songid})
    playlist = relationship("Playlist", foreign_keys={playlistid})


Base.metadata.create_all(conn)

def importArtist():
    with open("artist_data_final.json") as datafile:
        data = json.load(datafile)
        for artist in data:
            a = Artist(name=artist.get("name"), era=artist.get("era"))
            session.add(a)
            session.commit()

def importAlbum():
    with open("album_data_final.json") as datafile:
        data = json.load(datafile)
        for album in data:
            artistInfo = session.query(Artist).filter_by(name=album['artist']).first()
            artistID = int(artistInfo.artistid)
            a = Album(albumtitle=album.get("title"), artistid=artistID)
            session.add(a)
            session.commit()

def importSong():
    with open("song_data_final.json") as datafile:
        data = json.load(datafile)
        for song in data:
            artistInfo = session.query(Artist).filter_by(name=song['artist']).first()
            artistID = int(artistInfo.artistid)

            albumInfo = session.query(Album).filter_by(albumtitle=song['album_title']).first()
            albumid = int(albumInfo.albumid)

            s = Song(songtitle=song['track_title'], artistid=artistID, albumid=albumid)
            session.add(s)
            session.commit()

def importMood():
    with open("mood_data_final.json") as datafile:
        data = json.load(datafile)
        for mood in data:
            m = Mood(name=mood)
            session.add(m)
            session.commit()

def importGenre():
    with open("genre_data_final.json") as datafile:
        data = json.load(datafile)
        for genre in data:
            g = Genre(name=genre)
            session.add(g)
            session.commit()


def importTempo():
    with open("tempo_data_final.json") as datafile:
        data = json.load(datafile)
        for tempo in data:
            t = Tempo(name=tempo)
            session.add(t)
            session.commit()

def importSongMood():
    with open("song_data_final.json") as datafile:
        data = json.load(datafile)

        for song in data:
            songInfo = session.query(Song).filter_by(songtitle=song['track_title']).first()
            songid = int(songInfo.songid)

            for mood in song['mood'].values():
                m = mood['TEXT']

                moodInfo = session.query(Mood).filter_by(name=m).first()
                moodid = int(moodInfo.moodid)

                x = SongMood(songid=songid , moodid=moodid)
                session.add(x)
                session.commit()



def importSongTempo():
    with open("song_data_final.json") as datafile:
        data = json.load(datafile)

        for song in data:
            songInfo = session.query(Song).filter_by(songtitle=song['track_title']).first()
            songid = int(songInfo.songid)

            for tempo in song['tempo'].values():
                t = tempo['TEXT']

                tempoInfo = session.query(Tempo).filter_by(name=t).first()
                tempoid = int(tempoInfo.tempoid)

                x = SongTempo(songid=songid , tempoid=tempoid)
                session.add(x)
                session.commit()


def importSongGenre():
    with open("song_data_final.json") as datafile:
        data = json.load(datafile)

        for song in data:
            songInfo = session.query(Song).filter_by(songtitle=song['track_title']).first()
            songid = int(songInfo.songid)

            for genre in song['genre'].values():
                g = genre['TEXT']

                genreInfo = session.query(Genre).filter_by(name=g).first()
                genreid = int(genreInfo.genreid)

                x = SongGenre(songid=songid , genreid=genreid)
                session.add(x)
                session.commit()


def addSingleArtist():
    artistExists = True
    while artistExists:
        artistName = raw_input("Enter the artist's name: ")
        if session.query(Artist).filter_by(name=artistName).first():
            print("This artist already exists in the database. Please try again.")
        else:
            artistExists = False
    thisera = raw_input("Please enter the artist's era: ")
    artist = Artist(name=artistName, era=thisera)
    session.add(artist)
    session.commit()


def addSingleAlbum():
    albumExists = True
    while albumExists:
        albumName = raw_input("Please enter the name of the Album: ")
        artistName = raw_input("Please enter the name of the Artist: ")
        if not session.query(Artist).filter_by(name=artistName).first():
            print "This artist does not exist. Please enter an existing Artist: "
            continue
        else:
            artist = session.query(Artist).filter_by(name=artistName).first()
            artistID = artist.artistid
            if session.query(Album).filter_by(albumtitle=albumName, artistid=artistID).first():
                print "This album exists, please try again."
                continue
            else:
                thisalbum = Album(albumtitle=albumName, artistid=artistID)
                session.add(thisalbum)
                session.commit()
                albumExists = False


def addSingleSong():
    songExists = False
    while not songExists:
        songName = raw_input("Please enter the name of the song: ")
        artistName = raw_input("Please enter the name of the artist: ")
        albumName = raw_input("Please enter the name of the album: ")
        if not session.query(Artist).filter_by(name=artistName).first():
            print "This artist does not exist. Please enter an existing Artist: "
            continue
        if not session.query(Album).filter_by(albumtitle=albumName).first():
            print "This album does not exist. Please enter an existing album name: "
            continue
        else:
            artist = session.query(Artist).filter_by(name=artistName).first()
            artistID = artist.artistid
            album = session.query(Album).filter_by(albumtitle=albumName).first()
            albumID = album.albumid
            if session.query(Song).filter_by(songtitle=songName, artistid=artistID, albumid=albumID).first():
                print "This song already exists."
                continue
            else:
                thissong = Song(songtitle=songName, artistid=artistID, albumid=albumID)
                session.add(thissong)
                session.commit()
                songExists = True
                alldbmoods = session.query(Mood).all()
                allmoods = []
                for mood in alldbmoods:
                    allmoods.append(mood.name)
                pprint(allmoods)
                mood = raw_input("What is the mood of this song: ")
                if mood not in alldbmoods:
                    addMood(mood)
                addSongMood(songName, mood)
                alldbgenres = session.query(Genre).all()
                allgenres = []
                for genre in alldbgenres:
                    allgenres.append(genre.name)
                pprint(allgenres)
                genre = raw_input("What is the genre of this song: ")
                if genre not in allgenres:
                    addGenre(genre)
                addSongGenre(songName, genre)
                alldbtempos = session.query(Tempo).all()
                alltempos = []
                for tempo in alldbtempos:
                    alltempos.append(tempo.name)
                pprint(alltempos)
                tempo = raw_input("What is the tempo of this song: ")
                if tempo not in alltempos:
                    addTempo(tempo)
                addSongTempo(songName, tempo)


def makePlayList(song, length):
    try:
        song = session.query(Song).filter_by(songtitle=song).first()
        songID = song.songid
    except:
        print 'error song not found in database try a new one'
        return 

    choices = ['mood', 'genre', 'tempo']
    playlist = [songID]


    while len(playlist) < length:
        choice=random.choice(choices)

        if choice == 'mood':
            moodids = []
            songmoods=session.query(SongMood).filter_by(songid=songID).all()
            for songmood in songmoods:
                mood = session.query(Mood).filter_by(moodid=songmood.moodid).first()
                moodids.append(mood.moodid)

            mid = random.choice(moodids)
            songmoodswithmoodid = session.query(SongMood).filter_by(moodid=mid).all()
            songmood = random.choice(songmoodswithmoodid)
            song = session.query(Song).filter_by(songid=songmood.songid).first()
            if song.songid not in playlist:
                playlist.append(song.songid)



        if choice == 'genre':
            genreids = []
            songgenres=session.query(SongGenre).filter_by(songid=songID).all()
            for songgenre in songgenres:
                genre = session.query(Genre).filter_by(genreid=songgenre.genreid).first()
                genreids.append(genre.genreid)

            gid = random.choice(genreids)
            songgenreswithgenreid = session.query(SongGenre).filter_by(genreid=gid).all()
            songgenre = random.choice(songgenreswithgenreid)
            song = session.query(Song).filter_by(songid=songgenre.songid).first()
            if song.songid not in playlist:
                playlist.append(song.songid)


        if choice == 'tempo':
            tempoids = []
            songtempos=session.query(SongTempo).filter_by(songid=songID).all()
            for songtempo in songtempos:
                tempo = session.query(Tempo).filter_by(tempoid=songtempo.tempoid).first()
                tempoids.append(tempo.tempoid)

            tid = random.choice(tempoids)
            songtemposwithtempoid = session.query(SongTempo).filter_by(tempoid=tid).all()
            songtempo = random.choice(songtemposwithtempoid)
            song = session.query(Song).filter_by(songid=songtempo.songid).first()
            if song.songid not in playlist:
                playlist.append(song.songid)


    playlistByTitle = []
    for songid in playlist:
        title = session.query(Song).filter_by(songid=songid).first().songtitle
        playlistByTitle.append(title)
        print title

    save = raw_input("save playlist? (Y/n) ")
    if save == "Y":
        playlistname = raw_input("save as: ")
        newPlaylist = Playlist(name=playlistname)
        session.add(newPlaylist)
        session.commit()

        PlaylistObject = session.query(Playlist).filter_by(name=playlistname).order_by(desc(Playlist.playlistid)).first()
        pid = PlaylistObject.playlistid

        for songid in playlist:
            songToPlaylist = SongPlaylist(songid=songid, playlistid=pid)
            session.add(songToPlaylist)
            session.commit()


def getPlaylist(playlistname):
    try:
        playlist = session.query(Playlist).filter_by(name=playlistname).first()
        pid = playlist.playlistid
    except:
        print 'error: playlist with that name does not exist'
        return

    songplaylists = session.query(SongPlaylist).filter_by(playlistid=pid)

    for songplaylist in songplaylists:
        song = session.query(Song).filter_by(songid=songplaylist.songid).first()
        print song.songtitle


def updatePlaylistName():
    oldplaylistname = raw_input("whats the playlists old name: ")
    playlist = session.query(Playlist).filter_by(name=oldplaylistname).first()

    if not playlist:
        print 'error: playlist does not exist'
        return

    newPlaylistname = raw_input("whats the playlists new name: ")
    playlist.name = newPlaylistname
    session.commit()

def deletePlaylist(playlistname):
    try:
        playlist = session.query(Playlist).filter_by(name=playlistname).first()
        pid = playlist.playlistid
    except:
        print 'error: playlist with that name does not exist'
        return

    session.query(SongPlaylist).filter_by(playlistid=pid).delete()
    session.query(Playlist).filter_by(playlistid=pid).delete()
    session.commit()


def addSongMood(songname, moodname):
    if session.query(Song).filter_by(songtitle=songname).first():
        songID = session.query(Song).filter_by(songtitle=songname).first().songid
        if session.query(Mood).filter_by(name=moodname).first():
            moodID = session.query(Mood).filter_by(name=moodname).first().moodid
            thissongmood = SongMood(songid=songID, moodid=moodID)
            session.add(thissongmood)
            session.commit()
        else:
            print "Mood does not exist"
    else:
        print "Song does not exist"


def addSongTempo(songname, temponame):
     if session.query(Song).filter_by(songtitle=songname).first():
        songID = session.query(Song).filter_by(songtitle=songname).first().songid
        if session.query(Tempo).filter_by(name=temponame).first():
            tempoID = session.query(Tempo).filter_by(name=temponame).first().tempoid
            thissongtempo = SongTempo(songid=songID, tempoid=tempoID)
            session.add(thissongtempo)
            session.commit()
        else:
            print "Tempo does not exist"
     else:
        print "Song does not exist"


def addSongGenre(songname, genrename):
    if session.query(Song).filter_by(songtitle=songname).first():
        songID = session.query(Song).filter_by(songtitle=songname).first().songid
        if session.query(Genre).filter_by(name=genrename).first():
            genreID = session.query(Genre).filter_by(name=genrename).first().genreid
            thissonggenre = SongGenre(songid=songID, genreid=genreID)
            session.add(thissonggenre)
            session.commit()
        else:
            print "Genre does not exist"
    else:
        print "Song does not exist"


def addTempo(newName):  
    if session.query(Tempo).filter_by(name=newName).first():
        print "tempo already exists"
    else: 
        new_tempo = Tempo(name=newName)        
        try:
            session.add(new_tempo)
            session.commit()
            print "Tempo added succesfully" 
            return
        except:     
            print "Server side error" 


def addGenre(newName):  
    if session.query(Genre).filter_by(name=newName).first():
        print "Genre already exists"
    else: 
        new_genre = Genre(name=newName)        
        try:
            session.add(new_genre)
            session.commit()
            print "Genre added succesfully" 
            return
        except:     
            print "Server side error" 


def addMood(newName):  
    if session.query(Mood).filter_by(name=newName).first():
        print "Mood already exists"
    else: 
        new_mood = Mood(name=newName)        
        try:
            session.add(new_mood)
            session.commit()
            print "Mood added succesfully" 
            return
        except:     
            print "Server side error"      

def findArtistAndAddToDB(artistname):   
    # if session.query(Artist).filter_by(Artist) 
    artistData = pygn.search(clientID=clientID, userID=userID, artist=artistname)
    # pprint(artistData) 

    era = artistData.get("artist_era")['1']['TEXT']
    a = Artist(name=artistData.get("album_artist_name"), era=era)
    artistname = artistData.get("album_artist_name")

    artist_object = session.query(Artist).filter_by(name=artistname).first()

    if not artist_object:
        session.add(a)
        session.commit()
        artist_object = session.query(Artist).filter_by(name=artistname).first()


    artistID = artist_object.artistid


    tracks = artistData.get("tracks")
    tracks_with_info = []


    # for track in tracks:
    for track in tracks:
        track_info = pygn.search(clientID=clientID, userID=userID, artist=artistname, track=track['track_title'])
        tracks_with_info.append(track_info)
        album_title = track_info['album_title']
        # if it doesnt work try getting rid of artist id in query
        album = session.query(Album).filter_by(albumtitle=album_title, artistid=artistID).first()

        if not album:
            al = Album(albumtitle=album_title, artistid=artistID)
            session.add(al)
            session.commit()

        albumid = session.query(Album).filter_by(albumtitle=album_title, artistid=artistID).first().albumid
        track_info['albumID'] = albumid



    # for track in tracks:
    for track in tracks_with_info:

        findTrack = session.query(Song).filter_by(songtitle=track['track_title']).first()

        if findTrack:
            continue
        else:
            s = Song(songtitle=track['track_title'], artistid=artistID, albumid=track['albumID'])
            session.add(s)
            session.commit()

        song_object = session.query(Song).filter_by(songtitle=track['track_title']).first()

        for k, mood in track['mood'].iteritems():
            newmood = mood['TEXT']
            mood_object = session.query(Mood).filter_by(name=newmood).first()
            if not mood_object:
                m = Mood(name=newmood)
                session.add(m)
                session.commit

            mood_object = session.query(Mood).filter_by(name=newmood).first()
            sm = SongMood(songid=song_object.songid, moodid=mood_object.moodid)
            session.add(sm)
            session.commit()

        for k, genre in track['genre'].iteritems():
            newgenre = genre['TEXT']
            genre_object = session.query(Genre).filter_by(name=newgenre).first()
            if not genre_object:
                g = Genre(name=newgenre)
                session.add(g)
                session.commit

            genre_object = session.query(Genre).filter_by(name=newgenre).first()
            sg = SongGenre(songid=song_object.songid, genreid=genre_object.genreid)
            session.add(sg)
            session.commit()


        for k, tempo in track['tempo'].iteritems():
            newtempo = tempo['TEXT']
            tempo_object = session.query(Tempo).filter_by(name=newtempo).first()
            if not tempo_object:
                t = Tempo(name=newtempo)
                session.add(t)
                session.commit

            tempo_object = session.query(Tempo).filter_by(name=newtempo).first()
            st = SongTempo(songid=song_object.songid, tempoid=tempo_object.tempoid)
            session.add(st)
            session.commit()








def main():

    while 1:
        print '0) exit'
        print '1) add an artist'
        print '2) add an album'
        print '3) add a song'
        print '4) make a playlist'
        print '5) get a playlist'
        print '6) update playlist name'
        print '7) delete a playlist'
        print '8) search for new artist to add to the DB'

        option = raw_input("option: ")

        if option == "0":
            return

        if option == "1":
            addSingleArtist()

        if option == "2":
            addSingleAlbum()

        if option == "3":
            addSingleSong()

        if option == "4":
            print ''
            song = raw_input("Enter a song name: ")
            length = int(raw_input("Enter playlist length: "))
            print ''
            makePlayList(song=song, length=length)

        if option == "5":
            print ''
            playlistname = raw_input("Enter playlist name: ")
            getPlaylist(playlistname=playlistname)
            print ''

        if option == "6":
            updatePlaylistName()

        if option == "7":
            print ''
            playlistname = raw_input("Enter playlist name: ")
            deletePlaylist(playlistname=playlistname)
            print ''

        if option == "8":
            print ''
            newArtistName = raw_input("Enter new arists name: ")
            findArtistAndAddToDB(newArtistName)
            print ''

        if option == "list artists":
            print ''
            artists = session.query(Artist).all()
            for artist in artists:
                print artist.name

            print ''

        if option == 'list all':
            print ''
            artists = session.query(Artist).all()
            for artist in artists:
                print artist.name
                albums = session.query(Album).filter_by(artistid=artist.artistid)
                for album in albums:
                    print "     {}".format(album.albumtitle)
                    songs = session.query(Song).filter_by(albumid=album.albumid)
                    for song in songs:
                        print "         {}".format(song.songtitle)

        if option == 'list songs':
            print ''
            songs = session.query(Song).all()
            for song in songs:
                print song.songtitle
            print ''

        if option == "song info":
            song = raw_input("Enter a song name: ")
            try:
                song = session.query(Song).filter_by(songtitle=song).first()
                songID = song.songid
            except:
                print 'error song not found in database try a new one'
                continue

            print ''
            print "Title: {}".format(song.songtitle)


            album = session.query(Album).filter_by(albumid=song.albumid).first()
            print "Album: {}".format(album.albumtitle)



            artist = session.query(Artist).filter_by(artistid=song.artistid).first()
            print "Artist: {}".format(artist.name)



            print 'Moods:'
            moods = []
            songmoods=session.query(SongMood).filter_by(songid=song.songid).all()
            for songmood in songmoods:
                mood = session.query(Mood).filter_by(moodid=songmood.moodid).first()
                moods.append(mood.name)
            print moods



            print 'Genres:'
            genres = []
            songgenres=session.query(SongGenre).filter_by(songid=songID).all()
            for songgenre in songgenres:
                genre = session.query(Genre).filter_by(genreid=songgenre.genreid).first()
                genres.append(genre.name)
            print genres



            print 'Tempos:'
            tempos = []
            songtempos=session.query(SongTempo).filter_by(songid=songID).all()
            for songtempo in songtempos:
                tempo = session.query(Tempo).filter_by(tempoid=songtempo.tempoid).first()
                tempos.append(tempo.name)
            print tempos

            print ''

        if option == "list playlists":
            print ''
            playlists = session.query(Playlist).all()
            for playlist in playlists:
                print playlist.name
            print ''

        if option == "list playlists --all":
            print ''
            playlists = session.query(Playlist).all()
            for playlist in playlists:
                print playlist.name
                results = session.query(SongPlaylist).filter_by(playlistid=playlist.playlistid).all()
                for sp in results:
                    print "     {}".format(session.query(Song).filter_by(songid=sp.songid).first().songtitle)
                print ''


            print ''


        if option == "import":
            importArtist()
            importAlbum()
            importSong()  
            importMood()
            importGenre()
            importTempo()
            importSongMood()
            importSongTempo()
            importSongGenre()





if __name__ == '__main__':
  main()


     
            





