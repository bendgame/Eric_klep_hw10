#Eric Kleppen Hw 10 flask app
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"<br/>"
        f"Use the following rountes with a start date or a start and end date<br/>"
        f"For example:"
        f"/api/v1.0/2017-01-01/2017-12-31"
        f"<br/>"
        f"/api/v1.0/<start><br/>" 
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    """List dates and precipitation."""
    results = session.query(Measurement.date, Measurement.prcp).all()
    #prcp_meas = list(np.ravel(results))
    
    prcp_meas = []
    for row in results:
        prcpDict = {row[0]:row[1]}
        prcp_meas.append(prcpDict)

    return jsonify(prcp_meas)

@app.route("/api/v1.0/stations")
def station():
    """List all stations."""
    results = session.query(Station.name).distinct().all()
    stations = list(np.ravel(results))
    
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """List all temperature observations."""
    maxdate = session.query(func.max(Measurement.date)).first()
    maxdate = list(maxdate)

    startdate = dt.datetime.strptime(maxdate[0], "%Y-%m-%d")- dt.timedelta(days=366)

    results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= startdate).all()
    
    tobs = list(np.ravel(results))
    
    return jsonify(tobs)

@app.route("/api/v1.0/<start_date>")
def startDate(start_date):
    """List min, avg and max."""
    results =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
    temps = list(np.ravel(results))
    
    return jsonify(temps)

@app.route("/api/v1.0/<start_date>/<end_date>")
def dateRange(start_date, end_date):
   
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    temps = list(np.ravel(results))
    
    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)
