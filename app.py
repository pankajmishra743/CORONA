
from flask import Flask, jsonify, render_template, request, flash, redirect
from pandasql import sqldf
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import io
import requests
import responses
# State Wise Case Data
url_case = 'https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data/India_medical_cases_by_state_and_union_territory'
page_case = requests.get(url_case)
soup_case = BeautifulSoup(page_case.content, 'html.parser')
table_scrapped_case = soup_case.find('table',{'class':'wikitable plainrowheaders sortable'})
tab_data_case = [[cell.text for cell in row.find_all(["th","td"])]
                        for row in table_scrapped_case.find_all("tr")]
st_df = pd.DataFrame(tab_data_case)
st_df = st_df.iloc[3:-2]
st_df.replace(r'\n','', regex=True, inplace=True)
st_df = st_df.replace(to_replace ='\(.*\)', value = '', regex = True) 
st_df = st_df.replace(to_replace ='\[.*\]', value = '', regex = True)
st_df = st_df.replace(to_replace =',', value = '', regex = True)
st_df.columns = ['STATE_UT','TOTAL', 'DEATHS','RECOVERIES', 'ACTIVE_CASES'] 
Total =  [pd.to_numeric(st_df.iloc[:, 1], errors='coerce').fillna(0).astype(int).sum(),
          pd.to_numeric(st_df.iloc[:, 2], errors='coerce').fillna(0).astype(int).sum(),
          pd.to_numeric(st_df.iloc[:, 3], errors='coerce').fillna(0).astype(int).sum(),
          pd.to_numeric(st_df.iloc[:, 4], errors='coerce').fillna(0).astype(int).sum()]
new_row = pd.DataFrame({'STATE_UT':'All India', 'TOTAL':Total[0], 'DEATHS':Total[1], 'RECOVERIES':Total[2], 'ACTIVE_CASES':Total[3]}, index =[0])
final_df = pd.concat([new_row, st_df]).reset_index(drop = True)

# Date wise State Data
# wikitable mw-collapsible mw-collapsed
url_dateWise = 'https://en.wikipedia.org/wiki/COVID-19_pandemic_in_India/Statistics'
page_dateWise = requests.get(url_dateWise)
soup_dateWise = BeautifulSoup(page_dateWise.content, 'html.parser')
table_scrapped_dateWise = soup_dateWise.find('table',{'class':'wikitable mw-collapsible mw-datatable'}) 
tab_data_dateWise = [[cell.text for cell in row.find_all(["th","td"])]
                        for row in table_scrapped_dateWise.find_all("tr")]
state_df = pd.DataFrame(tab_data_dateWise)
state_df.replace(r'\n','', regex=True, inplace=True)
state_df = state_df.replace(to_replace ='\(.*\)', value = '', regex = True) 
state_df.fillna(0, inplace=True)
state_df = state_df.iloc[:, :-4]
state_df = state_df.iloc[2:-4]

cols = [36]
state_df.drop(state_df.columns[cols],axis=1,inplace=True)
state_df.insert(19, "Lakshadweep", '0')
ColumnName = final_df['STATE_UT'].tolist()
ColumnName.append('New')
ColumnName.append(ColumnName.pop(ColumnName.index('All India')))
ColumnName.insert(0, "Date")
state_df.columns = ColumnName

# for world analysis

url = 'https://www.worldometers.info/coronavirus'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
tables = soup.find_all("table")
table = tables[1]
tab_data = [[cell.text for cell in row.find_all(["th","td"])]
                        for row in table.find_all("tr")]
dataframe = pd.DataFrame(tab_data)
dataframe.drop(dataframe.columns[[0,7,14,15,16,17,18]], axis = 1, inplace=True)
# dataframe.columns = df.iloc[0]
dataframe.columns = ['Country', 'Total_Cases', 'New_Cases', 'Total_Deaths','New_Deaths', 'Total_Recovered', 'Active_Cases',
                     'Serious_Critical','Total_Cases_Per_1_M_PPL', 'Deaths_Per_1_M_PPL', 'Total_Tests', 'Total_Tests_Per_1_M_PPL']
dataframe = dataframe.loc[dataframe['Country'].isin(['India','USA','China','Japan','S. Korea','Italy','Taiwan'])]
dataframe.replace(to_replace =',', value = '', regex = True, inplace=True)
dataframe.replace(to_replace ="S. Korea", value ="South Korea", inplace=True)
dataframe.fillna(0, inplace=True)
dataframe = dataframe.convert_objects(convert_numeric=True).fillna(0)
dataframe.reset_index(inplace = True, drop = True)
Abbr = ['CH', 'US', 'IN', 'IT', 'JP','SK', 'TW']
dataframe['Abbr'] = Abbr
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
    state_metadata = {}
    state_metadata['Active Cases'] = ldf[ldf['STATE_UT']==state]['ACTIVE_CASES'].to_string(index=False)
    state_metadata['Recoveries'] = ldf[ldf['STATE_UT']==state]['RECOVERIES'].to_string(index=False)
    state_metadata['Deaths'] = ldf[ldf['STATE_UT']==state]['DEATHS'].to_string(index=False)
    state_metadata['TOTAL'] = ldf[ldf['STATE_UT']==state]['TOTAL'].to_string(index=False)
    return jsonify(state_metadata)
    
@app.route('/mdata/<state>')
def sample_mdata(state):
    """Return the MetaData for a given State."""
    final_list = [None] * 4
    final_list[0] = final_df[final_df['STATE_UT']==state]['ACTIVE_CASES'].to_string(index=False)
    final_list[1] = final_df[final_df['STATE_UT']==state]['DEATHS'].to_string(index=False)
    final_list[2] = final_df[final_df['STATE_UT']==state]['RECOVERIES'].to_string(index=False)
    final_list[3] = final_df[final_df['STATE_UT']==state]['TOTAL'].to_string(index=False)
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
    return jsonify(dataframe[dataframe['Country']=="India"]['Total_Cases'])
  
@app.route('/invsus')
def INvsUS():
    """Return Tableau graphs html page"""
    return render_template("India VS USA-COVID.html")
          
if __name__ == "__main__":
    app.run(debug=True)
   
    
