import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
app = Flask(__name__)
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect =True)
measurement = Base.classes.measurement
station = Base.classes.station
session =Session(engine)
year_ago= dt.date(2017,8,23)-dt.timedelta(days=365)

@app.route("/")
def welcome():
    return (f"Welcome to my API these are the routes you can use <br>" +  "/api/v1.0/precipitation <br>" + "/api/v1.0/stations<br>" +  "/api/v1.0/tobs<br>" + "/api/v1.0/temp/start <br>" + "/api/v1.0/temp/start/end <br>")
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago_prcp = session.query(measurement.prcp, measurement.date).filter(measurement.date >=year_ago).all()
    data=[]
    for prcp, date in year_ago_prcp:
        data.append({date:prcp})
        
    return(jsonify(data))

@app.route("/api/v1.0/stations")
def stations():
    wassup=session.query(station.station).all()
    data=[]
    for adsf in wassup:
        data.append(adsf)
    return(jsonify(data))

@app.route("/api/v1.0/tobs")
def tobs():
    popular=session.query(measurement.date,measurement.tobs)\
    .filter(measurement.date>=year_ago)\
    .filter(measurement.station=='USC00519281')\
    .all()
    return(jsonify(popular))

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def start(start=None,end=None):
    if not end:
        hat =session.query(func.min(measurement.tobs)\
        ,func.max(measurement.tobs)\
        ,func.avg(measurement.tobs))\
        .filter(measurement.date>=start)\
        .all()
        hatlist=list(np.ravel(hat))
        data ={"min":hatlist[0], "max": hatlist[1],"avg": hatlist[2]}
        
        return(jsonify(data))
    hat =session.query(func.min(measurement.tobs)\
    ,func.max(measurement.tobs)\
    ,func.avg(measurement.tobs))\
    .filter(measurement.date>=start)\
    .filter(measurement.date<=end)\
    .all()
    hatlist=list(np.ravel(hat))
    data ={"min":hatlist[0], "max": hatlist[1],"avg": hatlist[2]}
    return(jsonify(data))
    



if __name__ == '__main__':
    app.run()

