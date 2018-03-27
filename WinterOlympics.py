import os
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
yearlist = [1924, 1928, 1932, 1936, 1948, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1994, 1998, 2002, 2006, 2010, 2014, 2018]
sportlist = ["Biathlon", "Bobsleigh", "Cross-country skiing", "Figure skating", "Freestyle skiing", "Luge", "Nordic combined", "Skeleton", "Ski jumping", "Snowboarding", "Speed skating"]


def ReadMedallistData(year, country):

    combinedMedalistData=defaultdict(list)
    country = country.replace(' ', '_')
    try:
        m="https://en.wikipedia.org/wiki/"+country+"_at_the_"+str(year)+"_Winter_Olympics"

        f2=urlopen(m)
        lines2=f2.read()
        lines2=lines2.decode('utf-8')
        soup=BeautifulSoup(lines2,'html.parser')
        
        table=soup.find_all("table",class_="wikitable sortable")[0]
        rows=table.find_all('tr')

        for row in rows[1:]:
            cells=row.find_all('td')
            if(cells[0].find_all("img",src="//upload.wikimedia.org/wikipedia/commons/thumb/4/47/Gold_medal_icon.svg/16px-Gold_medal_icon.svg.png")):
                namesOfAthletes=[]
                for names in cells[1].find_all("a"):
                    namesOfAthletes.append(names.get('title'))
                combinedMedalistData['GoldMedalists'].append([namesOfAthletes]+[cells[2].a.string]+[cells[3].string])
            if(cells[0].find_all("img",src="//upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Silver_medal_icon.svg/16px-Silver_medal_icon.svg.png")):
                namesOfAthletes=[]
                for names in cells[1].find_all("a"):
                    namesOfAthletes.append(names.get('title'))
                combinedMedalistData['SilverMedalists'].append([namesOfAthletes]+[cells[2].a.string]+[cells[3].string])
            if(cells[0].find_all("img",src="//upload.wikimedia.org/wikipedia/commons/thumb/8/89/Bronze_medal_icon.svg/16px-Bronze_medal_icon.svg.png")):
                namesOfAthletes=[]
                for names in cells[1].find_all("a"):
                    namesOfAthletes.append(names.get('title'))
                combinedMedalistData['BronzeMedalists'].append([namesOfAthletes]+[cells[2].a.string]+[cells[3].string])
    except:
        pass
    return combinedMedalistData
 
def getNumberOfGSB(year, sport, country):
    combinedMedalistsData = ReadMedallistData(year, country)
    numGold = 0
    numSilver = 0
    numBronze = 0
    
    if(len(combinedMedalistsData['GoldMedalists'])):
        for event in combinedMedalistsData['GoldMedalists']:
                if(event[1]==sport):
                    numGold=numGold+1
    if(len(combinedMedalistsData['SilverMedalists'])):
        for event in combinedMedalistsData['SilverMedalists']:
                if(event[1]==sport):
                    numSilver=numSilver+1
    if(len(combinedMedalistsData['BronzeMedalists'])):
        for event in combinedMedalistsData['BronzeMedalists']:
                if(event[1]==sport):
                    numBronze=numBronze+1

    medallist = [numGold, numSilver, numBronze]
    return medallist

def readyearfile(year):
	combinedList = []
	
	os.chdir("./HTML Files/OlympicsByYear")
	try:
		f = open(str(year)+" Winter Olympics medal table.html", encoding='utf-8')
		lines = f.read()
		f.close()
		m=re.findall('Host \w+\s\([\w\s]+?\).+?Total\s+\(\d+\sNOCs\)', lines, re.DOTALL)
		if m:
			countrylist = re.findall('\"([\w\s]+)\s+at the '+str(year)+' Winter Olympics', m[0])
			#print(countrylist)
			medals = re.findall('\">\(\w\w\w\)</span>.+\n<td>(\d+)</td>\n<td>(\d+)</td>\n<td>(\d+)</td>\n<td>(\d+)</td>', m[0])
			#print(medals)
		combinedList = [countrylist]+[medals]
	except:
		pass
	os.chdir("../..")
	return combinedList
    

def readsportfile(sport):
    """to get gold silver bronze medal by a country in a year"""
    combinedData = []
    os.chdir("./HTML Files/OlympicsBySport")
	
    f = open(sport+" at the Winter Olympics.html", encoding='utf-8')
    lines = f.read()
    f.close()
    m=re.findall('Medal table\"(.+)colspan=\"2\">Total', lines, re.DOTALL)
    if m:
        countrylist = re.findall('\"([\w\s]+)\s+at the Olympics', m[0])
        print(countrylist)
        print(countrylist[0])
        medals = re.findall('">\(\w\w\w\)</span>\*?</td>\s+<td>(\d+)</td>\n<td>(\d+)</td>\n<td>(\d+)</td>\n<td>(\d+)</td>', m[0])
        print(medals)
    combinedData = [countrylist]+[medals]
    os.chdir("../..")
    return combinedData

