from flask import flash, redirect, render_template, url_for, jsonify
from flask.globals import request
from flask_login import login_required, current_user
import datetime
from . import dashboard
from .forms import FlightForm
from .. import db
from ..models import Flight, Process

processes = ["Deplanement", "Unloading", "Refuling", "Catering", "Cleaning", "Bording", "Loading", "Pushback"]

# list the ramp agent operated flights!
@dashboard.route('/flights', methods=['GET', 'POST'])
@login_required
def list_flights():
    """
    List all flights
    """
    flights = Flight.query.filter_by(rampagent_id = current_user.id)

    return render_template('dashboard/flights/flights.html', flights=flights)


def transform_date(date):
    transformed_date = ""
    months = {
        "01": "JAN",
        "02": "FEB",
        "03": "MAR",
        "04": "APR",
        "05": "MAY",
        "06": "JUN",
        "07": "JUL",
        "08": "AUG",
        "09": "SEP",
        "10": "OCT",
        "11": "NOV",
        "12": "DEC",
    }
    if date:
        date_split = date.split('-')
        if len(date_split) == 3:
            year = str(date_split[0])[-2:] #select the last 2 char , this is who the year is represented in the loadsheet
            month = date_split[1]
            day = date_split[2]
    else:
        return date
    for Mon_C, Mon_L in months.items():
        if Mon_C == month:
            month = Mon_L
    transformed_date = ''.join([day, month, year])
    return transformed_date

# dashboard to start the ramp operations!
@dashboard.route('/flights/<int:id>', methods=['GET', 'POST'])
@login_required
def start_operation(id):
    """
    render the ramp agent dashboard template
    start operations
    """

    flight = Flight.query.get_or_404(id)
    flight_data ={}
    flight_data["flight_number"] = flight.flight_number
    flight_data["departure"] = flight.departure
    flight_data["destination"] = flight.destination
    flight_data["aircraft_registration"] = flight.aircraft_registration
    flight_data["id"] = flight.id
    flight_data["date"] = flight.date

    return render_template('dashboard/rampdashboard.html', title="Dashboard", flight_data=flight_data)

# add a new flight
@dashboard.route('/flights/add', methods=['GET', 'POST'])
@login_required
def add_flight():
    """
    Add a flight to the database
    """
    #check current user
    add_flight = True
    form = FlightForm()
    if form.validate_on_submit():
        today = str(datetime.date.today())
        flight = Flight(flight_number=form.flight_number.data.upper(),
                        departure=form.departure.data.upper(),
                        destination=form.destination.data.upper(),
                        aircraft_registration=form.aircraft_registration.data.upper(),
                        date = transform_date(today),
                        rampagent_id = current_user.id)
        try:
            # add flight to the database and start ramp operations
            db.session.add(flight)
            db.session.commit()
            flash('You have successfully added a new flight.')
            return redirect(url_for('dashboard.start_operation', id=flight.id))
        except:
            # in case flight number already exists
            flash('Error: flight number already exists.')
            return redirect(url_for('dashboard.list_flights'))
        # redirect to departments page

    # load department template
    return render_template('dashboard/flights/flight.html', form=form, title="Add flight", add_flight=add_flight)



