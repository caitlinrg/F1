import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

driversdf = pd.read_csv('drivers.csv')
constructorsdf = pd.read_csv("constructors.csv")
resultsdf = pd.read_csv("results.csv")
racesdf = pd.read_csv("races.csv")

#Points dictionary
points = {1:25, 2:18, 3:15, 4:12, 5:10, 6:8, 7:6, 8:4, 9:2, 10:1, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0}

#constructors dictionary
constructorsdict = dict(zip(constructorsdf['constructorId'], constructorsdf['name'])) 

#drivers dictionary
driversdict  = dict(zip(driversdf['driverId'], driversdf['surname'])) 

#Collect data lines per year
def raceperyear(racesdf, year): 
    races23 = racesdf.loc[racesdf["year"] == year]
    return races23

#Collect race ID's
def collectids(races): 
    raceid = []
    for line in races.index:
        raceid.append(races["raceId"][line])
    return raceid

#Create Calendar for F1 races _________________________________________________

#Collect results for all races in 2023
def results23(races, resultsdf, year): 
    races = raceperyear(races, year)
    raceids = collectids(races)

    raceres = resultsdf.loc[resultsdf["raceId"].isin(raceids)]
    return raceres

#Calculate final standings constructors championships
def constructorschamp(results23):
    constructors = {}
    for index in results23.index: 

        #Try & catch to filter out all DNF, pass for DNF
        try: 
            construct = str(results23["constructorId"][index])
            res = int(results23["position"][index])
            constructor = constructorsdict[int(construct)]

            if constructor in constructors: 
                constructors[constructor] = constructors[constructor] + points[res]
            else: 
                constructors[constructor] = points[res]

        except ValueError:
            pass   

    return dict(sorted(constructors.items(), key=lambda item: item[1], reverse=True))

def driverschamp(results23): 
    drivers = {}
    for index in results23.index: 

        #Try & catch to filter out all DNF, pass for DNF
        try: 
            driver = str(results23["driverId"][index])
            res = int(results23["position"][index])
            winner = driversdict[int(driver)]

            if winner in drivers: 
                drivers[winner] = drivers[winner] + points[res]
            else: 
                drivers[winner] = points[res]

        except ValueError:
            pass   

    return dict(sorted(drivers.items(), key=lambda item: item[1], reverse=True))



def main():
    res23 = results23(racesdf, resultsdf, 2018)
    const = constructorschamp(res23)
    plt.bar(const.keys(), const.values())
    plt.xticks(rotation=90)
    plt.show() 

    c = driverschamp(res23)
    plt.bar(c.keys(), c.values())
    plt.xticks(rotation=90)
    plt.show()

main()