def totalParticipantsFromCountry(year,country):
    #print("Comes here")

    total=0
    count=0
    for x in sportlist:
        #print(x)
        grandList = numAthletesFromNation(x)
        try:
            index1 = grandList[0].index(country)
            index2 = grandList[2].index(year)
            try:
                count = int(grandList[1][index1][index2])
            except:
                pass
        except:
            pass
        
        total=total+count
            
        #print(total)

    return total

def numAthletesFromNation(sport):
    combinedNumAthletes = []
    
    os.chdir("./HTML Files/OlympicsBySport")
    namesOfCountries=[]
    year_list1=[]
    year_list2=[]
    year_list=[]
    f=open(sport+' at the Winter Olympics.html',encoding='utf-8')
    lines = f.read()
    f.close()
    os.chdir("../..")
    #print(lines)
    soup=BeautifulSoup(lines,'html.parser')
    #print(soup)
    if(sport=='Figure skating'):
        table=soup.find_all("table",class_="wikitable")[2]
    if(sport=='Biathlon'):
        table=soup.find_all("table",class_="wikitable")[4]
    if(sport=='Bobsleigh'):
        table=soup.find_all("table",class_="wikitable")[4]
    if(sport=='Cross-country skiing'):
        table=soup.find_all("table",class_="wikitable")[3]
    if(sport=='Freestyle skiing'):
        table=soup.find_all("table",class_="wikitable")[3]
    if(sport=='Luge'):
        table=soup.find_all("table",class_="wikitable")[3]   
    if(sport=='Nordic combined'):
        table=soup.find_all("table",class_="wikitable")[2]
    if(sport=='Skeleton'):
        table=soup.find_all("table",class_="wikitable")[2]
    if(sport=='Ski jumping'):
        table=soup.find_all("table",class_="wikitable")[2]
    if(sport=='Snowboarding'):
        table=soup.find_all("table",class_="wikitable")[3] 
    if(sport=='Speed skating'):
        table=soup.find_all("table",class_="wikitable")[3]        
    rows=table.find_all("tr")
    #print(rows)
    i=1
    cells=rows[0].find_all('th')

    while(int(cells[i].get_text())>6):
        year_list1.append(int(cells[i].get_text()))
        i=i+1
    year_list1=[x+1900 for x in year_list1]    
    while(int(cells[i].get_text())<18):
        year_list2.append(int(cells[i].get_text()))
        i=i+1
    year_list2.append(int(cells[i].get_text()))    
    year_list2=[x+2000 for x in year_list2]    
    
    year_list=year_list1+year_list2
    #print(year_list)
    
    if(sport=='Skeleton'):
        year_listneg=[1924,1932,1936,1952,1956,1960,1964,1968,1972,1976,1980,1984,1988,1992,1994,1998]
        year_list=[x for x in year_list if x not in year_listneg]

    
    for row in rows[1:-3]:
        try:
            cells=row.find_all('td')
            namesOfCountries=namesOfCountries+[cells[0].a.string]
        except:
            pass
    #print(namesOfCountries) 

    j=0
    numOfAthletes=[[] for x in range(len(namesOfCountries))]
    for row in rows[1:-3]:
        try:
            cells=row.find_all('td')
            for cell in cells[1:-1]:
                this=cell.get_text()
                this = this.replace(u'\xa0', u' ')
                numOfAthletes[j].append(this)
            combinedNumAthletes.append(numOfAthletes[j])    
            j=j+1
        except:
            pass
        
    
    try:
        if(sport=='Skeleton'):
            i=0
            while(i<len(combinedNumAthletes)):
                    #print(combinedNumAthletes)
                    del combinedNumAthletes[i][0]
                    del combinedNumAthletes[i][1]
                    del combinedNumAthletes[i][2]
                    i=i+1
    except:
        pass
    
        
    numAthletesFromNationList=[namesOfCountries]+[combinedNumAthletes]+[year_list] 
    #print(numAthletesFromNationList)
    return(numAthletesFromNationList)

		
def findHost(year):
    hostname = []
    try:
        os.chdir("./HTML Files/OlympicsByYear")
	
        f = open(str(year)+" Winter Olympics medal table.html", encoding='utf-8')
        lines = f.read()
        f.close()
        m=re.findall('Host nation (\([\w+\s]+\))', lines)
        if(not m):
            m=re.findall('Host country (\([\w+\s]+\))',lines)
        
        hostname = m[0]
    except:
        pass
    os.chdir("../..")
    return(hostname)
    
