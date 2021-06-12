class AnimeEntry(object):

    def __init__(self, name, id, globalranking, picture, status, score):

        self.name = name
        self.id = id
        self.globalranking = globalranking
        self.picture = picture
        self.status = status
        self.score = score

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def getGlobalRanking(self):
        return self.globalranking

    def getPicture(self):
        return self.picture

    def getStatus(self):
        return self.status

    def getScore(self):
        return self.score

    def setName(self, name):
        self.name = name

    def setId(self, id):
        self.id = id

    def setGlobalRanking(self, ranking):
        self.globalranking = ranking

    def setPicture(self, picture):
        self.picture = picture

    def setStatus(self, status):
        self.status = status

    def setScore(self, score):
        self.score = score



    


