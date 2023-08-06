class PostgresSchemaDto:
    def __init__(self, schema_version=None, asset_type=None, asset_id=None, store_id=None, location_description=None, location_id=None,
                 asset_latitude=None, asset_longitude=None, location_radius=None, location_latitude=None,
                 location_longitude=None, asset=None, event=None, created_ts=None, created_dt=None, updated_ts=None,
                 altitude=None, heading=None, speed=None, speed_accuracy=None, course=None, course_accuracy=None,
                 datasource=None, properties_dict=None):
        self.schema_version = schema_version
        self.asset_type = asset_type
        self.asset_id = asset_id
        self.store_id = store_id
        self.location_description = location_description
        self.location_id = location_id
        self.asset_latitude = asset_latitude
        self.asset_longitude = asset_longitude
        self.location_radius = location_radius
        self.location_latitude = location_latitude
        self.location_longitude = location_longitude
        self.asset = asset
        self.event = event
        self.created_dt = created_dt
        self.created_ts = created_ts
        self.updated_ts = updated_ts
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

    def get_store_id(self):
        return self.store_id

    def get_location_description(self):
        return self.location_description

    def get_location_id(self):
        return self.location_id

    def get_asset_latitude(self):
        return self.asset_latitude

    def get_asset_longitude(self):
        return self.asset_longitude

    def get_location_radius(self):
        return self.location_radius

    def get_location_latitude(self):
        return self.location_latitude

    def get_location_longitude(self):
        return self.location_longitude

    def get_asset(self):
        return self.asset

    def get_event(self):
        return self.event

    def get_created_dt(self):
        return self.created_dt

    def get_created_ts(self):
        return self.created_ts

    def get_updated_ts(self):
        return self.updated_ts

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

    def set_store_id(self, value):
        self.store_id = value

    def set_location_description(self, value):
        self.location_description = value

    def set_location_id(self, value):
        self.location_id = value

    def set_asset_latitude(self, value):
        self.asset_latitude = value

    def set_asset_longitude(self, value):
        self.asset_longitude = value

    def set_location_radius(self, value):
        self.location_radius = value

    def set_location_latitude(self, value):
        self.location_latitude = value

    def set_location_longitude(self, value):
        self.location_longitude = value

    def set_asset(self, value):
        self.asset = value

    def set_event(self, value):
        self.event = value

    def set_created_dt(self, value):
        self.created_dt = value

    def set_created_ts(self, value):
        self.created_ts = value

    def set_updated_ts(self, value):
        self.updated_ts = value

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
            'store_id': self.store_id,
            'location_description': self.location_description,
            'location_id': self.location_id,
            'asset_latitude': self.asset_latitude,
            'asset_longitude': self.asset_longitude,
            'location_radius': self.location_radius,
            'location_latitude': self.location_latitude,
            'location_longitude': self.location_longitude,
            'asset': self.asset,
            'event': self.event,
            'created_dt': self.created_dt,
            'created_ts': self.created_ts,
            'updated_ts': self.updated_ts,
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
        return f"{self.schema_version}, \'{self.asset_type}\', \'{self.asset_id}\', \'{self.store_id}\', \'{self.location_description}\', \'{self.location_id}\', " \
               f"{self.asset_latitude}, {self.asset_longitude}, {self.location_radius}, {self.location_latitude}, " \
               f"{self.location_longitude}, {self.asset}, \'{self.event}\', \'{self.created_dt}\', \'{self.created_ts}\', " \
               f"\'{self.updated_ts}\', {self.altitude}, {self.heading}, {self.speed}, {self.speed_accuracy}, {self.course}," \
               f" {self.course_accuracy}, \'{self.datasource}\', \'{self.properties_dict}\'"