def total_athletes_from_all_nations(sport):
    os.chdir("./HTML Files/OlympicsBySport")
    year_list1=[]
    year_list2=[]
    year_list=[]
    f=open(sport+' at the Winter Olympics.html',encoding='utf-8')
    lines = f.read()
    f.close()
    os.chdir("../..")
    #print(lines)
    soup=BeautifulSoup(lines,'html.parser')
    #print(soup)
    if(sport=='Figure skating'):
        table=soup.find_all("table",class_="wikitable")[2]
    if(sport=='Biathlon'):
        table=soup.find_all("table",class_="wikitable")[4]
    if(sport=='Bobsleigh'):
        table=soup.find_all("table",class_="wikitable")[4]
    if(sport=='Cross-country skiing'):
        table=soup.find_all("table",class_="wikitable")[3]
    if(sport=='Freestyle skiing'):
        table=soup.find_all("table",class_="wikitable")[3]
    if(sport=='Luge'):
        table=soup.find_all("table",class_="wikitable")[3]   
    if(sport=='Nordic combined'):
        table=soup.find_all("table",class_="wikitable")[2]
    if(sport=='Skeleton'):
        table=soup.find_all("table",class_="wikitable")[2]
    if(sport=='Ski jumping'):
        table=soup.find_all("table",class_="wikitable")[2]
    if(sport=='Snowboarding'):
        table=soup.find_all("table",class_="wikitable")[3] 
    if(sport=='Speed skating'):
        table=soup.find_all("table",class_="wikitable")[3]        
    rows=table.find_all("tr")
    #print(rows)
    i=1
    cells=rows[0].find_all('th')

    while(int(cells[i].get_text())>6):
        year_list1.append(int(cells[i].get_text()))
        i=i+1
    year_list1=[x+1900 for x in year_list1]    
    while(int(cells[i].get_text())<18):
        year_list2.append(int(cells[i].get_text()))
        i=i+1
    year_list2.append(int(cells[i].get_text()))  
    year_list2=[x+2000 for x in year_list2]    
    
    year_list=year_list1+year_list2
    #print(year_list)
    
    if(sport=='Skeleton'):
        year_listneg=[1924,1932,1936,1952,1956,1960,1964,1968,1972,1976,1980,1984,1988,1992,1994,1998]
        year_list=[x for x in year_list if x not in year_listneg]

    
    totalnumOfAthletes=[]
    totalnumOfNations=[]
    
    if(sport=="Figure skating"):
        i=0
        try:
            cells=rows[-3].find_all('td')
            while(int(cells[i].get_text())):
                totalnumOfAthletes.append(cells[i].get_text())
                i=i+1
            totalnumOfAthletes=totalnumOfAthletes[2:]
        except:
            pass 

        i=0
        cells=rows[-2].find_all('td')
        try:
            while(int(cells[i].get_text())):
                totalnumOfNations.append(int(cells[i].get_text()))
                i=i+1
            totalnumOfNations=totalnumOfNations[2:]    
        except:
            pass
        
        try:
            year_list=year_list[2:]
        except:
            pass
    
    elif(sport=='Skeleton'):
        i=2
        cells=rows[-2].find_all('th')
        
        while(i<len(year_list)+4):
            try:
                this=cells[i].get_text()
                totalnumOfAthletes.append(this)
                i=i+1
            except:
                pass
        totalnumOfAthletes=[x for x in totalnumOfAthletes if x!='']    

        i=2 
        cells=rows[-3].find_all('th')
        while(i<len(year_list)+4):
            try:
                this=cells[i].get_text()
                totalnumOfNations.append(this)
                i=i+1
            except:
                pass
        
        totalnumOfNations=[x for x in totalnumOfNations if x!=''] 
    

                
    else:
        i=1
        cells=rows[-2].find_all('th')
        try:
            while(cells[i].get_text()):
                this=cells[i].get_text()
                totalnumOfAthletes.append(this)
                i=i+1
        except:
            pass


        i=1 
        cells=rows[-3].find_all('th')
        try:
            while(cells[i].get_text()):
                this=cells[i].get_text()
                totalnumOfNations.append(this)
                i=i+1
        except:
            pass         
    
    totalnumAthletesFromNationList=[totalnumOfNations]+[totalnumOfAthletes]+[year_list]
    return(totalnumAthletesFromNationList)


def highestMedalWinningCountry(sport, year):
    countryList = []
    highestMedalWinner = ""
    sport = sport.replace(' ','_')
    try:
        f2 = urlopen('https://en.wikipedia.org/wiki/'+sport+'_at_the_'+str(year)+'_Winter_Olympics')
        lines=f2.read()
        lines=lines.decode('utf-8')
        soup = BeautifulSoup(lines,'html.parser')
    #medal=defaultdict(list)
        table=soup.find_all("table", class_="wikitable sortable plainrowheaders")[0]
    #table_body=table.find('tbody')
        rows=table.find_all('tr')
  
        for row in rows[1:]:
            cells = row.find_all("td")
            countryList.append(cells[-5].a.string)
        highestMedalWinner = countryList[0]
    except:
        pass
    return highestMedalWinner
 
