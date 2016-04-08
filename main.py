__author__ = 'Robert'

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from pprint import pprint
import json
import random




# Connection settings
settings = {
    'userName': 'root',           # The name of the MySQL account to use (or empty for anonymous)
    'password': '',           # The password for the MySQL account (or empty for anonymous)
    'serverName': "localhost",    # The name of the computer running MySQL
    'portNumber': 3306,           # The port of the MySQL server (default is 3306)from sqlalchemy import create_engine
    'dbName': "final",             # The name of the database we are testing with (this default is installed with MySQL)
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


def makePlayList(song):
    song = session.query(Song).filter_by(songtitle=song).first()
    songID = song.songid

    choices = ['mood', 'genre', 'tempo']
    playlist = []

    # while len(playlist) < 3:
    # choice=random.choice(choices)
    choice = 'mood'
    if choice == 'mood':
        songmoods=session.query(SongMood).filter_by(songid=songID).all()
        for songmood in songmoods:
            mood = session.query(Mood).filter_by(moodid=songmood.moodid).first()
            print mood.name


    if choice == 'genre':
        pass
    if choice == 'tempo':
        pass


    # TODO: theres gotta be a better way to do this part
    # moodid = session.query(SongMood).filter_by(songid=song.songid).first().moodid
    # moods = session.query(Mood).filter_by(moodid=moodid).first().Mood
    # print mood





     
            


# importArtist()
# importAlbum()
# importSong()
# importMood()
# importGenre()
# importTempo()
# importSongMood()
# importSongTempo()
# importSongGenre()
makePlayList(song="Dancing Queen")


