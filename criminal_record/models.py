import csv
import os
from .constants import FieldTypes as FT
import json
import psycopg2 as pg
from psycopg2.extras import DictCursor
from tkinter import messagebox
from psycopg2 import sql as SQL

class CSVModel:

    fields = {
        'First Name': {'req': True, 'type':FT.string, 'width':70},
        'Last Name': {'req': True, 'type':FT.string, 'width':70},
        'Aliases': {'req': True, 'type':FT.string, 'width':70},
        'Birth Date': {'req': True, 'type':FT.iso_date_string},
        'Age': {'req': True, 'type':FT.integer},
        'Male': {'req': True, 'type':FT.boolean},
        'Female': {'req': True, 'type':FT.boolean},
        'Height': {'req': True, 'type':FT.string, 'width':10},
        'Weight': {'req': True, 'type':FT.integer, 'width':10},
        'Eye Color': {'req': True, 'type':FT.string, 'width':12},
        'Hair Color': {'req': True, 'type':FT.string, 'width':12},
        'Body Build': {'req': True, 'type':FT.string_list,
                       'values': ['   --select--', 'Ectomorph', 'Endomorph', 'Mesomorph']},
        'Mutation': {'req': True, 'type':FT.long_string, 'width':25, 'height':3},
        'Scars and Marks': {'req': True, 'type':FT.long_string, 'width':25, 'height':3},
        'Nationality': {'req': True, 'type':FT.string},
        'State': {'req': True, 'type':FT.string_list,
                  'values':['   --select--', 'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Enugu', 'Ekiti', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto' , 'Taraba', 'Yobe', 'Zamfara']},
        'LGA': {'req': True, 'type':FT.string},
        'Residence Address': {'req': True, 'type':FT.string, 'width':70},
        'Date of Registration': {'req': True, 'type':FT.iso_date_string},
        'Date of Arrest': {'req': True, 'type':FT.iso_date_string},
        'Case Number': {'req': True, 'type':FT.integer},
        'Arresting Officer': {'req': True, 'type':FT.string, 'width':70},
        'Place of Arrest': {'req': True, 'type':FT.string, 'width':70},
        'Area': {'req': True, 'type':FT.string},
        'Division': {'req': True, 'type':FT.string},
        'Class of Crime': {'req': True, 'type':FT.string_list,
                       'values': ['   -- select--', 'Felony', 'Misdemeanors', 'Felony-Misdemeanors', 'Infractions']},
        'Ex-Convict': {'req': True, 'type':FT.boolean},
        'Crime': {'req': True, 'type':FT.long_string, 'width':25, 'height':5},
        'Known Gang': {'req': True, 'type':FT.long_string, 'width':25, 'height':5},
    }


    def __init__(self, filename):
        self.filename = filename

    def save_record(self, data, rownum=None):
        if rownum is not None:
            records = self.get_all_records()
            records[rownum] = data
            with open(self.filename, 'w') as fh:
                csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
                csvwriter.writeheader()
                csvwriter.writerows(records)
        else:
            newfile = not os.path.exists(self.filename)

            with open(self.filename, 'a') as fh:
                csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
                if newfile:
                    csvwriter.writeheader()
                csvwriter.writerow(data)

    def get_all_records(self):
        if not os.path.exists(self.filename):
            return[]
        with open(self.filename, 'r') as fh:
            csvreader = csv.DictReader(fh)
            missing_fields = (set(self.fields.keys()) - set(csvreader.fieldnames))
            if len(missing_fields) > 0:
                raise Exception('File is missing in fields:{}'.format(', '.join(missing_fields)))
            else:
                records = list(csvreader)
                trues = ('true', 'yes', '1', 'True')
                bool_fields = [
                    key for key, meta in self.fields.items()
                    if meta['type'] == FT.boolean
                ]
                for record in records:
                    for key in bool_fields:
                        record[key] = record[key].lower() in trues
                return records

    def get_record(self, rownum):
         return self.get_all_records()[rownum]
            


class SettingsModel:

    variables = {
        'autofill date': {'type': 'bool', 'value':True},
        'font size': {'type': 'int', 'value': 9},
        'theme': {'type': 'str', 'value': 'default'},
        'db_host': {'type': 'str', 'value': 'localhost'},
        'db_name': {'type': 'str', 'value': 'criminal_record'}
    }
    
    def __init__(self, filename='record_settings.json', path='~'):
        self.filepath = os.path.join(os.path.expanduser(path), filename)

        self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            return
        
        with open(self.filepath, 'r') as fh:
            raw_values = json.loads(fh.read())
        for key in self.variables:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.variables[key]['value'] = raw_value
        

    def save(self, settings=None):
        json_string = json.dumps(self.variables)
        with open(self.filepath, 'w') as fh:
            fh.write(json_string)

    def set(self, key, value):
        if(key in self.variables and type(value).__name__ == self.variables[key]['type']):
            self.variables[key]['value'] = value
        
        else:
            raise ValueError('Bad key or wrong variable type')


class SQLModel:
    fields = {
        'First Name': {'req': True, 'type':FT.string, 'width':35},
        'Last Name': {'req': True, 'type':FT.string, 'width':35},
        'Aliases': {'req': True, 'type':FT.string, 'width':70},
        'Birth Date': {'req': True, 'type':FT.iso_date_string},
        'Age': {'req': True, 'type':FT.integer},
        'Male': {'req': True, 'type':FT.boolean},
        'Female': {'req': True, 'type':FT.boolean},
        'Height': {'req': True, 'type':FT.string, 'width':10},
        'Weight': {'req': True, 'type':FT.integer, 'width':10},
        'Eye Color': {'req': True, 'type':FT.string, 'width':12},
        'Hair Color': {'req': True, 'type':FT.string, 'width':12},
        'Body Build': {'req': True, 'type':FT.string_list, 'values': []},
        'Mutation': {'req': True, 'type':FT.long_string, 'width':25, 'height':3},
        'Scars and Marks': {'req': True, 'type':FT.long_string, 'width':25, 'height':3},
        'Nationality': {'req': True, 'type':FT.string},
        'State': {'req': True, 'type':FT.string_list, 'values':[]},
        'LGA': {'req': True, 'type':FT.string},
        'Residence Address': {'req': True, 'type':FT.string, 'width':70},
        'Date of Registration': {'req': True, 'type':FT.iso_date_string},
        'Date of Arrest': {'req': True, 'type':FT.iso_date_string},
        'Case Number': {'req': True, 'type':FT.integer},
        'Arresting Officer': {'req': True, 'type':FT.string, 'width':70},
        'Place of Arrest': {'req': True, 'type':FT.string, 'width':70},
        'Area': {'req': True, 'type':FT.string},
        'Division': {'req': True, 'type':FT.string},
        'Class of Crime': {'req': True, 'type':FT.string_list, 'values': []},
        'Ex-Convict': {'req': True, 'type':FT.boolean},
        'Crime': {'req': True, 'type':FT.long_string, 'width':25, 'height':5},
        'Known Gang': {'req': True, 'type':FT.long_string, 'width':25, 'height':5},
    }

    def __init__(self, host, database, user, password):
        self.connection = pg.connect(host=host, database=database, user=user,
                                     password=password, cursor_factory=DictCursor)

        body_build = self.query("SELECT body_builds FROM bb_combo ORDER BY body_builds")
        state = self.query("SELECT states FROM states_combo ORDER BY states")
        class_of_crime = self.query("SELECT class_of_crimes FROM coc_combo ORDER BY class_of_crimes")
        self.fields["Body Build"]["values"] = [x['body_builds'] for x in body_build]
        self.fields["State"]["values"] = [x['states'] for x in state]
        self.fields["Class of Crime"]["values"] = [x['class_of_crimes'] for x in class_of_crime]
        
    def query(self, query, parameters=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, parameters)
        except(pg.Error) as e:
            self.connection.rollback()
            raise e
        else:
            self.connection.commit()
            if cursor.description is not None:
                return cursor.fetchall()

    def search_query(self, category, search_inp):
        query = ('SELECT * FROM data_record_view WHERE "{}" = %(search_inp)s').format(category)
        result = self.query(query, {'search_inp':search_inp})
        return result if result else {}
        

    def get_all_records(self, all_dates=False):
        query = ('SELECT * FROM data_record_view '
                 'WHERE NOT %(all_dates)s OR "Date of Registration" = CURRENT_DATE '
                 'ORDER BY "Case Number", "Date of Registration"')
        return self.query(query, {'all_dates':all_dates})

    def get_record(self, case_number, date_of_registration):
        query = ('SELECT * FROM data_record_view '
                 'WHERE "Case Number" = %(case_number)s '
                 'AND "Date of Registration" = %(date_of_registration)s')
        result = self.query(
            query, {'case_number': case_number, 'date_of_registration': date_of_registration})
        return result[0] if result else {}

    def get_cases(self, case_number, date_of_registration):
        query = ('SELECT case_numbers, dates_of_registration FROM cases')
        
        results = self.query(
            query, {'case_number': case_number, 'date_of_registration': date_of_registration})
        return results[0] if results else {}

    c_update_query = (    
        'UPDATE cases SET case_numbers = %(Case Number)s, '
        'dates_of_registration = %(Date of Registration)s'
        )

    c_insert_query = (
        'INSERT INTO cases VALUES (%(Case Number)s, '
        '%(Date of Registration)s)'
        )
        
    pi_update_query = (
        'UPDATE personal_information SET cases_number = %(Case Number)s, '
        'first_name = %(First Name)s, last_name = %(Last Name)s, aliases = %(Aliases)s, '
        'birth_date = %(Birth Date)s, age = %(Age)s, male = %(Male)s, '
        'female = %(Female)s, height = %(Height)s, weight = %(Weight)s, '
        'eye_color = %(Eye Color)s, hair_color = %(Hair Color)s, '
        'body_build = %(Body Build)s, mutation = %(Mutation)s, '
        'scars_and_marks = %(Scars and Marks)s, nationality = %(Nationality)s, '
        'state = %(State)s, lga = %(LGA)s, residence_address = %(Residence Address)s '
        )

    pi_insert_query = (
        'INSERT INTO personal_information VALUES (%(Case Number)s, %(First Name)s, '
        '%(Last Name)s, %(Aliases)s, %(Birth Date)s, %(Age)s, %(Male)s, %(Female)s, '
        '%(Height)s, %(Weight)s, %(Eye Color)s, %(Hair Color)s, '
        '%(Body Build)s, %(Mutation)s, %(Scars and Marks)s, '
        '%(Nationality)s, %(State)s, %(LGA)s, '
        '%(Residence Address)s)'
        )
        

    oi_update_query = (
        'UPDATE official_information SET case_number = %(Case Number)s, '
        'date_of_registration = %(Date of Registration)s, date_of_arrest = %(Date of Arrest)s, '
        'arresting_officer = %(Arresting Officer)s, place_of_arrest = %(Place of Arrest)s, '
        'area = %(Area)s, division = %(Division)s, class_of_crime = %(Class of Crime)s, '
        'crime = %(Crime)s, ex_convict = %(Ex-Convict)s, known_gang = %(Known Gang)s'
        )

    oi_insert_query = (
        'INSERT INTO official_information VALUES (%(Case Number)s, '
        '%(Date of Registration)s, %(Date of Arrest)s, '
        '%(Arresting Officer)s, %(Place of Arrest)s, '
        '%(Area)s, %(Division)s, %(Class of Crime)s, '
        '%(Crime)s, %(Ex-Convict)s, %(Known Gang)s)'
        )

    def save_record(self, record):
        case_number = record['Case Number']
        date_of_registration = record['Date of Registration']  
                 
        if self.get_record(case_number, date_of_registration):
            c_query = self.c_update_query
            pi_query = self.pi_update_query
            oi_query = self.oi_update_query
            self.last_write = 'update'
                 
        else:
            c_query = self.c_insert_query
            pi_query = self.pi_insert_query
            oi_query = self.oi_insert_query
            self.last_write = 'insert'
            
        self.query(c_query, record)    
        self.query(pi_query, record)
        self.query(oi_query, record)
        

                 

    
                
            
        

        


            
            


        