# edit a flight
@dashboard.route('/flights/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_flight(id):
    """
    Edit a flight
    """

    add_flight = False

    flight = Flight.query.get_or_404(id)
    form = FlightForm(obj=flight)
    if form.validate_on_submit():
        flight.flight_number = form.flight_number.data.upper()
        flight.departure = form.departure.data.upper()
        flight.destination = form.destination.data.upper()
        flight.aircraft_registration = form.aircraft_registration.data.upper()


        db.session.commit()
        flash('You have successfully edited the Flight.')

        # redirect to the flights page
        return redirect(url_for('dashboard.list_flights'))

    form.aircraft_registration.data = flight.aircraft_registration
    form.destination.data = flight.destination
    form.departure.data = flight.departure
    form.flight_number.data = flight.flight_number

    return render_template('dashboard/flights/flight.html', add_flight=add_flight, form=form,
                           flight=flight, title="Edit Flight")

@dashboard.route('/flights/Manual-Loadsheet', methods=['GET', 'POST'])
@login_required
def show_manual_loadsheet():
    """
    show manual loadsheet
    """
    return render_template('dashboard/loadsheet/manual.html')

@dashboard.route('/flights/EDP-Loadsheet', methods=['GET', 'POST'])
@login_required
def show_EDP_loadsheet():
    """
    show EDP loadsheet loadsheet
    """
    return render_template('dashboard/loadsheet/EDP.html')

# inside the tables section 1- list all flights operations data!
# with its specific search feature!
@dashboard.route('/list-operated_flights', methods=['GET', 'POST'])
@login_required
def operated_flights():
    """
    list all operated flights tables!
    """
    q = request.args.get('q')
    if q:
        flights = Flight.query.filter(Flight.flight_number.contains(q))
        processes = Process.query.all()
    else:
        flights = Flight.query.all()
        processes = Process.query.all()
    return render_template('dashboard/tables/operated_flights.html', flights=flights, processes=processes)

# inside the tables section 2- list all countries(departure or arrival) data! form the API based on the iata_code
# with its specific search feature!
@dashboard.route('/list-airports-IATA-code', methods=['GET', 'POST'])
@login_required
def iata_code():
    """
    list all flight tables!
    """
    from datapackage import Package
    package = Package('https://datahub.io/core/airport-codes/datapackage.json')
    # print list of all resources:
    print(package.resource_names)
    airport_data = []
    # print processed tabular data (if exists any)
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            print(type(resource))
            print(resource.schema.descriptor)
            for airport_code in resource.read(keyed=True):
                if airport_code["iata_code"] != None:
                    airport_data.append({"name": airport_code["name"], "municipality": airport_code["municipality"], "iso_country": airport_code["iso_country"], "ident": airport_code["ident"], "iata_code": airport_code["iata_code"]})
    return render_template('dashboard/tables/iata_code.html', airport_data=airport_data)

#### Processes ####

deplanement_data = []
@dashboard.route('/deplanement/<int:id>', methods=['POST'])
@login_required
def deplanement(id):
    flight = Flight.query.get_or_404(id)
    Status=""
    StartTime=""
    EndTime=""
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)
    print(dataGet)
    dataReply = {'backend_data':'hi there from python flask'}
    deplanement_data.append(dataGet)
    OneDeplanementPerFlight = Process.query.filter_by(flight_id=id, process_name="Deplanement").first()
    if OneDeplanementPerFlight == None: # There Still No flight with that flight_id
        deplanement = Process(process_name="Deplanement",
                            flight_id= flight.id,
                            rampagent_id = current_user.id)
        db.session.add(deplanement)
        db.session.commit()
        for item in deplanement_data:
            if next(iter(item)) == "status":
                print("this is the status: ")
                print(next(iter(item.items()))[1])
                Status = next(iter(item.items()))[1]
                if Status:
                    StatusUpdate = Process.query.get(deplanement.id)
                    StatusUpdate.status = Status
                    db.session.commit()
    else:
        deplanement = Process.query.filter_by(flight_id=id, process_name="Deplanement").first()
        print(deplanement_data)
        for item in deplanement_data:
            if next(iter(item)) == "StartTime":
                print("this is the StartTime: ")
                print(next(iter(item.items()))[1])
                StartTime = next(iter(item.items()))[1]
                if StartTime:
                    StartTimeUpdate = Process.query.get(deplanement.id)
                    if StartTimeUpdate.start_time == None:
                        StartTimeUpdate.start_time = StartTime
                        db.session.commit()

            if next(iter(item)) == "EndTime":
                print("this is the EndTime: ")
                print(next(iter(item.items()))[1])
                EndTime = next(iter(item.items()))[1]
                if EndTime:
                    EndTimeUpdate = Process.query.get(deplanement.id)
                    if EndTimeUpdate.end_time == None:
                        EndTimeUpdate.end_time = EndTime
                        db.session.commit()

    return jsonify(dataReply)