def printoutput1(sport, year, country, purpose):
    medalList = getNumberOfGSB(year, sport, country)
    grandList = numAthletesFromNation(sport)
    count = 0
    try:
        index1 = grandList[0].index(country)
        index2 = grandList[2].index(year)
        count = grandList[1][index1][index2]
    except:
        pass
    grandDict = ReadMedallistData(year, country)
    if purpose == '--summary' or purpose == '--summaryfile': 
        print(str(year)+" "+country+" "+sport)
        print("Summary: ("+str(medalList[0])+","+str(medalList[1])+","+str(medalList[2])+") / "+str(count))
        
        if(len(grandDict['GoldMedalists'])):
            print("Gold: ")
            for event in grandDict['GoldMedalists']:
                if(event[1]==sport):
                    print("Name/s: ",','.join(event[0]), end = " ")
                    print(" Event:",event[2])
        if(len(grandDict['SilverMedalists'])):    
            print("Silver: ")
            for event in grandDict['SilverMedalists']:
                if(event[1]==sport):
                    print("Name/s: ",','.join(event[0]), end = " ")
                    print(" Event:",event[2])
        if(len(grandDict['BronzeMedalists'])):    
            print("Bronze: ")
            for event in grandDict['BronzeMedalists']:
                if(event[1]==sport):
                    print("Name/s: ",','.join(event[0]), end = " ")
                    print(" Event:",event[2])
    if purpose == '--summaryfile':
        now = datetime.datetime.now()
        showtime = now.strftime("%Y-%m-%d-%H-%M")
        file = open("Summary"+str(year)+sport+country+str(showtime)+".txt","w")
        file.write(str(year)+" "+country+" "+sport+"\n")
        file.write("Summary: ("+str(medalList[0])+","+str(medalList[1])+","+str(medalList[2])+") / "+count+"\n")
        
        if(len(grandDict['GoldMedalists'])):
            file.write("Gold: \n")
            for event in grandDict['GoldMedalists']:
                if(event[1]==sport):
                    file.write("Name/s: "+str(event[0])+" ")
                    file.write(" Event: "+str(event[2])+"\n")
        if(len(grandDict['SilverMedalists'])):    
            file.write("Silver: \n")
            for event in grandDict['SilverMedalists']:
                if(event[1]==sport):
                    file.write("Name/s: "+str(event[0])+" ")
                    file.write(" Event:"+str(event[2])+"\n")
        if(len(grandDict['BronzeMedalists'])):    
            file.write("Bronze: \n")
            for event in grandDict['BronzeMedalists']:
                if(event[1]==sport):
                    file.write("Name/s: "+str(event[0])+" ")
                    file.write(" Event:"+str(event[2])+"\n")
                    
        file.close()

def printoutput2(sport, country, purpose):
    grandList = numAthletesFromNation(sport)
    year_list=grandList[2]
    medalListToPlotGold = []
    medalListToPlotSilver = []
    medalListToPlotBronze = []
    participants = []

    if purpose == '--summary' or purpose == '--summaryfile':
        print(country+" "+sport)
        for year in year_list:
            medalList = getNumberOfGSB(year, sport, country)
            medalListToPlotGold.append(medalList[0])
            medalListToPlotSilver.append(medalList[1])
            medalListToPlotBronze.append(medalList[2])
            index1 = grandList[0].index(country)
            index2 = grandList[2].index(year)
            count = grandList[1][index1][index2]
            participants.append(count)
            print(str(year)+": "+str(medalList[0])+","+str(medalList[1])+","+str(medalList[2])+" / "+count)
    if purpose == '--summaryfile':
        now = datetime.datetime.now()
        showtime = now.strftime("%Y-%m-%d-%H-%M")
        file = open("Summary"+sport+country+str(showtime)+".txt","w")
        file.write(country+" "+sport+"\n")
        for year in year_list:
            medalList = getNumberOfGSB(year, sport, country)
            index1 = grandList[0].index(country)
            index2 = grandList[2].index(year)
            count = grandList[1][index1][index2]
            file.write(str(year)+": "+str(medalList[0])+","+str(medalList[1])+","+str(medalList[2])+" / "+str(count)+"\n")
        file.close()
    if purpose == '--graph':
        yearsToPlot = []
        for year in year_list:
            medalList = getNumberOfGSB(year, sport, country)
#            #print(medalList)
#            medalListToPlotGold.append(medalList[0])
#            medalListToPlotSilver.append(medalList[1])
#            medalListToPlotBronze.append(medalList[2])
            index1 = grandList[0].index(country)
            index2 = grandList[2].index(year)
            count = grandList[1][index1][index2]
            
            if count != ' ':
                yearsToPlot.append(year)
                participants.append(count)
                medalListToPlotGold.append(medalList[0])
                medalListToPlotSilver.append(medalList[1])
                medalListToPlotBronze.append(medalList[2])
            
            
        width = 1.0
    
        x  = np.array(yearsToPlot)       
        y1 = np.array(medalListToPlotGold)       
        y2 = np.array(medalListToPlotSilver)
        y3 = np.array(medalListToPlotBronze)        
        y4 = np.array(participants)
        print(participants)
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ind = np.arange(len(yearsToPlot))
       
        p1 = ax1.bar(x,y1,width,color="orange")
        p2 = ax1.bar(x,y2,width,color="gray",bottom=y1)
        p3 = ax1.bar(x,y3,width,color="brown",bottom=y2)
        ax1.set_ylabel("Medal count")
        ax2 = ax1.twinx()
        
        p4 = ax2.bar(x+width,y4,width,color="green")
        ax2.set_ylabel("participant count")
        
        
        plt.legend((p1[0],p2[0],p3[0],p4[0]),('gold','silver','bronze','participants'),loc="upper left")
        plt.title("Medal count for "+country+" in year")
        plt.xlabel("year")
        
        plt.xticks(yearsToPlot, rotation=45)
        ax1.set_xticklabels(yearsToPlot,rotation=90)
        ax2.set_xticklabels(yearsToPlot,rotation=90)
        
        
        plt.show()
        
