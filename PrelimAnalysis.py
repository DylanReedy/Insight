import seedDataFetch
import numpy as numpy
import pandas
import scipy.stats as stats
import matplotlib.pyplot as pl

#seedDataFetch.FetchDataFromRiotS3()
#seedDataFetch.WriteRiotDataToFile('projectData.txt')

data = seedDataFetch.GetRiotData('test.txt')

rawDataFrame = pandas.DataFrame(data)

totalGames = 0
bins = numpy.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5,15.0])
wins = numpy.zeros([1,len(bins)])
totals = numpy.zeros([1,len(bins)])
count = 0
notSupport = 0

firstDragon = numpy.array([[1],[2]])
firstBaron = numpy.array([[1],[2]])
firstBlood = numpy.array([[1],[2]])
firstInhibitor = numpy.array([[1],[2]])
firstTower = numpy.array([[1],[2]])

for x in range(0,len(rawDataFrame.index)):
    for y in range(0,len(rawDataFrame.at[x,'matches'])):
        win = 'Win'
        csDeltaAt10 = 0
        for z in range(0,int(len(rawDataFrame.at[x,'matches'][y]['participants'])/2)):
            if rawDataFrame.at[x,'matches'][y]['participants'][z]['timeline']['role']!='DUO_SUPPORT':
                notSupport += 1
            if rawDataFrame.at[x,'matches'][y]['participants'][z]['teamId'] == rawDataFrame.at[x,'matches'][y]['teams'][0]['teamId']:
                win = rawDataFrame.at[x,'matches'][y]['teams'][0]['win']
            else:
                win = rawDataFrame.at[x,'matches'][y]['teams'][1]['win']
            if win == 'Win' and 'csDiffPerMinDeltas' in rawDataFrame.at[x,'matches'][y]['participants'][z]['timeline'].keys(): 
                if rawDataFrame.at[x,'matches'][y]['participants'][z]['timeline']['csDiffPerMinDeltas']['0-10'] > 0:
                    csBin = numpy.digitize(rawDataFrame.at[x,'matches'][y]['participants'][z]['timeline']['csDiffPerMinDeltas']['0-10'], bins)
                    wins[0,csBin] += 1
                    totals[0,csBin] += 1
                else:
                    csBin = numpy.digitize(abs(rawDataFrame.at[x,'matches'][y]['participants'][z]['timeline']['csDiffPerMinDeltas']['0-10']), bins)
                    totals[0,csBin] += 1        
                    count += 1
        totalGames += 1
        if(rawDataFrame.at[x,'matches'][y]['teams'][0]['win'] == 'Win'):
            if(rawDataFrame.at[x,'matches'][y]['teams'][0]['firstDragon']):
                firstDragon[0] = firstDragon[0] + 1
            if(rawDataFrame.at[x,'matches'][y]['teams'][1]['firstDragon']):
                firstDragon[1] = firstDragon[1] + 1
    
            if(rawDataFrame.at[x,'matches'][y]['teams'][0]['firstBaron']):
                firstBaron[0] = firstBaron[0] + 1
            if(rawDataFrame.at[x,'matches'][y]['teams'][1]['firstBaron']):
                firstBaron[1] = firstBaron[1] + 1
                    
            if(rawDataFrame.at[x,'matches'][y]['teams'][0]['firstBlood']):
                firstBlood[0] = firstBlood[0] + 1
            if(rawDataFrame.at[x,'matches'][y]['teams'][1]['firstBlood']):
                firstBlood[1] = firstBlood[1] + 1
                    
            if(rawDataFrame.at[x,'matches'][y]['teams'][0]['firstInhibitor']):
                firstInhibitor[0] = firstInhibitor[0] + 1
            if(rawDataFrame.at[x,'matches'][y]['teams'][1]['firstInhibitor']):
                firstInhibitor[1] = firstInhibitor[1] + 1
                
            if(rawDataFrame.at[x,'matches'][y]['teams'][0]['firstTower']):
                firstTower[0] = firstTower[0] + 1
            if(rawDataFrame.at[x,'matches'][y]['teams'][1]['firstTower']):
                firstTower[1] = firstTower[1] + 1


dragonHalf = (firstDragon[0] + firstDragon[1])/2
dragChi2, dragp = stats.chisquare(firstDragon,f_exp=[dragonHalf,dragonHalf])

baronHalf = (firstBaron[0] + firstBaron[1])/2
baronChi2, baronp = stats.chisquare(firstBaron,f_exp=[baronHalf,baronHalf])

bloodHalf = (firstBlood[0] + firstBlood[1])/2
bloodChi2, bloodp = stats.chisquare(firstBlood,f_exp=[bloodHalf,bloodHalf])

inhibHalf = (firstInhibitor[0] + firstInhibitor[1])/2
inhibChi2, inhibp= stats.chisquare(firstInhibitor,f_exp=[inhibHalf,inhibHalf])

towerHalf = (firstTower[0] + firstTower[1])/2
towerChi2, towerp= stats.chisquare(firstTower,f_exp=[towerHalf,towerHalf])


# =============================================================================
# Plot Chi-Squared for each of the "first" objectives
# =============================================================================

#y = [bloodChi2,towerChi2,baronChi2,dragChi2,inhibChi2]
#yMax = 0
#for x in range(0,len(y)):
#    if y[x] > yMax:
#        yMax = y[x]        
#
#x=[1,2,3,4,5]
#xticks=['Kill', 'Tower', 'Baron', 'Dragon', 'Inhibitor']
#pl.xlim(0.5,5.5)
#pl.ylim(10,yMax+10)
#pl.plot(x,y, 'bo')
#pl.xticks(x,xticks)
#pl.ylabel("Chi-squared", size=15)
#pl.xlabel("First Objective Secured", size=15)
#pl.title("Game First Objectives Relevance", size=20)

# =============================================================================
# Plot Chi-Squared again, omit inhibitors
# =============================================================================

#y = [bloodChi2,towerChi2,baronChi2,dragChi2]
#yMax = 0
#for x in range(0,len(y)-1):
#    if y[x] > yMax:
#        yMax = y[x]        
#
#x=[1,2,3,4]
#xticks=['Kill', 'Tower', 'Baron', 'Dragon']
#pl.xlim(0.5,4.5)
#pl.ylim(10,yMax+10)
#pl.plot(x,y, 'bo')
#pl.xticks(x,xticks)
#pl.ylabel("Chi-squared", size=15)
#pl.xlabel("First Objective Secured", size=15)
#pl.title("Game First Objectives Relevance", size=20)

# =============================================================================
# Plot win percentage as a function of CS Delta
# =============================================================================

winPercentage = numpy.divide(wins,totals)
winError = numpy.divide(numpy.sqrt(wins),totals)

bins = numpy.reshape(bins, winPercentage.shape)
bins = bins.reshape((10,))
winPercentage = winPercentage.reshape((10,))
winError = winError.reshape((10,))
 

slope, intercept, r_value, p_value, std_err = stats.linregress(bins[:8],y=winPercentage[:8])
pl.xlim(0,5)
pl.ylim(0.3,1)
pl.errorbar(bins,winPercentage,xerr=0,yerr=winError,fmt='bo', label = 'Data')
r2 = round((r_value*r_value),3)
pl.ylabel("Win %", size=15)
pl.xlabel("CreepScore/min $\Delta$, < 10 minutes", size=15)
pl.plot(bins,bins*slope + intercept, 'r', label = 'Fit (r^2 = ' + str(r2) + ')')
pl.legend()
pl.title('Win Percentage vs. CreepScore/Min Deltas', size=20)
pl.show()