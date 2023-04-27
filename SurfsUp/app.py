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
    
    station_dict = dict(query_result)
    return jsonify(station_dict)
    
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
    
    tobs_dict = dict(query_tobs)
    return jsonify(tobs_dict)
    

if __name__ == '__main__':
    app.run(debug=True)