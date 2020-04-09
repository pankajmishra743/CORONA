
from flask import Flask, jsonify, render_template, request, flash, redirect
from pandasql import sqldf

import pandas as pd
import numpy as np
import io
import requests
import responses

d = pd.read_html('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India')
df = d[5].iloc[:-2]
df1 = df.iloc[:-1]
df2 = df.tail(1)
final_df = pd.concat([df2, df1]).reset_index(drop=True)
final_df.columns = ['SN', 'STATE_UT', 'ACTIVE_CASES', 'DEATHS', 'RECOVERIES', 'TOTAL'] 
final_df['STATE_UT'] = (final_df['STATE_UT'].str.strip(' †'))
final_df.at[0, 'STATE_UT'] = 'All India'

dd = pd.read_html('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India')
state_df = dd[7].iloc[:-4]
state_df = state_df.replace(to_replace ='\(.*\)', value = '', regex = True) 
state_df = state_df.replace(to_replace ='\[.*\]', value = '', regex = True)
state_df.fillna(0, inplace=True)
state_df = state_df.iloc[:, :-4]

ColumnName = final_df['STATE_UT'].tolist()
ColumnName.append('New')
ColumnName.append(ColumnName.pop(ColumnName.index('All India')))
ColumnName.insert(0, "Date")
ColumnName = ColumnName[2:]
state_df.columns = ColumnName
# state_df.rename(columns = {'Total':'All India'}, inplace = True)
# state_df.rename(columns = {'Date (2020)':'Date'}, inplace = True)

# for world analysis

url = 'https://www.worldometers.info/coronavirus'
r = requests.get(url)
dm = pd.read_html(r.text)
l_df = dm[1]
l_df.rename(columns = {'Country,Other':'Country'}, inplace = True)
df_US = l_df.loc[(l_df['Country'] == 'USA')]
df_India = l_df.loc[(l_df['Country'] == 'India')]
df_China = l_df.loc[(l_df['Country'] == 'China')]
df_Japan = l_df.loc[(l_df['Country'] == 'Japan')]
df_South_Korea = l_df.loc[(l_df['Country'] == 'S. Korea')]
df_Italy = l_df.loc[(l_df['Country'] == 'Italy')]
df_Taiwan = l_df.loc[(l_df['Country'] == 'Taiwan')]
frames = [df_India, df_US, df_China, df_Japan, df_South_Korea, df_Italy, df_Taiwan]
dataframe = pd.concat(frames)
dataframe.fillna(0, inplace=True)
dataframe.reset_index(inplace=True)
dataframe['NewCases'] = dataframe['NewCases'].str.replace(',', '')
dataframe['NewCases'] = (dataframe['NewCases'].str.strip('+').astype(float))
dataframe['NewDeaths'] = dataframe['NewDeaths'].str.replace(',', '')
dataframe['NewDeaths'] = (dataframe['NewDeaths'].str.strip('+').astype(float))
del dataframe["index"]
dataframe.replace(to_replace ="S. Korea", value ="South Korea", inplace=True)
Abbr = ['IN', 'US', 'CH', 'JP', 'SK','IT', 'TW']
dataframe['Abbr'] = Abbr
dataframe.fillna(0, inplace=True)
dataframe.columns = ['Country', 'Total_Cases', 'New_Cases', 'Total_Deaths','New_Deaths', 'Total_Recovered', 'Active_Cases',
                     'Serious_Critical','Total_Cases_Per_1_M_PPL', 'Deaths_Per_1_M_PPL', 'Total_Tests', 'Total_Tests_Per_1_M_PPL', 'Abbr']
#cols = ['Total_Deaths', 'New_Deaths', 'Total_Recovered']
#dataframe[cols] = dataframe[cols]                  
dataframe.to_csv('static/assets/data/file1.csv') 
 


#for world analysis-2

url = [
       'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
       'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
       'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
      ]
colName = ['Confirmed', 'Recovered', 'Deaths']
countryList = ['India', 'China', 'USA', 'Japan', 'South Korea', 'Italy', 'Taiwan']
finalDataframe = []
for i in range(len(url)): 
    s=requests.get(url[i]).content
    fetched_Dataframe=pd.read_csv(io.StringIO(s.decode('utf-8')))
    fetched_Dataframe.fillna(0, inplace=True)
    fetched_Dataframe = fetched_Dataframe.groupby('Country/Region', as_index=False).sum()
    columns = ['Lat', 'Long']
    fetched_Dataframe.drop(columns, inplace=True, axis=1)
    fetched_Dataframe.replace(to_replace ="Korea, South", value ="South Korea", inplace=True) 
    fetched_Dataframe.replace(to_replace ="Taiwan*", value ="Taiwan", inplace=True)
    fetched_Dataframe.replace(to_replace ="US", value ="USA", inplace=True)
    Record = []
    for j in range(len(countryList)): 
        parameter_Specific_Dataframe_4_Country = fetched_Dataframe.loc[fetched_Dataframe['Country/Region'] == str(countryList[j])]
        parameter_Specific_Dataframe_4_Country = parameter_Specific_Dataframe_4_Country.transpose()
        parameter_Specific_Dataframe_4_Country.columns = [colName[i]]
        if (i==1):
            parameter_Specific_Dataframe_4_Country.insert(0, 'Country', str(countryList[j])) 
        parameter_Specific_Dataframe_4_Country = parameter_Specific_Dataframe_4_Country.iloc[1:]
        Record.append(parameter_Specific_Dataframe_4_Country) 
    parameter_Specific_Dataframe = pd.concat(Record, axis=0)
    finalDataframe.append(parameter_Specific_Dataframe)
