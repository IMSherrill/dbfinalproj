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
    ArtistId = Column(Integer, nullable=False, unique=True, primary_key=True)
    ArtistName = Column(String)
    Era = Column(String)

class Album(Base):
    __tablename__ = "Album"
    AlbumId = Column(Integer, primary_key=True)
    AlbumTitle = Column(String)
    ArtistId = Column(Integer, ForeignKey(Artist.ArtistId))
    artist = relationship("Artist", foreign_keys={ArtistId})


class Song(Base):
    __tablename__ = 'Song'
    SongId = Column(Integer, primary_key=True)
    SongTitle = Column(String)
    ArtistId = Column(Integer, ForeignKey(Artist.ArtistId))
    AlbumId = Column(Integer, ForeignKey(Album.AlbumId))

    artist = relationship("Artist", foreign_keys={ArtistId})
    album = relationship("Album", foreign_keys={AlbumId})

class Tempo(Base):
    __tablename__ = "Tempo"
    TempoID = Column(Integer, primary_key=True)
    Tempo = Column(String)

class Mood(Base):
    __tablename__ = "Mood"
    MoodID = Column(Integer, primary_key=True)
    Mood = Column(String)

class Genre(Base):
    __tablename__ = "Genre"
    GenreID = Column(Integer, primary_key=True)
    GenreName = Column(String)

class Playlist(Base):
    __tablename__ = "Playlist"
    PlaylistID = Column(Integer, primary_key=True)
    PlaylistName = Column(String)

class SongGenre(Base):
    __tablename__ = "SongGenre"
    SongGenreID = Column(Integer, primary_key=True)
    SongId = Column(Integer, ForeignKey(Song.SongId))
    GenreID = Column(Integer, ForeignKey(Genre.GenreID))

    song = relationship("Song", foreign_keys={SongId})
    genre = relationship("Genre", foreign_keys={GenreID})

class SongTempo(Base):
    __tablename__ = "SongTempo"
    SongTempoID = Column(Integer, primary_key=True)
    SongId = Column(Integer, ForeignKey(Song.SongId))
    TempoID = Column(Integer, ForeignKey(Tempo.TempoID))

    song = relationship("Song", foreign_keys={SongId})
    tempo = relationship("Tempo", foreign_keys={TempoID})

class SongMood(Base):
    __tablename__ = "SongMood"
    SongMoodID = Column(Integer, primary_key=True)
    SongId = Column(Integer, ForeignKey(Song.SongId))
    MoodID = Column(Integer, ForeignKey(Mood.MoodID))

    song = relationship("Song", foreign_keys={SongId})
    mood = relationship("Mood", foreign_keys={MoodID})

class SongPlaylist(Base):
    __tablename__ = "songplaylist"
    SongPlaylistID = Column(Integer, primary_key=True)
    SongId = Column(Integer, ForeignKey(Song.SongId))
    PlaylistID = Column(Integer, ForeignKey(Playlist.PlaylistID))

    song = relationship("Song", foreign_keys={SongId})
    playlist = relationship("Playlist", foreign_keys={PlaylistID})


Base.metadata.create_all(conn)

def addArtist():
    with open("artist_data_final.json") as datafile:
        data = json.load(datafile)
        pprint(data)
        for artist in data:
            a = Artist(ArtistName=artist.get("name"), Era=artist.get("era"))
            session.add(a)
            session.commit()

def addAlbum():
    with open("album_data_final.json") as datafile:
        data = json.load(datafile)
        for album in data:
            artistInfo = session.query(Artist).filter_by(ArtistName=album['artist']).first()
            artistID = int(artistInfo.ArtistId)
            a = Album(AlbumTitle=album.get("title"), ArtistId=artistID)
            session.add(a)
            session.commit()

def addSong():
    with open("song_data_final.json") as datafile:
        data = json.load(datafile)
        for song in data:
            artistInfo = session.query(Artist).filter_by(ArtistName=song['artist']).first()
            artistID = int(artistInfo.ArtistId)

            albumInfo = session.query(Album).filter_by(AlbumTitle=song['album_title']).first()
            albumID = int(albumInfo.AlbumId)

            s = Song(SongTitle=song['track_title'], ArtistId=artistID, AlbumId=albumID)
            session.add(s)
            session.commit()

def addMood():
    with open("mood_data_final.json") as datafile:
        data = json.load(datafile)
        for mood in data:
            m = Mood(Mood=mood)
            session.add(m)
            session.commit()

def addGenre():
    with open("genre_data_final.json") as datafile:
        data = json.load(datafile)
        for genre in data:
            g = Genre(GenreName=genre)
            session.add(g)
            session.commit()


def addTempo():
    with open("tempo_data_final.json") as datafile:
        data = json.load(datafile)
        for tempo in data:
            t = Tempo(Tempo=tempo)
            session.add(t)
            session.commit()

def addSongMood():
    with open("song_data_final.json") as datafile:
        data = json.load(datafile)

        for song in data:
            songInfo = session.query(Song).filter_by(SongTitle=song['track_title']).first()
            songID = int(songInfo.SongId)

            for mood in song['mood'].values():
                m = mood['TEXT']

                moodInfo = session.query(Mood).filter_by(Mood=m).first()
                moodID = int(moodInfo.MoodID)

                x = SongMood(SongId=songID , MoodID=moodID)
                session.add(x)
                session.commit()



def addSongTempo():
    with open("song_data_final.json") as datafile:
        data = json.load(datafile)

        for song in data:
            songInfo = session.query(Song).filter_by(SongTitle=song['track_title']).first()
            songID = int(songInfo.SongId)

            for tempo in song['tempo'].values():
                t = tempo['TEXT']

                tempoInfo = session.query(Tempo).filter_by(Tempo=t).first()
                tempoID = int(tempoInfo.TempoID)

                x = SongTempo(SongId=songID , TempoID=tempoID)
                session.add(x)
                session.commit()

def addSongGenre():
    with open("song_data_final.json") as datafile:
        data = json.load(datafile)

        for song in data:
            songInfo = session.query(Song).filter_by(SongTitle=song['track_title']).first()
            songID = int(songInfo.SongId)

            for genre in song['genre'].values():
                g = genre['TEXT']

                genreInfo = session.query(Genre).filter_by(GenreName=g).first()
                genreID = int(genreInfo.GenreID)

                x = SongGenre(SongId=songID , GenreID=genreID)
                session.add(x)
                session.commit()


     
            


# addArtist()
# addAlbum()
# addSong()
# addMood()
# addGenre()
# addTempo()
# addSongMood()
# addSongTempo()
# addSongGenre()
