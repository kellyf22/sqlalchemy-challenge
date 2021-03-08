
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaiian Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Convert the query results to a dictionary using date as the key and prcp as the value."""
    results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= '2016-08-23').all()
    session.close()

    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip.append(precip_dict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query should retrieve all stations
    results = session.query(Station.station).all()
    session.close()

    #Return a JSON list of stations
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query dates and tobs of the most active station for the last year
    results = session.query(Measurement.date, Measurement.tobs, Measurement.station).\
                            filter(Measurement.station == 'USC00519281').\
                            filter(Measurement.date >= '2016-08-17').all()
    session.close()

    temp_obs = []
    for entry in results:
        tobs_dict = {}
        tobs_dict[entry[0]] = entry[1]
        temp_obs.append(tobs_dict)

    return jsonify(temp_obs)
    # #tobs_yr = np.ravel(results)
    #return list(np.ravel(results))
    #return jsonify(results)
    #need to pull station id out of this IOT return just a list of temps(?)

@app.route("/api/v1.0/<start>")
# Calculate TMin, TAvg, and TMax for all dates >= start date
def after(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    return(
        f"Minimum temp: {min_temp}<br/>"
        f"Maximum temp: {max_temp}<br/>"
        f"Average temp: {avg_temp}")

@app.route("/api/v1.0/<start>/<end>")
# Calculate TMin, TAvg, and TMax for all dates between start and end date
def between(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return(
        f"Minimum temp: {min_temp}<br/>"
        f"Maximum temp: {max_temp}<br/>"
        f"Average temp: {avg_temp}")

if __name__ == "__main__":
    app.run(debug=True)
