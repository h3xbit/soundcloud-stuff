import soundcloud

client = soundcloud.Client(client_id=open("client-key-in-here","r").read())

class User:
    def __init__(self,permalink):
       self.user = client.get("/resolve",url="http://www.soundcloud.com/"+permalink)
       #print(self.user.keys())
    
    def printSummary(self):
       # total = self.user.followings_count+self.user.followers_count
        followings = float(self.user.followings_count)
        followers = float(self.user.followers_count)
        total = followers+followings
        
        followingsPercent = int(followings/total*100)
        followersPercent = int(followers/total*100)
        print "\n============USER======================"
        print "User      :",self.user.username
        #print "followings:followers :",followingsPercent,":",followersPercent
        print "Following :",followings
        print "Followers :",followers
        print "Tracks    :",self.user.track_count
        #print "======================================"
        
    def getFullList(self,endPoint):
        page_size = 200
        tracks = []
        
        endPointFull = "/users/"+str(self.user.id)+endPoint
        offset = 0
        pageNumber = 0
        
        while 1:
            page = client.get(endPointFull,
                                limit=page_size,
                                linked_partitioning=pageNumber,
                                offset=offset)
            
            trackList = page.collection
            tracks.extend(trackList)
            #print pageNumber,offset
            
            if("next_href" in page.fields()):
                nextLink = page.next_href.split("&")
                pageNumber = nextLink[2].split("=")[1]
                offset = nextLink[3].split("=")[1]
            else:
                break

        return tracks

    def printGenreStats(self):
        print(len(self.getLikes()))
        
    def getFirstTrack(self):
        tracks = self.getFullList("/tracks")
        firstTrackPermaLink = tracks[-1]["permalink_url"]
        return Track(firstTrackPermaLink)

class Track:
    def __init__(self,permalink):
        self.track = client.get("/resolve",url=permalink)
    def printSummary(self,detailed):
        print "\n===============TRACK================="
        #followings = self.user.followings_count
        #followers = self.user.followers_count
       # total = followers+followings
        
       #followingsPercent = int(followings/total*100)
       # followersPercent = int(followers/total*100)
        print "Artist: ",self.track.user["username"] 
        print "Title : ",self.track.title
        print "Plays : ",self.track.playback_count
        print "Faves : ",self.track.favoritings_count
        if(detailed):
            print "Url   : ",self.track.permalink_url
            print "Date of creation: ",self.track.created_at
            
        #print "followings:followers :",followingsPercent,":",followersPercent
      #  print "Following            :",followings
      #  print "Followers            :",followers
      #  print "Tracks               :",self.user.track_count
      #  print "======================================"
        
unames = ["c0zmic","skrillex","nero","seamlessr","subsoundproductions","drumstep"]


    
#print("tracks: ",tracks)

def printFirstTracks(unames):
    for uname in unames:
        user = User(uname)
        #user.printSummary()
        firstTrack = user.getFirstTrack()
        firstTrack.printSummary(True)    

#def genre