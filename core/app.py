# -*- coding: utf-8 -*-
"""
    Aim versions monitoring tool
    ~~~~~~
    A tool to collect data from AIM apps or artifacts versions
    and displays it in an helpful way
    Flask and sqlite3.
    :author: Wuelfhis Asuaje.
"""
# TODO: Make the app mysqlable!
import os
# from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, json, jsonify, current_app, Blueprint
import datetime
from dateutil.parser import *
import pandas as pd
import pdb


core_app = Blueprint(
    'core_app',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/core')


def run_sql_cmd(cmd, params=None, run_commit=None, many=None):
    """wrapper to sql commands execute to abtract the db engine"""
    db = current_app.config["DATABASE"]

    # jsut in case the conn is closed seems to work in pivotal
    db.ping()

    cursor = db.cursor()
    if many:
        cursor.executemany(cmd, params)
    else:
        cursor.execute(cmd, params)

    if run_commit:
        db.commit()

    return cursor


def init_db():
    """Initializes the database."""
    data_sql = 'scheme_mysql.sql'

    with app.open_resource(data_sql, mode='r') as f:
        run_sql_cmd(f.read(), run_commit=True)


def _get_formatted_date(str_data):

    try:
        now = parse(str_data)
    except AttributeError:
        print "Attribute Error parsing date trying to fix"
        now = str_data

    return now.strftime("%m-%d-%Y - %H:%M:%S")


def _get_lobs_from_db():
    try:
        cur3 = run_sql_cmd('select distinct lob from entries order by lob;',)
        rows = cur3.fetchall()
    except TypeError as e:
        print e
        rows = ["No data"]
    lobs = rows

    return lobs


def _get_pivot_table(sql_cmd, sql_args, db=None):
    db = current_app.config["DATABASE"]
    count = 0
    html = ""
    #
    # get a raw pandas dataframe straight from a sql query
    #
    try:
        sheet = pd.read_sql(
            sql_cmd,
            con=db,
            params=sql_args,
            index_col="id")
    except:
        print "Something went wrong in pivoting tables"
    else:
        #
        # pivoting the data frame into 2 dicts one for versios one for dates
        #
        pivot_ver = sheet.pivot(
            index="env",
            columns="app",
            values="version")
        pivot_lu = sheet.pivot(
            index="env",
            columns="app",
            values="last_update")
        pivot_lu = pivot_lu.to_dict()
        pivot_ver = pivot_ver.to_dict()
        #
        # get unique cols names for entire lob
        #
        cols = []
        for app in pivot_ver.keys():
            for env in pivot_ver[app]:
                if not env in cols:
                    cols.append(env)

        #
        # Building the html table to pass to template
        #
        html = ""
        count = len(pivot_lu)
        new_line = False
        if len(cols) > 0:
            lob = sheet.values[0][0]
            html += "".join(["<td>{}</td>".format(x) for x in cols])
            html += "</tr>"

            for app in pivot_ver.keys():
                html += "<tr>"
                if not new_line:
                    html += "<td>{}</td>".format(lob)
                else:
                    html += "<td></td>"
                html += "<td>{}</td>".format(app)

                for env in pivot_ver[app]:
                    if str(pivot_lu[app][env]) == 'nan':
                        html += "<td class='data'>--</td>"
                    else:
                        ver = pivot_ver[app][env]
                        lu = _get_formatted_date(pivot_lu[app][env])
                        html += "<td class='data'><a class='tooltip'" \
                            "href='javascript:void(0)'" \
                            "data-title='{}'>{}</a></td>".format(lu, ver)

                html += "</tr>"
                new_line = True
        else:
            html += "<tr><td colspan = '2'>No Records</td></tr>"
    return count, html


def _get_last_update_db_data():
    try:
        cur3 = run_sql_cmd('select last_update from config order by id desc')
        date_record = cur3.fetchone()
        last_update_date = _get_formatted_date(date_record["last_update"])
    except TypeError as e:
        print e.message
        last_update_date = "No update"

    return last_update_date


@core_app.route('/', methods=['POST', 'GET'])
def index():
    # init_db()
    # flash(u'Welcome to Aim Versions Tools','error')
    text_search = ""
    lob_search = ""
    lobs = _get_lobs_from_db()
    if request.method == "POST":
        text_search = request.form["text_search"]
        lob_search = request.form["lob_search"]

        if len(text_search) > 0 and len(lob_search) > 0:
            sql_cmd = "select * from entries where lob = %s \
                        and app like %s order by lob, app, env"
            sql_args = ("{}".format(lob_search), "%{}%".format(text_search))
        elif len(text_search) == 0 and len(lob_search) > 0:
            sql_cmd = "select * from entries where lob = %s \
                         order by lob, app, env "
            sql_args = ("{}".format(lob_search),)
    else:
        if len(lobs) > 0 and 'No data' not in lobs:
            sql_cmd = "select * from entries where lob = %s order by lob, app, env"
            sql_args = (lobs[0]["lob"],)
        else:
            sql_cmd = "select * from entries order by lob, app, env"
            sql_args = None

    last_update_date = _get_last_update_db_data()
    count, html = _get_pivot_table(sql_cmd, sql_args)

    return render_template('index.html', html=html,
                           last_update_date=last_update_date,
                           lobs=lobs, count=count, text_search=text_search,
                           lob_search=lob_search)


@core_app.route('/add_data_for_testing', methods=['GET'])
def add_testing_data():
    #
    # initdb create data structure
    #
    init_db()
    data = current_app.config["DATA"]
    data_tuple_list = []

    for rows in data[u"rows"]:
        for row in rows:
            if len(row) > 0:
                data_tuple_list.append(tuple([row[u"lob"], row[u"app"],
                                              row[u"version"], row[u"env"],
                                              row[u"last_modified_date"]]))
    #
    # Execute a bulk insert of all data pe collections at once
    #
    run_sql_cmd(
        "insert into entries (lob, app, version, env, last_update) \
                   values (%s,%s,%s,%s,%s)", tuple(data_tuple_list),
        many=True,
        run_commit=True
    )
    run_sql_cmd(
        "insert into config (last_update) values (%s)",
        (datetime.datetime.now(),), run_commit=True
    )

    return redirect(url_for('core_app.index'))


@core_app.route('/add', methods=['POST'])
def add_entry():
    """
    Adds the data to de DB:
     Receives a json {u'rows': [{list of dicts},]}
     grouped by collection names
    """

    if request.method == "POST":
        json_dict = request.get_json()
        data_tuple_list = []
        # print "##dict - ##", json_dict
        for rows in json_dict[u"rows"]:
            for row in rows:
                # print "## row  ##", row
                if len(row) > 0:
                    data_tuple_list.append(tuple([row[u"lob"], row[u"app"],
                                                  row[u"version"], row[u"env"],
                                                  row[u"last_modified_date"]]))
        #
        # Execute a bulk insert of all data pe collections at once
        #
        try:
            run_sql_cmd(
                "insert into entries (lob, app, version, env, last_update) \
                            values (%s,%s,%s,%s,%s)", tuple(data_tuple_list),
                many=True,
                run_commit=True
            )
            run_sql_cmd(
                "insert into config (last_update) values (%s)",
                (datetime.datetime.now(),),
                run_commit=True
            )

        except:
            return_data = {"result": "ERROR",
                           "Message": "Something went wrong inserting data"}
            return_code = 500
        else:
            return_data = {"result": "OK",
                           "Message": "Successfully processed"}
            return_code = 200

    resp = jsonify(return_data)
    resp.status_code = return_code
    return resp


@core_app.route('/login')
def login():
    return "Hello World"


@core_app.route('/logout')
def logout():
    return "Hello World"
