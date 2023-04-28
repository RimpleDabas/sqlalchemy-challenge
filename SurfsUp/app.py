# Import the dependencies.

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
Base.classes.keys()

# list the columns for measurement  and station table
inspector = inspect(engine)
columns = inspector.get_columns('measurement')
for c in columns:
    print(c['name'], c["type"])

inspector = inspect(engine)
columns = inspector.get_columns('station')
for c in columns:
    print(c['name'], c["type"])
# Save references to each table
Measurements = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine) 

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
        )
#################################################
# Precipitation Route

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    recent_date = dt.datetime(2017, 8, 23)
# Calculate the date one year from the last date in data set.
    query_date = recent_date - dt.timedelta(days = 366)
# Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurements.date, 
                        Measurements.prcp).\
                  filter(Measurements.date > query_date).all()
    session.close()
#create an empty list to get all the key value pairs from the above query results by looping and appending the list
    result_list = []
    for date,prcp in results:
        result_dict = {}
        result_dict['date'] = date
        result_dict['precipiation'] = prcp
        result_list.append(result_dict)

    return jsonify(result_list)

#################################################
# Station Route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    query_result = session.query(Stations.station,Stations.name).all()
    session.close()
    #create an empty list to get all the key value pairs from the above query results by looping and appending the list
    stations_list = []
    for station,name in query_result:
        stations_dict = {}
        stations_dict['Station'] = station
        stations_dict['Name'] = name
        stations_list.append(stations_dict)

    return jsonify(stations_list)
    
#################################################
# Tobs Route 
@app.route("/api/v1.0/tobs")
def tobs():
    recent_date = dt.datetime(2017, 8, 23)
# Calculate the date one year from the last date in data set.
    query_date = recent_date - dt.timedelta(days = 366)
    session = Session(engine)
    query_tobs = session.query(Measurements.date,Measurements.tobs).\
        filter(Measurements.station ==  'USC00519281').filter(Measurements.date > query_date).all()
    session.close()
    #create an empty list to get all the key value pairs from the above query results by looping and appending the list
    tobs_list = []
    for date,tobs in query_tobs:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['temperature'] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)
    
#################################################
# start and start/end route
# @app.route("/api/v1.0/<start>")
# def start_date(start):
#     session = Session(engine)
#     query_start = session.query(Measurements.date,func.min(Measurements.tobs),\
#                                 func.max(Measurements.tobs),func.avg(Measurements.tobs)).filter(Measurements.date>=start).all()
#     session.close()
#     start_list = []
#     for date,min,max,avg in query_start:
#         start_dict = {}
#         start_dict['date'] = date
#         start_dict['min'] = min
#         start_dict['max'] = max
#         start_dict['average'] = avg
#         start_list.append(start_dict)
#     return jsonify(start_list)

if __name__ == '__main__':
    app.run(debug=True)