unloading_data = []
@dashboard.route('/unloading/<int:id>', methods=['POST'])
@login_required
def unloading(id):
    flight = Flight.query.get_or_404(id)
    Status=""
    StartTime=""
    EndTime=""
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)
    print(dataGet)
    dataReply = {'backend_data':'hi there from python flask'}
    unloading_data.append(dataGet)
    OneUnloadingPerFlight = Process.query.filter_by(flight_id=id, process_name="Unloading").first()
    if OneUnloadingPerFlight == None: # There Still No flight with that flight_id
        unloading = Process(process_name="Unloading",
                            flight_id= flight.id,
                            rampagent_id = current_user.id)
        db.session.add(unloading)
        db.session.commit()
        for item in unloading_data:
            if next(iter(item)) == "status":
                print("this is the status: ")
                print(next(iter(item.items()))[1])
                Status = next(iter(item.items()))[1]
                if Status:
                    StatusUpdate = Process.query.get(unloading.id)
                    StatusUpdate.status = Status
                    db.session.commit()

    else:
        unloading = Process.query.filter_by(flight_id=id, process_name="Unloading").first()
        for item in unloading_data:
            if next(iter(item)) == "StartTime":
                print("this is the StartTime: ")
                print(next(iter(item.items()))[1])
                StartTime = next(iter(item.items()))[1]
                if StartTime:
                    StartTimeUpdate = Process.query.get(unloading.id)
                    if StartTimeUpdate.start_time == None:

                        StartTimeUpdate.start_time = StartTime
                        db.session.commit()

            if next(iter(item)) == "EndTime":
                print("this is the EndTime: ")
                print(next(iter(item.items()))[1])
                EndTime = next(iter(item.items()))[1]
                if EndTime:
                    EndTimeUpdate = Process.query.get(unloading.id)
                    if EndTimeUpdate.end_time == None:
                        EndTimeUpdate.end_time = EndTime
                        db.session.commit()

    return jsonify(dataReply)



refuling_data = []
@dashboard.route('/refuling/<int:id>', methods=['POST'])
@login_required
def refuling(id):
    flight = Flight.query.get_or_404(id)
    Status=""
    StartTime=""
    EndTime=""
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)
    print(dataGet)
    dataReply = {'backend_data':'hi there from python flask'}
    refuling_data.append(dataGet)
    OneRefulingPerFlight = Process.query.filter_by(flight_id=id, process_name="Refuling").first()
    if OneRefulingPerFlight == None: # There Still No flight with that flight_id
        refuling = Process(process_name="Refuling",
                            flight_id= flight.id,
                            rampagent_id = current_user.id)
        db.session.add(refuling)
        db.session.commit()
        for item in refuling_data:
            if next(iter(item)) == "status":
                print("this is the status: ")
                print(next(iter(item.items()))[1])
                Status = next(iter(item.items()))[1]
                if Status:
                    StatusUpdate = Process.query.get(refuling.id)
                    StatusUpdate.status = Status
                    db.session.commit()

    else:
        refuling = Process.query.filter_by(flight_id=id, process_name="Refuling").first()
        for item in refuling_data:
            if next(iter(item)) == "StartTime":
                print("this is the StartTime: ")
                print(next(iter(item.items()))[1])
                StartTime = next(iter(item.items()))[1]
                if StartTime:
                    StartTimeUpdate = Process.query.get(refuling.id)
                    if StartTimeUpdate.start_time == None:
                        StartTimeUpdate.start_time = StartTime
                        db.session.commit()

            if next(iter(item)) == "EndTime":
                print("this is the EndTime: ")
                print(next(iter(item.items()))[1])
                EndTime = next(iter(item.items()))[1]
                if EndTime:
                    EndTimeUpdate = Process.query.get(refuling.id)
                    if EndTimeUpdate.end_time == None:
                        EndTimeUpdate.end_time = EndTime
                        db.session.commit()

    return jsonify(dataReply)


catering_data = []
@dashboard.route('/catering/<int:id>', methods=['POST'])
@login_required
def catering(id):
    flight = Flight.query.get_or_404(id)
    Status=""
    StartTime=""
    EndTime=""
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)
    print(dataGet)
    dataReply = {'backend_data':'hi there from python flask'}
    catering_data.append(dataGet)
    OneCateringPerFlight = Process.query.filter_by(flight_id=id, process_name="Catering").first()
    if OneCateringPerFlight == None: # There Still No flight with that flight_id
        catering = Process(process_name="Catering",
                            flight_id= flight.id,
                            rampagent_id = current_user.id)
        db.session.add(catering)
        db.session.commit()
        for item in catering_data:
            if next(iter(item)) == "status":
                print("this is the status: ")
                print(next(iter(item.items()))[1])
                Status = next(iter(item.items()))[1]
                if Status:
                    StatusUpdate = Process.query.get(catering.id)
                    StatusUpdate.status = Status
                    db.session.commit()

    else:
        catering = Process.query.filter_by(flight_id=id, process_name="Catering").first()
        for item in catering_data:
            if next(iter(item)) == "StartTime":
                print("this is the StartTime: ")
                print(next(iter(item.items()))[1])
                StartTime = next(iter(item.items()))[1]
                if StartTime:
                    StartTimeUpdate = Process.query.get(catering.id)
                    if StartTimeUpdate.start_time == None:
                        StartTimeUpdate.start_time = StartTime
                        db.session.commit()

            if next(iter(item)) == "EndTime":
                print("this is the EndTime: ")
                print(next(iter(item.items()))[1])
                EndTime = next(iter(item.items()))[1]
                if EndTime:
                    EndTimeUpdate = Process.query.get(catering.id)
                    if EndTimeUpdate.end_time == None:
                        EndTimeUpdate.end_time = EndTime
                        db.session.commit()

    return jsonify(dataReply)


