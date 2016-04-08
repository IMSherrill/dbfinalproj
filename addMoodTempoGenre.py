def newTempo(newName):  
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

def newGenre(newName):  
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

def newMood(newName):  
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