total_df = pd.concat(finalDataframe, axis=1)
total_df.reset_index(inplace=True)
total_df.rename(columns = {'index':'Date'}, inplace = True)
total_df['Date'] = pd.to_datetime(total_df['Date']) 
total_df['Date'] = total_df['Date'].dt.strftime('%d/%m/%Y')


meta_df = final_df.transpose()
meta_df = meta_df.iloc[1:]
headers = meta_df.iloc[0]
meta_df  = pd.DataFrame(meta_df.values[1:], columns=headers)


app = Flask(__name__)
@app.route("/")
def index():
    return render_template("myindex.html")
    
@app.route("/INvsWL")
def index1():
    return render_template("index.html")  

@app.route('/names')
def names():
    """Return a list of sample names."""
    a = final_df["STATE_UT"].tolist()
    a = a[3:]
    a.insert(0, "All India")
    return jsonify(a)

@app.route('/metadata/<state>')
def sample_metadata(state):
    """Return the MetaData for a given State."""
    ldf = final_df
    final = {}
    
    state_metadata = {}
    state_metadata['Active Cases'] = ldf[ldf['STATE_UT']==state]['ACTIVE_CASES'].to_string(index=False)
    state_metadata['Recoveries'] = ldf[ldf['STATE_UT']==state]['RECOVERIES'].to_string(index=False)
    state_metadata['Deaths'] = ldf[ldf['STATE_UT']==state]['DEATHS'].to_string(index=False)
    state_metadata['TOTAL'] = ldf[ldf['STATE_UT']==state]['TOTAL'].to_string(index=False)
        
    AllIndia_metadata = {}
    AllIndia_metadata['Deaths'] = ldf[ldf['STATE_UT']==state]['ACTIVE_CASES'].to_string(index=False)
    AllIndia_metadata['Recoveries'] = ldf[ldf['STATE_UT']==state]['DEATHS'].to_string(index=False)
    AllIndia_metadata['TOTAL'] = ldf[ldf['STATE_UT']==state]['RECOVERIES'].to_string(index=False).replace("#", "").replace("*", "")
    a = pd.to_numeric(AllIndia_metadata['Deaths'], errors='coerce').astype(int)
    b = pd.to_numeric(AllIndia_metadata['Recoveries'], errors='coerce').astype(int)
    c = pd.to_numeric(AllIndia_metadata['TOTAL'], errors='coerce').astype(int)
    p = a+b
    d = c-p
    AllIndia_metadata['Active Cases'] = str(d)
    
    if(state == "All India"):
      final = AllIndia_metadata
    else:
      final = state_metadata
      
    return jsonify(final)
    
@app.route('/mdata/<state>')
def sample_mdata(state):
    """Return the MetaData for a given State."""
    final_list = [None] * 4
    a = meta_df[state]
    if(state == "All India"):
      final_list[3] = a[2].replace("#", "").replace("*", "")
      final_list[2] = a[1]
      final_list[1] = a[0]
      
      a = pd.to_numeric(final_list[1], errors='coerce').astype(int)
      b = pd.to_numeric(final_list[2], errors='coerce').astype(int)
      c = pd.to_numeric(final_list[3], errors='coerce').astype(int)
      p = a+b
      d = c-p
      final_list[0] = str(d)
    else:
      final_list[0] = a[0]
      final_list[1] = a[1]
      final_list[2] = a[2]
      final_list[3] = a[3]
    return jsonify(final_list)    
    
@app.route('/dates')
def sample_homedata():
    """Return all dates."""
    x = state_df.iloc[:,0]
    xx = x[2:]
    return jsonify(list(xx)) 

@app.route('/wdates')
def world_data_date():
    """Return all dates."""
    q="""SELECT DISTINCT Date FROM total_df;"""
    pysqldf = lambda q: sqldf(q, globals())
    a_df = pysqldf(q)
    return jsonify(list(a_df.Date))