cleaning_data = []
@dashboard.route('/cleaning/<int:id>', methods=['POST'])
@login_required
def cleaning(id):
    flight = Flight.query.get_or_404(id)
    Status=""
    StartTime=""
    EndTime=""
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)
    print(dataGet)
    dataReply = {'backend_data':'hi there from python flask'}
    cleaning_data.append(dataGet)
    OneCleaningPerFlight = Process.query.filter_by(flight_id=id, process_name="Cleaning").first()
    if OneCleaningPerFlight == None: # There Still No flight with that flight_id
        cleaning = Process(process_name="Cleaning",
                            flight_id= flight.id,
                            rampagent_id = current_user.id)
        db.session.add(cleaning)
        db.session.commit()
        for item in cleaning_data:
            if next(iter(item)) == "status":
                print("this is the status: ")
                print(next(iter(item.items()))[1])
                Status = next(iter(item.items()))[1]
                if Status:
                    StatusUpdate = Process.query.get(cleaning.id)
                    StatusUpdate.status = Status
                    db.session.commit()

    else:
        cleaning = Process.query.filter_by(flight_id=id, process_name="Cleaning").first()
        for item in cleaning_data:
            if next(iter(item)) == "StartTime":
                print("this is the StartTime: ")
                print(next(iter(item.items()))[1])
                StartTime = next(iter(item.items()))[1]
                if StartTime:
                    StartTimeUpdate = Process.query.get(cleaning.id)
                    if StartTimeUpdate.start_time == None:
                        StartTimeUpdate.start_time = StartTime
                        db.session.commit()

            if next(iter(item)) == "EndTime":
                print("this is the EndTime: ")
                print(next(iter(item.items()))[1])
                EndTime = next(iter(item.items()))[1]
                if EndTime:
                    EndTimeUpdate = Process.query.get(cleaning.id)
                    if EndTimeUpdate.end_time == None:
                        EndTimeUpdate.end_time = EndTime
                        db.session.commit()

    return jsonify(dataReply)

bording_data = []
@dashboard.route('/bording/<int:id>', methods=['POST'])
@login_required
def bording(id):
    flight = Flight.query.get_or_404(id)
    Status=""
    StartTime=""
    EndTime=""
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)
    print(dataGet)
    dataReply = {'backend_data':'hi there from python flask'}
    bording_data.append(dataGet)
    OneBordingPerFlight = Process.query.filter_by(flight_id=id, process_name="Bording").first()
    if OneBordingPerFlight == None: # There Still No flight with that flight_id
        bording = Process(process_name="Bording",
                            flight_id= flight.id,
                            rampagent_id = current_user.id)
        db.session.add(bording)
        db.session.commit()
        for item in bording_data:
            if next(iter(item)) == "status":
                print("this is the status: ")
                print(next(iter(item.items()))[1])
                Status = next(iter(item.items()))[1]
                if Status:
                    StatusUpdate = Process.query.get(bording.id)
                    StatusUpdate.status = Status
                    db.session.commit()

    else:
        bording = Process.query.filter_by(flight_id=id, process_name="Bording").first()
        for item in bording_data:
            if next(iter(item)) == "StartTime":
                print("this is the StartTime: ")
                print(next(iter(item.items()))[1])
                StartTime = next(iter(item.items()))[1]
                if StartTime:
                    StartTimeUpdate = Process.query.get(bording.id)
                    if StartTimeUpdate.start_time == None:
                        StartTimeUpdate.start_time = StartTime
                        db.session.commit()

            if next(iter(item)) == "EndTime":
                print("this is the EndTime: ")
                print(next(iter(item.items()))[1])
                EndTime = next(iter(item.items()))[1]
                if EndTime:
                    EndTimeUpdate = Process.query.get(bording.id)
                    if EndTimeUpdate.end_time == None:
                        EndTimeUpdate.end_time = EndTime
                        db.session.commit()

    return jsonify(dataReply)