def printoutput3(year, country, purpose):
    medalListToPlotGold = []
    medalListToPlotSilver = []
    medalListToPlotBronze = []
    participants = []
    g=0
    s=0
    b=0
    total=0
    if purpose == '--summary' or purpose == '--summaryfile':
        print(str(year)+" "+country)
        for sport in sportlist:
            medalList = getNumberOfGSB(year, sport, country)
            g=g+medalList[0]
            s=s+medalList[1]
            b=b+medalList[2]
            grandList = numAthletesFromNation(sport)
            if country in grandList[0]:
                index1 = grandList[0].index(country)    
                if year in grandList[2]:
                    index2 = grandList[2].index(year)
                    count = grandList[1][index1][index2]
                    print(sport+": "+str(medalList[0])+","+str(medalList[1])+","+str(medalList[2])+" / "+str(count))
        total=totalParticipantsFromCountry(year,country)
        print('('+str(g)+','+str(s)+','+str(b)+') in all sports by '+country+' in '+str(year)+'/'+str(total))

    if purpose == '--summaryfile':
        now = datetime.datetime.now()
        showtime = now.strftime("%Y-%m-%d-%H-%M")
        file = open("Summary"+str(year)+country+str(showtime)+".txt","w")
        file.write(str(year)+" "+country+"\n")
        for sport in sportlist:
            medalList = getNumberOfGSB(year, sport, country)
            grandList = numAthletesFromNation(sport)
            if country in grandList[0]:
                index1 = grandList[0].index(country)    
                if year in grandList[2]:
                    index2 = grandList[2].index(year)
                    count = grandList[1][index1][index2]       
                    file.write(sport+": "+str(medalList[0])+","+str(medalList[1])+","+str(medalList[2])+" / "+str(count)+"\n")
        file.write('('+str(g)+','+str(s)+','+str(b)+') in all sports by '+country+' in '+str(year)+'/'+str(total))
        file.close()
        
    if purpose == '--graph':
        for sport in sportlist:
            medalList = getNumberOfGSB(year, sport, country)
            medalListToPlotGold.append(medalList[0])
            medalListToPlotSilver.append(medalList[1])
            medalListToPlotBronze.append(medalList[2])
            grandList = numAthletesFromNation(sport)
            if country in grandList[0]:
                index1 = grandList[0].index(country)    
                if year in grandList[2]:
                    index2 = grandList[2].index(year)
                    count = grandList[1][index1][index2]
                    participants.append(count)
        width = 0.5
    
        x= np.array(sportlist)
        y1 = np.array(medalListToPlotGold)
        y2 = np.array(medalListToPlotSilver)
        y3 = np.array(medalListToPlotBronze)
        y4 = np.array(participants)
        ind = np.arange(len(sportlist))

        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        p1 = ax1.bar(ind,y1,width,color="orange")
        p2 = ax1.bar(ind,y2,width,color="gray",bottom=y1)
        p3 = ax1.bar(ind,y3,width,color="brown",bottom=y2)
        
        ax2=ax1.twinx()
        p4 = ax2.bar(ind+width,y4,width,color="green")

        plt.legend((p1[0],p2[0],p3[0],p4[0]),('gold','silver','bronze','participants'),loc="upper right")
        plt.title("Medal count for "+country+" in "+str(year))
        ax1.set_ylabel("Medal Count")
        ax2.set_ylabel("Participant count")
        plt.xlabel("sport")
        
#        plt.xticks(sportlist,rotation=45)
        ax1.set_xticklabels(sportlist,rotation=90)
        ax2.set_xticklabels(sportlist,rotation=90)
    
        plt.show()
            
