from string import ascii_lowercase
from bs4 import BeautifulSoup
import requests
from bokeh.plotting import figure, show, output_file
import datetime
import pandas_datareader
from pandas_datareader import data
# import fix_yahoo_finance
from datetime import datetime as dt
year = dt.now().year
month = dt.now().month
day = dt.now().day


# Global Variable Decleration
names = []
my_string = []
final = []
ticker = ""
headers = {
    'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

# Getting the input and first letter

string = input("Enter the company name (NYSE): ")
fl = string[0]


# Creating the url
base_url = f"https://www.dogsofthedow.com/stock/stock-symbols-list-{fl}.htm"

# Scraping Website for data
r = requests.get(base_url, headers=headers)
c = r.content
soup = BeautifulSoup(c, "html.parser")
all_1 = soup.find_all("td", {"class": "column-1"})
all_2 = soup.find_all("td", {"class": "column-2"})
all_3 = soup.find_all("td", {"class": "column-3"})


# Getting specific values
def get_value(x):
    final = []
    for i in range(len(x)):
        names.append(x[i].find("a"))
        i += 1

    for i in range(len(x)):
        my_string.append((str(names[i])).split(">", 1)[1].split('<'))

    for i in range(len(my_string)):
        final.append(my_string[i][0])

    return final


def tget_value(x):
    final = []
    my_string = []
    names = []
    for i in range(len(x)):
        names.append(x[i].find("a"))
        i += 1
    for i in range(len(x)):
        my_string.append((str(names[i])).split(">", 2)[1].split('<'))
    for i in range(len(my_string)):
        final.append(my_string[i][0])

    return final


all_names = (get_value(all_1))
all_tickers = (tget_value(all_2))

# Comparing input string to all names

if string in all_names:
    ticker = all_tickers[all_names.index(string)]

s_year = input("Enter the initial year: ")
s_month = input("Enter the initial month: ")
s_day = input("Enter the initial day: ")

# Generation of Graph

start = datetime.datetime(int(s_year), int(s_month), int(s_day))
end = datetime.datetime(year, month, day)

df = data.DataReader(
    name=f"{ticker}", data_source="yahoo", start=start, end=end)


def inc_dec(c, o):
    if c > o:
        value = "Increase"
    elif c < o:
        value = "Decrease"
    else:
        value = "Equal"
    return value


df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]

df["Middle"] = (df.Open+df.Close)/2
df["Height"] = abs(df.Close-df.Open)

p = figure(x_axis_type='datetime', width=1000, height=300,
           title="Candlestick Chart", sizing_mode="scale_width")
p.grid.grid_line_alpha = 0.3


hour_12 = 12*60*60*1000

p.segment(df.index, df.High, df.index, df.Low, color="black")

p.rect(df.index[df.Status == 'Increase'], df.Middle[df.Status == 'Increase'],
       hour_12, df.Height[df.Status == 'Increase'], fill_color="#CCFFFF", line_color="black")

p.rect(df.index[df.Status == 'Decrease'], df.Middle[df.Status == 'Decrease'],
       hour_12, df.Height[df.Status == 'Decrease'], fill_color="#FF3333", line_color="black")

output_file("CS.html")
show(p)
