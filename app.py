
from flask import Flask, jsonify, render_template, request, flash, redirect
from pandasql import sqldf

import pandas as pd
import numpy as np
import io
import requests

d = pd.read_html('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India')
df = d[7].iloc[:-2]
df.columns = ['SN', 'STATE_UT', 'ACTIVE_CASES', 'DEATHS', 'RECOVERIES', 'TOTAL'] 
df1 = df.iloc[:-1]
df2 = df.tail(1)
final_df = pd.concat([df2, df1]).reset_index(drop=True)
final_df['STATE_UT'] = (final_df['STATE_UT'].str.strip(' †'))
final_df.set_value(0, 'STATE_UT', 'All India') 

dd = pd.read_html('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India')
state_df = dd[6].iloc[:-4]
state_df = state_df.replace(to_replace ='\(.*\)', value = '', regex = True)    
state_df.fillna(0, inplace=True)
state_df = state_df.iloc[:, :-4]

ColumnName = final_df['STATE_UT'].tolist()
#ColumnName.append('New')
ColumnName.append(ColumnName.pop(ColumnName.index('All India')))
#ColumnName.insert(0, "Date")
state_df.columns = ColumnName
# state_df.rename(columns = {'Total':'All India'}, inplace = True)
# state_df.rename(columns = {'Date (2020)':'Date'}, inplace = True)
dataframe.to_csv('static/assets/data/india12345.csv') 

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
dataframe['NewCases'] = dataframe['NewCases'].str.replace(',', '').astype(int)
#dataframe['NewDeaths'] = (dataframe['NewDeaths'].str.strip('+').astype(float))
del dataframe["index"]
dataframe.replace(to_replace ="S. Korea", value ="South Korea", inplace=True)
Abbr = ['IN', 'US', 'CH', 'JP', 'SK','IT', 'TW']
dataframe['Abbr'] = Abbr
dataframe.fillna(0, inplace=True)
dataframe.columns = ['Country', 'Total_Cases', 'New_Cases', 'Total_Deaths','New_Deaths', 'Total_Recovered', 'Active_Cases',
                     'Serious_Critical','Total_Cases_Per_1_M_PPL', 'Deaths_Per_1_M_PPL', '1st_Case_On','Abbr']
cols = ['Total_Deaths', 'New_Deaths', 'Total_Recovered']
dataframe[cols] = dataframe[cols].astype(int)                    
dataframe.to_csv('static/assets/data/file1.csv') 
 


#for world analysis-2

url = 'https://datahub.io/core/covid-19/r/time-series-19-covid-combined.csv'
s=requests.get(url).content
c_df=pd.read_csv(io.StringIO(s.decode('utf-8')))
c_df.fillna(0, inplace=True)
c_df.rename(columns = {'Country/Region':'Country'}, inplace = True)
cf_US = c_df.loc[(c_df['Country'] == 'US')]
cf_India = c_df.loc[(c_df['Country'] == 'India')]

cf_China = c_df.loc[(c_df['Country'] == 'China')]
cf_China = cf_China.groupby('Date', as_index=False).sum()
cf_China.insert(loc=2, column='Country', value=['China' for i in range(cf_China.shape[0])])

cf_Japan = c_df.loc[(c_df['Country'] == 'Japan')]
cf_South_Korea = c_df.loc[(c_df['Country'] == 'Korea, South')]
cf_Italy = c_df.loc[(c_df['Country'] == 'Italy')]
cf_Taiwan = c_df.loc[(c_df['Country'] == 'Taiwan*')]
frame = [cf_India, cf_US, cf_Japan, cf_Italy, cf_China, cf_Taiwan, cf_South_Korea]
total_df = pd.concat(frame, axis=0)
total_df.reset_index(inplace=True)
columns = ['index', 'Province/State', 'Lat', 'Long']
total_df.drop(columns, inplace=True, axis=1)

total_df.replace(to_replace ="Korea, South", value ="South Korea", inplace=True) 
total_df.replace(to_replace ="Taiwan*", value ="Taiwan", inplace=True)
total_df.replace(to_replace ="US", value ="USA", inplace=True)


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
    return jsonify(list(final_df.STATE_UT))

@app.route('/metadata/<state>')
def sample_metadata(state):
    """Return the MetaData for a given State."""
    state_metadata = {}
    state_metadata['Active Cases'] = final_df[final_df['STATE_UT']==state]['ACTIVE_CASES'].to_string(index=False)
    state_metadata['Recoveries'] = final_df[final_df['STATE_UT']==state]['RECOVERIES'].to_string(index=False)
    state_metadata['Deaths'] = final_df[final_df['STATE_UT']==state]['DEATHS'].to_string(index=False)
    state_metadata['TOTAL'] = final_df[final_df['STATE_UT']==state]['TOTAL'].to_string(index=False)
    return jsonify(state_metadata)
    
@app.route('/mdata/<state>')
def sample_mdata(state):
    """Return the MetaData for a given State."""
    return jsonify(list(meta_df[state]))    
    
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
                     'Serious_Critical','Total_Cases_Per_1_M_PPL', 'Deaths_Per_1_M_PPL', '1st_Case_On','Abbr']
    country_metadata['Total Cases'] = dataframe[dataframe['Country']==country]['Total_Cases'].to_string(index=False)
    country_metadata['New Cases'] = dataframe[dataframe['Country']==country]['New_Cases'].to_string(index=False)
    country_metadata['Total Deaths'] = dataframe[dataframe['Country']==country]['Total_Deaths'].to_string(index=False)
    country_metadata['New Deaths'] = dataframe[dataframe['Country']==country]['New_Deaths'].to_string(index=False)
    country_metadata['Total Recovered'] = dataframe[dataframe['Country']==country]['Total_Recovered'].to_string(index=False)
    country_metadata['Active Cases'] = dataframe[dataframe['Country']==country]['Active_Cases'].to_string(index=False)
    country_metadata['Total Cases/1M Pop'] = dataframe[dataframe['Country']==country]['Total_Cases_Per_1_M_PPL'].to_string(index=False)
    country_metadata['Deaths/1M Pop'] = dataframe[dataframe['Country']==country]['Deaths_Per_1_M_PPL'].to_string(index=False)
    country_metadata['1st Case On'] = dataframe[dataframe['Country']==country]['1st_Case_On'].to_string(index=False)
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
    return jsonify(list(state_df["All India"]))

@app.route('/new')
def all_india_new_cases():
    """Return total new cases."""
    return jsonify(list(state_df.New))  
  

if __name__ == "__main__":
    app.run(debug=True)
   
    