def printoutput4(year, sport, purpose):
    medalListToPlotGold = []
    medalListToPlotSilver = []
    medalListToPlotBronze = []
    participants = []
    count = 0
    totalparticipantcount=0
    totalcountrycount=0
    totalcounts=[]
    if purpose == '--summary' or purpose == '--summaryfile':
        print(str(year)+" "+sport)
        grandList = numAthletesFromNation(sport)
        totalcounts=total_athletes_from_all_nations(sport)
        country_list = numAthletesFromNation(sport)[0]
        for country in country_list:
            medalList = getNumberOfGSB(year, sport, country)

            try:
                index1 = grandList[0].index(country)
                index2 = grandList[2].index(year)
                count = grandList[1][index1][index2]
                
            except:
                pass
            if medalList[0] or medalList[1] or medalList[2]:
                print(country+": "+str(medalList[0])+","+str(medalList[1])+","+str(medalList[2])+" / "+str(count))
        index1t = totalcounts[2].index(year)
        totalcountrycount=totalcounts[0][index1t]
        totalparticipantcount=totalcounts[1][index1t]
        print('Total participants in '+sport+' in '+str(year)+' from no of countries: '\
              +str(totalparticipantcount)+' from '+str(totalcountrycount)+' countries')
    if purpose == '--summaryfile':
        now = datetime.datetime.now()
        showtime = now.strftime("%Y-%m-%d-%H-%M")
        file = open("Summary"+str(year)+sport+str(showtime)+".txt","w")
        file.write(str(year)+" "+sport+"\n")
        country_list = numAthletesFromNation(sport)[0]
        grandList = numAthletesFromNation(sport)
        for country in country_list:
            medalList = getNumberOfGSB(year, sport, country)
            
            try:
                index1 = grandList[0].index(country)
                index2 = grandList[2].index(year)
                count = grandList[1][index1][index2]
            except:
                pass
            
            if medalList[0] or medalList[1] or medalList[2]:
                file.write(country+": "+str(medalList[0])+","+str(medalList[1])+","+str(medalList[2])+" / "+str(count)+"\n")
        file.write('Total participants in '+sport+' in '+str(year)+' from no of countries: '\
              +str(totalparticipantcount)+' from '+str(totalcountrycount)+' countries')
        file.close()
    if purpose == '--graph':
        countryListToPlot = []
        country_list = numAthletesFromNation(sport)[0]
        for country in country_list:
            medalList = getNumberOfGSB(year, sport, country)
            if medalList[0] or medalList[1] or medalList[2]:
                medalListToPlotGold.append(medalList[0])
                medalListToPlotSilver.append(medalList[1])
                medalListToPlotBronze.append(medalList[2])
                grandList = numAthletesFromNation(sport)
                countryListToPlot.append(country)
                try:
                    index1 = grandList[0].index(country)
                    index2 = grandList[2].index(year)
                    count = grandList[1][index1][index2]
                    participants.append(count)
                except:
                    pass
            
            
        width = 0.35
        x=np.array(countryListToPlot)
        y1 =np.array(medalListToPlotGold)
        y2 =np.array(medalListToPlotSilver)
        y3 =np.array(medalListToPlotBronze)
        y4 =np.array(participants)
        ind = np.arange(len(countryListToPlot))
        
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        
        p1 = ax1.bar(ind,y1,width,color="orange")
        p2 = ax1.bar(ind,y2,width,color="gray",bottom=y1)
        p3 = ax1.bar(ind,y3,width,color="brown",bottom=y2)
        
        ax2 = ax1.twinx()
        p4 = ax2.bar(ind+width,y4,width,color="green")

        plt.legend((p1[0],p2[0],p3[0],p4[0]),('gold','silver','bronze','participants'),loc="upper right")
        plt.title("Medal count for "+sport+" in "+str(year))
        ax1.set_ylabel("Medal Count")
        ax2.set_ylabel("participant count")
        plt.xlabel("country")
        #plt.xticks(countryListToPlot,rotation=45)
        ax1.set_xticklabels(countryListToPlot,rotation=90)
        ax2.set_xticklabels(countryListToPlot,rotation=90)
        plt.show()
      
def printoutput5(sport, purpose):
    participants = []
    hostnameList = []
    #grandlist=total_athletes_from_all_nations(sport)
    #print(grandlist)
    year_list = total_athletes_from_all_nations(sport)[2]
    nationCount = total_athletes_from_all_nations(sport)[0]
    #print(nationCount)
    athleteCount = total_athletes_from_all_nations(sport)[1]
    #print(athleteCount)
    
    if purpose == '--summary' or purpose == '--summaryfile':            
        for year in year_list:                
            print(str(year)+":")
            hostName = findHost(year)
            print("Host country :", hostName)
            try:
                i = year_list.index(year)                
                print("No of participants from "+str(nationCount[i])+" countries in "+str(year)+": "+str(athleteCount[i]))
                print("Highest medal winner: ", highestMedalWinningCountry(sport,year))
            except:
                pass
                
    if purpose == '--summaryfile':
        now = datetime.datetime.now()
        showtime = now.strftime("%Y-%m-%d-%H-%M")
        file = open("Summary"+sport+str(showtime)+".txt","w")
        for year in yearlist:
            try:
                file.write(str(year)+":"+"\n")
                hostName = findHost(year)
                file.write("Host country :"+str(hostName)+"\n")
                i = year_list.index(year)
                
                file.write("No of participants from "+str(nationCount[i])+" countries in "+str(year)+": "+str(athleteCount[i])+"\n")
                file.write("Highest medal winner: "+highestMedalWinningCountry(sport,year)+"\n")
            except:
                pass
        file.close()

    if purpose == '--graph':
        participants = []
        hostnameList = []
        year_list = total_athletes_from_all_nations(sport)[2]
        highestMedalWinningCountryList = []
        yearToPlot = []
        for year in year_list:
            hostName = findHost(year)
            
            try:
                i = year_list.index(year)
                nationCount = total_athletes_from_all_nations(sport)[0][i]
                athleteCount = total_athletes_from_all_nations(sport)[1][i]
                if athleteCount != '-':
                    hostnameList.append(hostName)
                    yearToPlot.append(year)
                    participants.append(athleteCount)

                highestMedalWinningCountryList.append(highestMedalWinningCountry(sport,year))
            except:
                pass
        width = 2.0
        
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
    
        x=np.array(yearToPlot)
        #print(yearToPlot)
        y1 = np.array(participants)
        #print(participants)
        ind = np.arange(len(x))

        r1 = ax1.bar(x,y1,width,color="brown")    
        for rect in r1:
            print(highestMedalWinningCountry(sport,rect.get_x()))
            ax1.text(rect.get_x(),rect.get_y(),str(highestMedalWinningCountry(sport,rect.get_x())))
        ax1.set_title("Athlete count for "+sport+" in <year>")
        ax1.set_ylabel("total number of participants ")
        ax1.set_xlabel("year")
        #ax1.set_xtickslabels(x, rotation=90)
        plt.xticks(yearToPlot,rotation=90)
