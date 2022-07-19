import requests
from bs4 import BeautifulSoup
import pandas as pd

def returndata(x): #function to get the table from the nfl.com website
    if x == "passing": #different link for each statistic
        url = "https://www.nfl.com/stats/player-stats/category/passing/2021/POST/all/passingyards/desc"
    elif x == "rushing":
        url = "https://www.nfl.com/stats/player-stats/category/rushing/2021/POST/all/rushingyards/desc"
    elif x == "recieving":
        url = "https://www.nfl.com/stats/player-stats/category/receiving/2021/POST/all/receivingreceptions/desc"
    else:
        print("no data recieved, restart program") #restarts program if none of the three are requested
        exit()
        

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser') #gets the html parser
    table1 = soup.find('table') #find where it says table in html
    headers = []

    for i in table1.find_all('th'):
        title = i.text
        headers.append(title)

    mydata = pd.DataFrame(columns = headers)
    for j in table1.find_all('tr')[1:]: #makes a column for each header name
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(mydata)
        mydata.loc[length] = row

    return mydata

def ydstd(x): #function to normalize the Yards statistic so columns can be combined and sorted
    y = returndata(x)
    if x == "passing":
        y["Yds"] = y["Pass Yds"]
    elif x == "rushing":
        y["Yds"] = y["Rush Yds"]
    elif x == "recieving":
        y['Yds'] = y['Yds']
    else:
        print("wrong data recieved, restart program")
        exit()
    
    y.drop(y.columns.difference(['Player','Yds', 'TD']), 1, inplace=True) #drops everything but 3 columns

    return y
    
class plyrs: #class for filtering the data based on input
    def __init__(self, z, x, y):
        self.z = z
        self.x = x
        self.y = y
    def getrows(self):
        self.z = self.z.sort_values(by = [self.x], ascending = [False]) #sorts value by input
        filter = self.z[ self.z[self.x].astype(int) >= self.y ] #sets condition based on input
        print(filter) #prints filtered table
        print("We will export this to a new csv file")
        filter.to_csv('filtered_stats.csv')

x = input("What offensive 2021 season statistic do you want to analyze: passing, rushing, or recieving? ") #ask user for first statistic
x = x.lower() #makes sure its lowercase
y = returndata(x) #gets the table
print("This is the data for the 2021 season on", x, "for the top 24 players: ")
print(y)


print("There numerous ways to examine this data using Pandas and Python")
print("for example, you can see who has the most passing touchdowns with the least interceptions like this")
p="passing"
n = returndata(p)
j = n.sort_values(by = ['TD', 'INT'], ascending = [False, True]) #sorts values of two columns
print(j)

print("You can combine tables and see which players from different categories had the most yards and TDs") #user will combine tables
first = input("Pick the first statistic to combine with yards and touchdown: passing, rushing, or recieving: ") #first table
second = input("Pick the second statistic: ") #second table
first=first.lower()
second=second.lower()
if first == second:
    while first == second:
        second = input("Use a different statistic for the second one: ") #ensures that user is not combining same table
a = ydstd(first)
b = ydstd(second)


result = pd.concat([a,b]) #combines the tables
result = result.sort_values(by = ['Yds'], ascending=[False]) #sorts it by yards
print(result)


print("Another stat that is calculated for frequently is QB rating. The formula consists of 4 different equations")
print("I will create a new column in the passing table for QBR") #QBR is one of the most important stats in the game
p2="passing"
z = returndata(p2)
#qbr contains 4 formulas
form1 = (z['Cmp'].astype(int)/z['Att'].astype(int) -.3)*5 #important to change column values to integers
form2 = (z['Pass Yds'].astype(int)/z['Att'].astype(int) -.3)*.25
form3 = (z['TD'].astype(int)/z['Att'].astype(int))*20
form4 = (2.375-z['INT'].astype(int)/z['Att'].astype(int))*25
z['QBR'] = (form1+form2+form3+form4/6)*10 #adds new columns by summing formulas
print(z)

#ask user for stat and condtion
stat = input("You can also compare players by filtering stats, which Quarterback stat do you want to filter: ") 
num = input("What is the minimum the player needs to have? ")
num = int(num)
df = plyrs(z, stat, num) 
df.getrows() #prints the new dataframe with only those rows met by the condition 