from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    schema_version: Optional[float] = None
    asset_type: Optional[str] = None
    asset_id: Optional[str] = None
    event_type: Optional[str] = None
    location_description: Optional[str] = None
    location_id: Optional[str] = None
    asset_latitude: Optional[float] = None
    asset_longitude: Optional[float] = None
    lat_long_acc: Optional[float] = None
    created_ts: Optional[str] = None
    altitude: Optional[float] = None
    heading: Optional[float] = None
    speed: Optional[float] = None
    speed_accuracy: Optional[float] = None
    course: Optional[float] = None
    course_accuracy: Optional[float] = None
    datasource: Optional[str] = None
    properties_dict: Optional[str] = None


class PostgresSchemaDto:
    schema_version: Optional[float] = None
    asset_type: Optional[str] = None
    asset_id: Optional[str] = None
    event_type: Optional[str] = None
    location_description: Optional[str] = None
    location_id: Optional[str] = None
    asset_latitude: Optional[float] = None
    asset_longitude: Optional[float] = None
    lat_long_acc: Optional[float] = None
    created_ts: Optional[str] = None
    altitude: Optional[float] = None
    heading: Optional[float] = None
    speed: Optional[float] = None
    speed_accuracy: Optional[float] = None
    course: Optional[float] = None
    course_accuracy: Optional[float] = None
    datasource: Optional[str] = None
    properties_dict: Optional[str] = None

    def __init__(self, schema_version=None, asset_type=None, asset_id=None, event_type=None, location_description=None, location_id=None,
                 asset_latitude=None, asset_longitude=None, lat_long_acc=None, created_ts=None, altitude=None, heading=None,
                 speed=None, speed_accuracy=None, course=None, course_accuracy=None,
                 datasource=None, properties_dict=None):
        self.schema_version = schema_version
        self.asset_type = asset_type
        self.asset_id = asset_id
        self.event_type = event_type
        self.location_description = location_description
        self.location_id = location_id
        self.asset_latitude = asset_latitude
        self.asset_longitude = asset_longitude
        self.lat_long_acc = lat_long_acc
        self.created_ts = created_ts
        self.altitude = altitude
        self.heading = heading
        self.speed = speed
        self.speed_accuracy = speed_accuracy
        self.course = course
        self.course_accuracy = course_accuracy
        self.datasource = datasource
        self.properties_dict = properties_dict

    # Getter methods
    def get_schema_version(self):
        return self.schema_version

    def get_asset_type(self):
        return self.asset_type

    def get_asset_id(self):
        return self.asset_id

    def get_event_type(self):
        return self.event_type

    def get_location_description(self):
        return self.location_description

    def get_location_id(self):
        return self.location_id

    def get_asset_latitude(self):
        return self.asset_latitude

    def get_asset_longitude(self):
        return self.asset_longitude

    def get_lat_long_acc(self):
        return self.lat_long_acc

    def get_created_ts(self):
        return self.created_ts

    def get_altitude(self):
        return self.altitude

    def get_heading(self):
        return self.heading

    def get_speed(self):
        return self.speed

    def get_speed_accuracy(self):
        return self.speed_accuracy

    def get_course(self):
        return self.course

    def get_course_accuracy(self):
        return self.course_accuracy

    def get_datasource(self):
        return self.datasource

    def get_properties_dict(self):
        return self.properties_dict

    # Setter methods
    def set_schema_version(self, value):
        self.schema_version = value

    def set_asset_type(self, value):
        self.asset_type = value

    def set_asset_id(self, value):
        self.asset_id = value

    def set_event_type(self, value):
        self.event_type = value

    def set_location_description(self, value):
        self.location_description = value

    def set_location_id(self, value):
        self.location_id = value

    def set_asset_latitude(self, value):
        self.asset_latitude = value

    def set_asset_longitude(self, value):
        self.asset_longitude = value

    def set_lat_long_acc(self, value):
        self.lat_long_acc = value

    def set_created_ts(self, value):
        self.created_ts = value

    def set_altitude(self, value):
        self.altitude = value

    def set_heading(self, value):
        self.heading = value

    def set_speed(self, value):
        self.speed = value

    def set_speed_accuracy(self, value):
        self.speed_accuracy = value

    def set_course(self, value):
        self.course = value

    def set_course_accuracy(self, value):
        self.course_accuracy = value

    def set_datasource(self, value):
        self.datasource = value

    def set_properties_dict(self, value):
        self.properties_dict = value

    def __dict__(self):
        return {
            'schema_version': self.schema_version,
            'asset_type': self.asset_type,
            'asset_id': self.asset_id,
            'event_type': self.event_type,
            'location_description': self.location_description,
            'location_id': self.location_id,
            'asset_latitude': self.asset_latitude,
            'asset_longitude': self.asset_longitude,
            'lat_long_acc': self.lat_long_acc,
            'created_ts': self.created_ts,
            'altitude': self.altitude,
            'heading': self.heading,
            'speed': self.speed,
            'speed_accuracy': self.speed_accuracy,
            'course': self.course,
            'course_accuracy': self.course_accuracy,
            'datasource': self.datasource,
            'properties_dict': self.properties_dict
        }

    def __str__(self):
        return f"{self.schema_version}, \'{self.asset_type}\', \'{self.asset_id}\', \'{self.event_type}\', \'{self.location_description}\', " \
               f"\'{self.location_id}\', {self.asset_latitude}, {self.asset_longitude}, {self.lat_long_acc}, \'{self.created_ts}\', " \
               f"{self.altitude}, {self.heading}, {self.speed}, {self.speed_accuracy}, {self.course}, {self.course_accuracy}, " \
               f"\'{self.datasource}\', \'{self.properties_dict}\'"