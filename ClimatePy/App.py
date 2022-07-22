from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
# Home page displays available routes
@app.route("/")
def home():
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start><end><br>"
            )

# Returns a JSON representation of a date and precipitation dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_date = session.query(Measurement.date, Measurement.prcp)   
    prcp_date_dict = dict(prcp_date)
    return jsonify(prcp_date_dict)

# Returns a JSON list of stations and counts from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Measurement.station, func.count(Measurement.date)).group_by(Measurement.station).all()
    stations_dict = dict(stations)
    return jsonify(stations_dict)

# Queries the dates and temperature observations (TOBS) of the most active station for the last year of data, returns in JSON format
@app.route("/api/v1.0/tobs")
def tobs():
    tobs = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.date.desc() >= "2016-08-23").all()
    tobs_dict = dict(tobs)
    return jsonify(tobs_dict)

#@app.route('/api/v1.0/<start>', defaults={'end': None})
#@app.route('/api/v1.0/<start><end>')

if __name__ == '__main__':
    app.run(debug=True)


### Sorry, could not get the rest finished in time ###