#        rects = ax1.patches
        #labels = [""highestMedalWinningCountryList]
#        for rect in rects:
#            height = rect.get_height()
#            ax1.text(5,height+5,ha='center',va='bottom')
        plt.show()
            
def printoutput6(year, purpose):
    if purpose == '--summary' or purpose == '--summaryfile':
        print(year)
        print("Host country: ", findHost(year))
        print("List of Athletes by sport:")
        for sport in sportlist:
            totalAthletesFromAllNations = total_athletes_from_all_nations(sport)
            AthleteCount=0
            nationCount=0
            try:
                year_list = total_athletes_from_all_nations(sport)[2]
                i=year_list.index(year)
                nationCount = totalAthletesFromAllNations[0][i]
                AthleteCount = totalAthletesFromAllNations[1][i]
            except:
                pass
            print(sport+": total "+str(AthleteCount)+" participants from "+str(nationCount)+" countries")
        print("List of countries and their medal count that year:")
        countrylist = readyearfile(year)[0]
        for country in countrylist:
            medalData = readyearfile(year)
            medallist=(0,0,0,0)
            try:
                countrynames = medalData[0]
                index = countrynames.index(country)
                medallist = medalData[1][index]
            except:
                pass
            print(country+": ( "+str(medallist[0])+","+str(medallist[1])+","+str(medallist[2])+") / "+str(totalParticipantsFromCountry(year,country)))
    if purpose == '--summaryfile':
        now = datetime.datetime.now()
        showtime = now.strftime("%Y-%m-%d-%H-%M")
        file = open("Summary"+str(year)+str(showtime)+".txt","w")
        file.write(str(year)+"\n")
        file.write("Host country: "+str(findHost(year))+"\n")
        file.write("List of Athletes by sport: \n")
        for sport in sportlist:
            totalAthletesFromAllNations = total_athletes_from_all_nations(sport)
            AthleteCount=0
            nationCount=0
            try:
                year_list = total_athletes_from_all_nations(sport)[2]
                i=year_list.index(year)
                nationCount = totalAthletesFromAllNations[0][i]
                AthleteCount = totalAthletesFromAllNations[1][i]
            except:
                pass
            file.write(sport+": total "+str(AthleteCount)+" participants from "+str(nationCount)+" countries \n")

        file.write("List of countries and their medal count that year: \n")
        countrylist = readyearfile(year)[0]
        for country in countrylist:
            medalData = readyearfile(year)
            medallist=(0,0,0,0)
            try:
                countrynames = medalData[0]
                index = countrynames.index(country)
                medallist = medalData[1][index]
            except:
                pass
            file.write(country+": ( "+str(medallist[0])+","+str(medallist[1])+","+str(medallist[2])+") / "+str(totalParticipantsFromCountry(year,country))+"\n")
        file.close()
    if purpose == '--graph':
        nationCountToPlot = []
        athleteCountToPlot = []
        for sport in sportlist:
            totalAthletesFromAllNations = total_athletes_from_all_nations(sport)
            AthleteCount=0
            nationCount=0
            try:
                year_list = total_athletes_from_all_nations(sport)[2]
                i=year_list.index(year)
                nationCount = totalAthletesFromAllNations[0][i]
                nationCountToPlot.append(nationCount)
                AthleteCount = totalAthletesFromAllNations[1][i]
                athleteCountToPlot.append(AthleteCount)
            except:
                pass
        width = 0.5
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        x=np.array(sportlist)
        y1 = np.array(nationCountToPlot)
        
        ax2= ax1.twinx()
        y2 = np.array(athleteCountToPlot)
        ind = np.arange(len(x))

        r1= ax1.bar(ind,y1,width,color="brown")
        r2= ax2.bar(ind+width,y2,width,color="yellow")
       

        plt.legend((r1[0],r2[0]),('nationcount','athleteCount'),loc="upper left")
        plt.title("Athlete count and nation count for "+str(year)+" in <sport>")
        ax1.set_ylabel("total number of countries ")
        ax2.set_ylabel("Total number of participants")
        plt.xlabel("sport")
        
        plt.xticks(ind, sportlist, rotation=45)
        ax1.set_xticklabels(sportlist,rotation=90)
        ax2.set_xticklabels(sportlist,rotation=90)

        
        plt.yticks(ind,y2,50)      

        plt.show()
        
        
           
