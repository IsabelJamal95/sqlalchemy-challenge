import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement= Base.classes.measurement
Station= Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
session = Session(engine)

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
        f"/api/v1.0/July<br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter (Measurement.date >= prev_year).all()
   return jsonify(precipitation)

    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = session.query(Station.station).all()
    session.close()
   
    return jsonify(stations)
    

@app.route("/api/v1.0/tobs")
def tobs():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temperature = session.query(Measurement.date, Measurement.tobs).\
     filter (Measurement.station == "USC00519281").\
     filter (Measurement.date >= prev_year).all()
    
    return jsonify(temperature)

@app.route("/api/v1.0/julytrip")
def julytrip():
    start_date = dt.date(2017, 7, 4)
    end_date = dt.date(2017, 7, 11)
    
    TMIN = session.query(func.min(Measurement.tobs)).\
     filter(Measurement.date >= start_date).\
     filter(Measurement.date <= end_date).all()

    TMAX = session.query(func.max(Measurement.tobs)).\
     filter(Measurement.date >= start_date).\
     filter(Measurement.date <= end_date).all()

    TAVG = session.query(func.avg(Measurement.tobs)).\
     filter(Measurement.date >= start_date).\
     filter(Measurement.date <= end_date).all()
     
    return jsonify(TMIN, TMAX, TAVG)

    

   

                                                 
    


if __name__ == '__main__':
    app.run(debug=True)