loading_data = []
@dashboard.route('/loading/<int:id>', methods=['POST'])
@login_required
def loading(id):
    flight = Flight.query.get_or_404(id)
    Status=""
    StartTime=""
    EndTime=""
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)
    print(dataGet)
    dataReply = {'backend_data':'hi there from python flask'}
    loading_data.append(dataGet)
    OneLoadingPerFlight = Process.query.filter_by(flight_id=id, process_name="Loading").first()
    if OneLoadingPerFlight == None: # There Still No flight with that flight_id
        loading = Process(process_name="Loading",
                            flight_id= flight.id,
                            rampagent_id = current_user.id)
        db.session.add(loading)
        db.session.commit()
        for item in loading_data:
            if next(iter(item)) == "status":
                print("this is the status: ")
                print(next(iter(item.items()))[1])
                Status = next(iter(item.items()))[1]
                if Status:
                    StatusUpdate = Process.query.get(loading.id)
                    StatusUpdate.status = Status
                    db.session.commit()

    else:
        loading = Process.query.filter_by(flight_id=id, process_name="Loading").first()
        for item in loading_data:
            if next(iter(item)) == "StartTime":
                print("this is the StartTime: ")
                print(next(iter(item.items()))[1])
                StartTime = next(iter(item.items()))[1]
                if StartTime:
                    StartTimeUpdate = Process.query.get(loading.id)
                    if StartTimeUpdate.start_time == None:
                        StartTimeUpdate.start_time = StartTime
                        db.session.commit()

            if next(iter(item)) == "EndTime":
                print("this is the EndTime: ")
                print(next(iter(item.items()))[1])
                EndTime = next(iter(item.items()))[1]
                if EndTime:
                    EndTimeUpdate = Process.query.get(loading.id)
                    if EndTimeUpdate.end_time == None:
                        EndTimeUpdate.end_time = EndTime
                        db.session.commit()

    return jsonify(dataReply)


pushback_data = []
@dashboard.route('/pushback/<int:id>', methods=['POST'])
@login_required
def pushback(id):
    flight = Flight.query.get_or_404(id)
    Status=""
    StartTime=""
    EndTime=""
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)
    print(dataGet)
    dataReply = {'backend_data':'hi there from python flask'}
    pushback_data.append(dataGet)
    OnePushbackPerFlight = Process.query.filter_by(flight_id=id, process_name="Pushback").first()
    if OnePushbackPerFlight == None: # There Still No flight with that flight_id
        pushback = Process(process_name="Pushback",
                            flight_id= flight.id,
                            rampagent_id = current_user.id)
        db.session.add(pushback)
        db.session.commit()
        for item in pushback_data:
            if next(iter(item)) == "status":
                print("this is the status: ")
                print(next(iter(item.items()))[1])
                Status = next(iter(item.items()))[1]
                if Status:
                    StatusUpdate = Process.query.get(pushback.id)
                    StatusUpdate.status = Status
                    db.session.commit()

    else:
        pushback = Process.query.filter_by(flight_id=id, process_name="Pushback").first()
        for item in pushback_data:
            if next(iter(item)) == "StartTime":
                print("this is the StartTime: ")
                print(next(iter(item.items()))[1])
                StartTime = next(iter(item.items()))[1]
                if StartTime:
                    StartTimeUpdate = Process.query.get(pushback.id)
                    if StartTimeUpdate.start_time == None:
                        StartTimeUpdate.start_time = StartTime
                        db.session.commit()

            if next(iter(item)) == "EndTime":
                print("this is the EndTime: ")
                print(next(iter(item.items()))[1])
                EndTime = next(iter(item.items()))[1]
                if EndTime:
                    EndTimeUpdate = Process.query.get(pushback.id)
                    if EndTimeUpdate.end_time == None:
                        EndTimeUpdate.end_time = EndTime
                        db.session.commit()
    return jsonify(dataReply)