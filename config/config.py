import pymysql
import pymysql.cursors

# Connect to the database


class BaseConfig(object):
    DEBUG = False
    TESTING = False


class Development(BaseConfig):
    DEBUG = True
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'development key'
    PRODUCTION = False
    DATA = {
        "rows": [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                 [], [], [], [], [], [], [], [], [], [], [], [], [], [], [
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.37",
                  "last_modified_date": "2016-11-18T23:14:51-05:00",
                  "env": "prod"},
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.32",
                  "last_modified_date": "2016-11-18T23:13:31-05:00",
                  "env": "prod-prev"},
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.37",
                  "last_modified_date": "2016-11-15T12:56:21-05:00",
                  "env": "prod2"},
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.32",
                  "last_modified_date": "2016-11-15T12:54:18-05:00",
                  "env": "prod2-prev"},
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.37",
                  "last_modified_date": "2016-11-18T23:05:01-05:00",
                  "env": "proddr"},
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.32",
                  "last_modified_date": "2016-11-18T23:04:13-05:00",
                  "env": "proddr-prev"}], [], [], [], [
                 {"lob": "grips", "app": "grips-box-exception-report",
                  "version": "0.90",
                  "last_modified_date": "2015-10-16T11:01:05-04:00",
                  "env": "prod"}]]}


class Production(BaseConfig):
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'production key'
    PRODUCTION = True
    DATA = {
        "rows": [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                 [], [], [], [], [], [], [], [], [], [], [], [], [], [], [
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.37",
                  "last_modified_date": "2016-11-18T23:14:51-05:00",
                  "env": "prod"},
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.32",
                  "last_modified_date": "2016-11-18T23:13:31-05:00",
                  "env": "prod-prev"},
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.37",
                  "last_modified_date": "2016-11-15T12:56:21-05:00",
                  "env": "prod2"},
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.32",
                  "last_modified_date": "2016-11-15T12:54:18-05:00",
                  "env": "prod2-prev"},
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.37",
                  "last_modified_date": "2016-11-18T23:05:01-05:00",
                  "env": "proddr"},
                 {"lob": "grips", "app": "grips-adapter-stability-athena",
                  "version": "0.32",
                  "last_modified_date": "2016-11-18T23:04:13-05:00",
                  "env": "proddr-prev"}], [], [], [], [
                 {"lob": "grips", "app": "grips-box-exception-report",
                  "version": "0.90",
                  "last_modified_date": "2015-10-16T11:01:05-04:00",
                  "env": "prod"}]]}
