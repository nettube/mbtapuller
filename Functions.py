from geopy.distance import vincenty
from Classes import Station


def current_station(trip_record, session):
    """
    Find the current station that a TripRecord is at.

    Example return: Harvard station object, Alewife station object
    Example if the train is not within 400 of a station: None

    :param trip_record: The TripRecord object to evaluate.
    :param session: The database session to use for data queries
    :return: A Station object
    """
    all_stations = session.query(Station).all()
    for station in all_stations:
        us = (trip_record.location_lat, trip_record.location_lng)
        it = (station.location_lat, station.location_lng)

        if vincenty(us, it).feet <= 400:
            return station

    return None
