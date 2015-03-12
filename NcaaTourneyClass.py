class NcaaGame(object):
    def __init__(self):
        self.region = None
        self.team1 = None
        self.team2 = None
        self.result = {}
        self.before1 = None
        self.before2 = None
        self.after = None
        self.seed1 = None
        self.seed2 = None
        self.winner= None
        self.points = None
        self.bonus = 0
    
    def setBonus(self, bonus):
        self.bonus = bonus
    def getBonus(self):
        return self.bonus    
    def setTeam1(self, team):
        self.team1 = team
    def setTeam2(self, team):
        self.team2 = team
    
    def setSeeds(self,seed1, seed2):
        self.seed1 = seed1
        self.seed2 = seed2
    def setSeed1(self, seed1):
        self.seed1 = seed1
    def setSeed2(self, seed2):
        self.seed2 = seed2 
    def setAfter(self, after):
        self.after = after
    def setBefore(self,before1, before2):
        self.before1 = before1
        self.before2 = before2
    def setResult(self, team, score):
        self.result[team] = score
    def setWinner(self, team):
        self.winner = team
    def setPoints(self, points):
        self.points = points
    def getWinner(self):
        return self.winner
    def getBefore1(self):
        return self.before1
    def getBefore2(self):
        return self.before2
    def getAfter(self):
        return self.after
    def getSeed1(self):
        return self.seed1
    def getSeed2(self):
        return self.seed2
    def getTeam2(self):
        return self.team2
    def getTeam1(self):
        return self.team1
        
    def getData(self):
        print 'team1: ' + str(self.team1) + '\n' +'team2: ' + str(self.team2) +\
        '\n' +'result: ' + str(self.result) + '\n'+ 'winner: '+ str(self.winner)+\
        '\n' + 'seed1: ' + str(self.seed1) + '\n' + 'seed2: ' + str(self.seed2) +\
        '\n' + 'points: ' + str(self.points) + '\n' + 'Bonus: ' + str(self.bonus)
        
class NcaaTournament(object):
    def __init__(self, teams, points = [1,2,4,8,10,20]):
        self.games = [NcaaGame() for i in range(63)]
        self.owner = None
        
        seeds = [1,16,8,9,5,12,4,13,6,11,3,14,7,10, 2,15]
        s = 0
        for i in range(32):
            s = s%15
            self.games[i].setSeeds(seeds[s], seeds[s+1])
            self.games[i].setPoints(points[0])
            s += 2
            if i%2 == 0:
                self.games[i].setAfter(self.games[i+32])
            else:
                self.games[i].setAfter(self.games[i+31])
           
        for i in range(32, 48):
            
            self.games[i].setBefore(self.games[i-32], self.games[i-31])
            self.games[i].setPoints(points[1])
            
            if i%2 == 0:
                self.games[i].setAfter(self.games[i+16])
            else:
                self.games[i].setAfter(self.games[i+15])
            
        
        for i in range(48, 56):
            self.games[i].setBefore(self.games[i-16], self.games[i-15])
            self.games[i].setPoints(points[2])
            
            if i%2 == 0:
                self.games[i].setAfter(self.games[i+8])
            else:
                self.games[i].setAfter(self.games[i+7])
        
        for i in range(56,60):
            self.games[i].setBefore(self.games[i-8], self.games[i-7])
            self.games[i].setPoints(points[3])
            
            if i%2 == 0:
                self.games[i].setAfter(self.games[i+4])
            else:
                self.games[i].setAfter(self.games[i+3])
            
        for i in range(60, 62):
            self.games[i].setBefore(self.games[i-4], self.games[i-3])
            self.games[i].setPoints(points[4])
            
            if i%2 == 0:
                self.games[i].setAfter(self.games[i+2])
            else:
                self.games[i].setAfter(self.games[i+1])
        
        self.games[62].setBefore(self.games[60], self.games[61])
        self.games[62].setPoints(points[5])
        
        n = 0
        for i in range(32):
           self.games[i].setTeam1(teams[n])
           self.games[i].setTeam2(teams[n+1])
           n += 2
           
    
            
        
class mainTournament(NcaaTournament):
        
             
    def updateGame(self, gameNum, team1, team1score, team2, team2score):
        if team1 != self.games[gameNum].team1 and team1 != self.games[gameNum].team2:
            return "Team 1 is not a valid team for GameID"
        if team2 != self.games[gameNum].team1 and team2 != self.games[gameNum].team2:
            return "Team 2 is not a valid team for GameID"
        
        
        self.games[gameNum].setResult(team2, team2score)
        self.games[gameNum].setResult(team1, team1score)
        
        if team1 == self.games[gameNum].getTeam2():
            temp = team1
            team1 = team2
            team2 = temp
            temp1 = team1score
            team1score = team2score
            team2score = temp1
        
        aftGame = self.games[gameNum].getAfter()
        seed = self.games[gameNum].getSeed2()
        
        if team1score > team2score:
            winner = team1
            
            seed = self.games[gameNum].getSeed1()
            
            self.games[gameNum].setBonus(max(0, seed - self.games[gameNum].getSeed2()))
            
        else:
            winner = team2
            self.games[gameNum].setBonus(max(0, seed - self.games[gameNum].getSeed1()))
            
            
        self.games[gameNum].setWinner(winner)
        
        if self.games[gameNum] == aftGame.getBefore1():
            aftGame.setTeam1(winner)
            aftGame.setSeed1(seed)
        else:
            aftGame.setTeam2(winner)
            aftGame.setSeed2(seed)

class TournamentEntry(NcaaTournament):
    def setOwner(self, Owner):
        self.owner = Owner
        
    def addPicks(self, picks):
        
        for i in range(len(self.games)):
            self.games[i].setWinner(picks[i])
            
        for i in range(32, 63):
            
            self.games[i].setTeam1(self.games[i].getBefore1().getWinner())
            self.games[i].setTeam2(self.games[i].getBefore2().getWinner())
            
            if self.games[i].getTeam1() == self.games[i].getBefore1().getTeam1():
                self.games[i].setSeed1(self.games[i].getBefore1().getSeed1())
            else:
                self.games[i].setSeed1(self.games[i].getBefore1().getSeed2())
            
            if self.games[i].getTeam2() == self.games[i].getBefore2().getTeam1():
                self.games[i].setSeed2(self.games[i].getBefore2().getSeed1())
            else:
                self.games[i].setSeed2(self.games[i].getBefore2().getSeed2())