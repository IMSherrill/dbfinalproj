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
    'userName': 'rshanholtz',           # The name of the MySQL account to use (or empty for anonymous)
    'password': 'blackbelt95',           # The password for the MySQL account (or empty for anonymous)
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

