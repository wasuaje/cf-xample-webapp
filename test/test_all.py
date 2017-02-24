# -*- coding: utf-8 -*-
__author__ = 'D569906 - Wuelfhis Asuaje'


import unittest
import json
import os
import tempfile
import datetime
from dateutil.parser import *

import core.app

data_to_insert = {
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


class WebAppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, core.app.app.config['DATABASE'] = tempfile.mkstemp()
        core.app.app.config['TESTING'] = True
        self.app = core.app.app.test_client()
        with core.app.app.app_context():
            core.app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(core.app.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        self.assertIn(b'No update', rv.data)
        self.assertIn(b'No Records', rv.data)

    def test_add_data(self):
        data = json.dumps(data_to_insert)
        rv = self.app.post('/add', data=data, content_type='application/json')
        # print rv.data
        self.assertNotIn(b'Something went wrong inserting data', rv.data)
        self.assertNotIn(b'Error', rv.data)
        self.assertIn(b'Successfully processed', rv.data)

    def test_add_show_data(self):
        data = json.dumps(data_to_insert)
        rv = self.app.post('/add', data=data, content_type='application/json')
        get_data = self.app.get('/')
        # print get_data.data
        self.assertNotIn(b'Something went wrong inserting data', rv.data)
        self.assertNotIn(b'Error', rv.data)
        self.assertIn(b'Successfully processed', rv.data)

        # Test all application came with data in call to '/' after insert
        for dt in data_to_insert["rows"]:
            if len(dt) > 0:
                for apps in dt:
                    self.assertIn(apps["app"], get_data.data)

    def test_search_text(self):
        data = json.dumps(data_to_insert)
        to_search = u'grips-adapter-stability-athena'
        rv = self.app.post('/add', data=data, content_type='application/json')
        get_data = self.app.post('/', data=dict(text_search=to_search,
                                                lob_search='grips'),
                                 follow_redirects=True)
        # print get_data.data
        self.assertNotIn(b'Something went wrong inserting data', rv.data)
        self.assertNotIn(b'Error', rv.data)
        self.assertIn(b'Successfully processed', rv.data)
        self.assertIn(to_search, get_data.data)

    def test_date_formatting(self):
        date = datetime.datetime.now()
        string_date = date.strftime("%m-%d-%Y - %H:%M:%S")
        result_date = core.app.get_formatted_date(date.strftime(
                                                        "%m-%d-%Y - %H:%M:%S"))
        self.assertTrue( result_date == string_date )

    def test_empty_pivot_when_no_records(self):
        sql_cmd = "select * from entries where lob = ? order by lob, app, env"
        sql_args = ('grips',)

        with core.app.app.app_context():
            pivot = core.app._get_pivot_table(sql_cmd, sql_args, core.app.get_db())

        self.assertIn('No Records', pivot[1])

    def test_pivot_filled_with_data(self):
        data = json.dumps(data_to_insert)
        rv = self.app.post('/add', data=data, content_type='application/json')

        to_search = u'grips-adapter-stability-athena'
        sql_cmd = "select * from entries where lob = ? order by lob, app, env"
        sql_args = ('grips',)

        with core.app.app.app_context():
            pivot = core.app._get_pivot_table(sql_cmd, sql_args, core.app.get_db())

        self.assertIn(to_search, pivot[1])
        self.assertNotIn('No Records', pivot[1])