def printoutput7(country, purpose):
    if purpose == '--summary' or purpose == '--summaryfile':
        print(country)
        for year in yearlist:
            combinedList = readyearfile(year)
            medallist=(0,0,0,0)
            try:
                index = combinedList[0].index(country)
                medallist = combinedList[1][index]
            except:
                pass
            print(str(year)+": total ("+str(medallist[0])+","+str(medallist[1])+","+str(medallist[2])+") /"+str(totalParticipantsFromCountry(year,country)))
    if purpose == '--summaryfile':
        now = datetime.datetime.now()
        showtime = now.strftime("%Y-%m-%d-%H-%M")
        file = open("Summary"+country+str(showtime)+".txt","w")
        file.write(country+"\n")
        for year in yearlist:
            combinedList = readyearfile(year)
            medallist=(0,0,0,0)
            try:
                index = combinedList[0].index(country)
                medallist = combinedList[1][index]
            except:
                pass
            file.write(str(year)+": total ("+str(medallist[0])+","+str(medallist[1])+","+str(medallist[2])+") /"+str(totalParticipantsFromCountry(year,country))+"\n")
        file.close()
    if purpose == '--graph':
       
        participants = []
        yearToPlot = []
        totalNumberOfMedals = []
        
        for year in yearlist:
            combinedList = readyearfile(year)
            medallist=(0,0,0,0)
            try:
                index = combinedList[0].index(country)
                medallist = combinedList[1][index]
                totalNumberOfMedals.append(medallist[3])               
                participants.append(totalParticipantsFromCountry(year,country))
                if medallist[0] or medallist[1] or medallist[2]:
                    yearToPlot.append(year)
            except:
                pass
        width = 0.5
    
       
        
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        
        x=np.array(yearToPlot)
        y1 = np.array(totalNumberOfMedals)
        #print(totalNumberOfMedals)
        y2 = np.array(participants)
        #print(participants)
        
        ind = np.arange(len(x))
        
        r1= ax1.bar(ind,y1,width,color="yellow")
        
        ax2 = ax1.twinx()
        r2 = ax2.bar(ind+width,y2,width,color="green")
        ax1.set_ylabel("Medal count ")
        ax2.set_ylabel("participant count ")
        ax1.set_xlabel("year")
        plt.xticks(ind, yearToPlot, rotation=45)
        ax1.set_xticklabels(yearToPlot,rotation=90)
        ax2.set_xticklabels(yearToPlot,rotation=90)
        plt.legend((r1[0],r2[0]),('medal count','participants'),loc="upper left")
        plt.title("Medal count and prticipant count for "+country)
        
        plt.show()
        
        

def main():
	import sys
	args = sys.argv[1:]
	print(args)
	print(len(args))
	sport = ""
	country = ""
	year = 0
	
	"""checking if minimum argments are provided or not"""
	if not args:
		print('Please provide at least two arguments: usage is WinterOlympics.py <purpose> -year <year> -sport "sport" -country "country"')
		sys.exit()
	elif len(args) < 2:
		print('Please provide purpose and one more argument: usage is WinterOlympics.py <purpose> -year <year> -sport "sport" -country "country"')
		sys.exit()
	elif len(args) > 7:
		print("too many arguments")
		print('usage: WinterOlympics.py <purpose> -year <year> -sport "sport" -country "country"')
		print("purpose should be one of the following: --summary, --summaryfile, --graph")
		sys.exit()
	else:
		purpose = sys.argv[1]
		if purpose not in ("--summary", "--summaryfile", "--graph"):
			print("not valid purpose specified, purpose should be one of the following: --summary, --summaryfile, --graph")
			sys.exit()
			
	if "-sport" in args:
		index = args.index("-sport")
		sport = args[index+1]
		if sport not in sportlist:
			print("not a valid sport, please choose from the below list")
			print(sportlist)
			sys.exit()
	if "-year" in args:
		index = args.index("-year")
		year = int(args[index+1])
		if year not in yearlist:
			print("invalid year, please choose from the below list")
			print(yearlist)
			sys.exit()
	if "-country" in args:
		index = args.index("-country")
		country = args[index+1]
		
	"""printing output to the console for case 1"""
	if sport != "" and year != 0 and country != "":
		printoutput1(sport, year, country,sys.argv[1])
	elif sport != "" and country != "" and year == 0:
		printoutput2(sport, country, sys.argv[1])
	elif sport == "" and year != 0 and country != "":
		printoutput3(year, country, sys.argv[1])
	elif sport != "" and year != 0 and country == "":
		printoutput4(year, sport, sys.argv[1])
	elif sport != "" and year == 0 and country =="":
		printoutput5(sport, sys.argv[1])
	elif sport == "" and year != 0 and country == "":
		printoutput6(year, sys.argv[1])
	else:
		printoutput7(country, sys.argv[1])
		
		

			
	
	
if __name__ == '__main__':
	main()

