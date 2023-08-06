import traceback
import json
from dto.PostgresSchema import PostgresSchemaDto
import pandas as pd
from datetime import datetime


class AssetTrackingIngest:
    def __init__(self) -> None:
        self.stop_list = [',', '[', ']', '(', ')', '\n', ' ', '"']

    def convert_datetime(self, time_str):
        try:
            datetime_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            date = datetime_obj.date()
            return date
        except:
            traceback.print_exc()

    def create_dataframe(self, json_list):
        try:
            df = pd.DataFrame.from_records(json_list)
            df['Properties'] = df['Properties'].replace('', '{}').apply(json.loads)
            return df
        except:
            traceback.print_exc()

    def extract_json(self, data):
        try:
            st = 1
            ind = []
            json_list = []
            for ix, i in enumerate(data):
                if ix == 0 or i in self.stop_list:
                    continue
                if i == '{':
                    ind.append(i)
                elif i == '}' and len(ind) > 0:
                    ind.pop(-1)
                if len(ind) == 0:
                    end = ix
                    sub_str = data[st:end + 1]
                    sub = json.loads(sub_str)
                    json_list.append(sub)
                    st = end + 1
            return json_list
        except:
            traceback.print_exc()

    def extract_properties(self, properties):
        try:
            emp_det = properties['Employee']
            loc_info = properties['UserLocationCoordinates']
            asset_id, emp_name = [i.strip() for i in emp_det.split(',')]
            lat, long, rad, _ = loc_info.split(',')
            lat, long, rad = float(lat.strip()), float(long.strip()), float(rad.strip())
            event_desc = properties['Description']
            try:
                transition = properties['Transition']
            except KeyError:
                transition = None
            try:
                route = properties['Route']
            except KeyError:
                route = None
            version = properties['Version']
            return asset_id, emp_name, lat, long, rad, event_desc, transition, route, version
        except KeyError:
            traceback.print_exc()

    def create_schema_list(self, df, asset_type, data_source, schema_version):
        try:
            schema_list = []
            for idx, item in df.iterrows():
                if item['EventName'] == 'CrashDiagnostics' or item['EventName'] == '':
                    continue
                asset_id, emp_name, lat, long, rad, event_desc, transition, route, version = \
                    None, None, None, None, None, None, None, None, None
                if len(item['Properties']) != 0:
                    asset_id, emp_name, lat, long, rad, event_desc, transition, route, version = \
                        self.extract_properties(item['Properties'])

                times = item['Timestamp']
                dt = self.convert_datetime(times)
                event = {'event': item['EventName'], 'event_id': item['EventId'], 'description': event_desc}

                properties_dict = {
                    'Employee_Name': emp_name,
                    'AppNamespace': item['AppNamespace'],
                    'AppVersion': item['AppVersion'],
                    'OsVersion': item['OsVersion'],
                    'Transition': transition,
                    'Route': route,
                    'Version': version
                }

                schema = PostgresSchemaDto(schema_version=schema_version, asset_id=asset_id, asset_type=asset_type, asset_latitude=lat, asset_longitude=long,
                                           created_dt=dt, created_ts=times, location_radius=rad, event=str(event), datasource=data_source,
                                           properties_dict=str(properties_dict))
                schema_list.append(schema)
            return schema_list
        except:
            traceback.print_exc()
