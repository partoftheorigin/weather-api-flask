import dateutil.parser
from getweather import get_weather
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer)
    city = db.Column(db.String(50))
    country = db.Column(db.String(30))
    date = db.Column(db.String(20))
    description = db.Column(db.String(50))


# All cities in the system
@app.route("/city", methods=["GET"])
def get_all_cities():
    cities = City.query.all()
    output = []
    for city in cities:
        city_data = {}
        city_data['id'] = city.id
        city_data['name'] = city.name
        city_data['country'] = city.country
        output.append(city_data)
    return jsonify({'cities': output})


# Add a new city to the system
@app.route('/city', methods=['POST'])
def add_city():
    city = request.args.get('city', '')
    country = request.args.get('country', '')
    new_city = City(name=city, country=country)
    db.session.add(new_city)
    db.session.commit()
    return jsonify({'message': 'new city added'})


# Get a city details by id
@app.route("/city/<int:id>", methods=["GET"])
def get_one_city(id):
    city = City.query.filter_by(id=id).first()
    if not city:
        return jsonify({"messsage": "No City Found"})
    city_data = {}
    city_data['name'] = city.name
    city_data['country'] = city.country
    return jsonify({"city": city_data})


# Delete a city by id
@app.route("/city/<int:id>", methods=["DELETE"])
def delete_city(id):
    city = City.query.filter_by(id=id).first()
    if not city:
        return jsonify({"messsage": "No City Found"})
    db.session.delete(city)
    db.session.commit()
    return jsonify({'message': 'City Deleted'})


# Get weather of all cities for last 5 days
@app.route('/weather/allcities', methods=['GET'])
def get_weather_all():
    reports = Weather.query.all()
    output = list()
    for report in reports:
        report_date = dateutil.parser.parse(report.date)
        if (datetime.now() - report_date).days < 6:
            weather_data = dict()
            weather_data['id'] = report.id
            weather_data['name'] = report.city
            weather_data['country'] = report.country
            weather_data['temperature'] = report.temperature
            weather_data['date'] = report.date
            weather_data['description'] = report.description
            output.append(weather_data)
    return jsonify({'weather': output})


# Get weather report by city and date filter
@app.route('/weather/filter', methods=['GET'])
def get_weather_filter():
    city = request.args.get('city', '')
    date = request.args.get('date', '')
    reports = Weather.query.all()
    output = list()
    for report in reports:
        if report.city == city and date in report.date:
            weather_data = dict()
            weather_data['id'] = report.id
            weather_data['name'] = report.city
            weather_data['country'] = report.country
            weather_data['temperature'] = report.temperature
            weather_data['date'] = report.date
            weather_data['description'] = report.description
            output.append(weather_data)
    return jsonify({'weather': output})


# Get weather report for a given city and store data in database
@app.route('/weather', methods=['POST'])
def get_report():
    city = request.args.get('city', '')
    country = request.args.get('country', '')
    report = get_weather(city, country)
    new_report = Weather(city=report['city'], country=report['country'], temperature=report['temperature'], date=report['date'], description=report['description'])
    db.session.add(new_report)
    db.session.commit()
    return jsonify({'message': 'new report added'})


# Update a particular weather report by id
@app.route('/weather/<int:id>', methods=['PUT'])
def update_report(id):
    report = Weather.query.filter_by(id=id).first()
    print(report.city)
    data = request.get_json()
    report.temperature = data['temperature']
    report.city = data['city']
    report.country = data['country']
    report.date = data['date']
    db.session.commit()
    return jsonify({'message': 'Report Updated'})


# Delete a particular weather report by id
@app.route('/weather/<int:id>', methods=['DELETE'])
def delete_report(id):
    report = Weather.query.filter_by(id=id).first()
    if not report:
        return jsonify({"messsage": "No Report Found"})
    db.session.delete(report)
    db.session.commit()
    return jsonify({'message': 'Report Deleted'})


def job_function():
    report = get_weather(Bangalore, IN)
    new_report = Weather(city=report['city'], country=report['country'], temperature=report['temperature'],
                         date=report['date'], description=report['description'])
    db.session.add(new_report)
    db.session.commit()
    return jsonify({'message': 'new report added'})


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    sched = BlockingScheduler()
    # Schedule job_function to be called every twenty four hours
    sched.add_job(job_function, 'interval', hours=24, start_date='2017-12-13 17:00:00')
    sched.start()