@app.route('/wcnames')
def world_country_name():
    """Return all dates."""
    q="""SELECT DISTINCT Country FROM total_df;"""
    pysqldf = lambda q: sqldf(q, globals())
    a_df = pysqldf(q)
    return jsonify(list(a_df.Country))  
    
@app.route('/wmetadata/<country>')
def world_country_metadata(country):
    """Return the MetaData for a given country."""
    country_metadata = {}
    ['Country', 'Total_Cases', 'New_Cases', 'Total_Deaths','New_Deaths', 'Total_Recovered', 'Active_Cases',
                     'Serious_Critical','Total_Cases_Per_1_M_PPL', 'Deaths_Per_1_M_PPL', 'Total_Tests', 'Total_Tests_Per_1_M_PPL', 'Abbr']
    country_metadata['Total Cases'] = dataframe[dataframe['Country']==country]['Total_Cases'].to_string(index=False)
    country_metadata['New Cases'] = dataframe[dataframe['Country']==country]['New_Cases'].to_string(index=False)
    country_metadata['Total Deaths'] = dataframe[dataframe['Country']==country]['Total_Deaths'].to_string(index=False)
    country_metadata['New Deaths'] = dataframe[dataframe['Country']==country]['New_Deaths'].to_string(index=False)
    country_metadata['Total Recovered'] = dataframe[dataframe['Country']==country]['Total_Recovered'].to_string(index=False)
    country_metadata['Active Cases'] = dataframe[dataframe['Country']==country]['Active_Cases'].to_string(index=False)
    country_metadata['Total Cases/1M Pop'] = dataframe[dataframe['Country']==country]['Total_Cases_Per_1_M_PPL'].to_string(index=False)
    country_metadata['Deaths/1M Pop'] = dataframe[dataframe['Country']==country]['Deaths_Per_1_M_PPL'].to_string(index=False)
    country_metadata['Total Tests'] = dataframe[dataframe['Country']==country]['Total_Tests'].to_string(index=False)
    country_metadata['Total Tests/1M Pop'] = dataframe[dataframe['Country']==country]['Total_Tests_Per_1_M_PPL'].to_string(index=False)
    return jsonify(country_metadata)  

@app.route('/<country>/conf')
def country_conf(country):
    """Return country wise confirm cases list data."""
    q="SELECT Confirmed FROM total_df where Country = '"+country+"';"
    pysqldf = lambda q: sqldf(q, globals())
    sf = pysqldf(q)
    sf['Confirmed'] = sf['Confirmed'].apply(str)
    return jsonify(list(sf.Confirmed))
    
@app.route('/<country>/recv')
def country_recv(country):
    """Return country wise confirm cases list data."""
    q="SELECT Recovered FROM total_df where Country = '"+country+"';"
    pysqldf = lambda q: sqldf(q, globals())
    sf = pysqldf(q)
    sf['Recovered'] = sf['Recovered'].apply(str)
    return jsonify(list(sf.Recovered))

@app.route('/<country>/death')
def country_death(country):
    """Return country wise confirm cases list data."""
    q="SELECT Deaths FROM total_df where Country = '"+country+"';"
    pysqldf = lambda q: sqldf(q, globals())
    sf = pysqldf(q)
    sf['Deaths'] = sf['Deaths'].apply(str)
    return jsonify(list(sf.Deaths))


@app.route('/statedata/<state>')
def state_data(state):
    """Return state related data."""
    y = state_df[state]
    yy = y[2:]
    return jsonify(list(yy)) 
     
@app.route('/total')
def all_india_data():
    """Return total case."""
    z = state_df["All India"]
    zz = z[2:]
    return jsonify(list(zz))
    
@app.route('/new')
def all_india_new_cases():
    """Return total new cases."""
    l = state_df["New"]
    ll = l[2:]
    return jsonify(list(ll))  
 
@app.route('/check')
def all_check():
    """Return csv."""
    column = final_df.iloc[:,0]
    return jsonify(list(dataframe.columns))
  
@app.route('/check1')
def all_check1():
    """Return csv."""
    column1= final_df.iloc[:,1]
    return jsonify(list(column1))
  
@app.route('/check2')
def all_check2():
    """Return csv."""
    column2 = final_df.iloc[:,2]
    return jsonify(list(column2))
  
@app.route('/checks3')
def all_checks3():
    """Return csv."""
    column3= final_df.iloc[:,3]
    return jsonify(list(column3))
  
@app.route('/check4')
def all_check4():
    """Return csv."""
    column4 = final_df.iloc[:,4]
    return jsonify(list(column4))
  
@app.route('/checks5')
def all_checks5():
    """Return csv."""
    column5= final_df.iloc[:,5]
    return jsonify(list(column5))

  
if __name__ == "__main__":
    app.run(debug=True)
   
    
