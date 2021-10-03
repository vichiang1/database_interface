# Copyright 2021 Vitalant
# Author: Vincent Chiang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this software. If not, see <http://www.gnu.org/licenses/>.


from flask import Flask, render_template, make_response, url_for, request, send_file, session, Blueprint, redirect, flash, current_app, g
import pandas as pd
from pandas import DataFrame
from flask_security import login_required, current_user
import pyodbc
import os
from . import db
from .models import Queries, user_datastore, Users

webApp = Blueprint('webApp', __name__)

# Global comments removed for public release

# Setting up before Request from the config file:
@webApp.before_request
def load_config():
  server_url = current_app.config["SERVER_URL"]
  database = current_app.config["DATABASE_NAME"]
  g.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server_url+';DATABASE='+database+';Trusted_Connection=yes')
  g.DATA_TYPES = pd.read_sql("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COlUMNS", g.cnxn).set_index(
                        "COLUMN_NAME").to_dict()['DATA_TYPE']
  g.partial_variables = current_app.config["PARTIAL_VARIABLES"]
  g.PRIMARY = current_app.config["PRIMARY"]
  g.date_column = current_app.config["DATE_COLUMN"]
  g.date_format = current_app.config["DATE_FORMAT"]
  g.PREVIEW_NUM = current_app.config["PREVIEW_NUM"]

  if len(Users.query.all()) == 0:
    user_datastore.find_or_create_role(name = 'Admin')
    user_datastore.create_user(
                email = current_app.config["ADMIN_EMAIL"],
                password = current_app.config["ADMIN_PASS"],
                roles = ['Admin']
            )
    db.session.commit()

# Global comments removed for public release

# DATA_TYPES = pd.read_sql("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COlUMNS", g.cnxn).set_index(
#                         "COLUMN_NAME").to_dict()['DATA_TYPE']

  

# app = Flask(__name__)

# app.secret_key = os.urandom(28)


# df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
#                    'B': [5, 6, 7, 8, 9],
#                    'C': [10, 11, 12, 13, 14]})

# df1 = pd.DataFrame({'D': [0, 1, 2, 3, 4],
#                    'E': [5, 6, 7, 8, 9],
#                    'F': [10, 11, 12, 13, 14]})


# @app.route('/table', methods=("POST", "GET"))
# def html_table():
#   if request.method == 'POST':
#     if request.form['input'] == '0':
#       session["table"] = df.to_json()
#       return render_template('index.html', tables=[df.to_html(classes='data', header="true")])
#     else:
#       session["table"] = df1.to_json()
#       return render_template('index.html', tables = [df1.to_html(classes='data', header="true")])
#   elif request.method == "GET":
#     return f"Table name not given please return to /main"

@webApp.route('/download', methods=("POST", "GET"))
def download():
  if request.method == "GET":
    return f"No data given, please return to /main"
  sql = session.get("table")
  df = pd.read_sql(sql, g.cnxn)
  df = df.loc[:,~df.columns.duplicated()]
  resp = make_response(df.to_csv())

  resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
  resp.headers["Content-Type"] = "text/csv"

  return resp

@webApp.route('/save', methods=("POST", "GET"))
def save():
  if request.method == "GET":
    return f"No data given, please return to /main"

  sql = session.get("table")
  tables = session["names"]
  tName = session["tName"]

  try:
    q = Queries(name = request.form.get("name"), tables = tables, tName = tName, sql = sql)

    current_user.queries.append(q)

    db.session.commit()
    flash("success")
  except:
    flash("Name already existed")

  return redirect(url_for('webApp.html_table', index = 0), code = 307)


@webApp.route('/table', methods=("POST", "GET"))
@webApp.route('/table/<index>', methods=("POST", "GET"))
def html_table(index = 0, tName = None):
  print(request.form)
  index = int(index)
  if request.method == 'POST':
    # print(request.form)
    if "table" not in session:

      table_name = session["tName"]
      sql = table_name + " WHERE f.SAMPLEID is not NULL"

      for k in request.form:
        temp = request.form.getlist(k)

        if len(temp) == 1 and temp[0] == "":
          continue


        if g.PRIMARY in k:
          temp = temp[0].split()

          if "partial" in k and len(temp) > 0:
            sql += " AND (f." + g.PRIMARY + " LIKE '%" + temp[0] +  "%'"
            for j in range(1, len(temp)):
              sql += " OR f." + g.PRIMARY + " LIKE '%" + temp[j] +  "%'"
            sql += ")"
          else:
            sql += " AND f." + g.PRIMARY + " IN " + str(tuple(temp))
        elif k in g.partial_variables:
          sql += " AND " + k + " LIKE '%" + temp[0] +  "%'"
        elif k not in g.DATA_TYPES:
          temp = temp[0]
          if g.date_column in k:
            temp = temp.replace("-", "")
          
          if "min" == k[:3]:
            sql += " AND " + k[3:] + " >= " + temp
          else:
            sql += " AND " + k[3:] + " <= " + temp
        else:
          if len(temp) == 1:
            sql += " AND " + k + " = '" + temp[0] + "'"
          else:
            sql += " AND " + k + " IN " + str(tuple(temp))

      # sid = request.form['id']
      # if sid:
      #   sql += " AND f.SAMPLEID LIKE '%" + sid + "%'"


      # for col in session["cols"]:

      #   if col  == PRIMARY:
      #     if col in request.form:
      #       temp = request.form[col]
      #       if temp:
      #         if col in partial_variables:
      #           sql += " AND f." + col + " LIKE '%" + temp +  "%'"
      #         else:
      #           sql += " AND f." + col + " = " + temp

      #   elif col in partial_variables:
      #     temp = request.form[col]
      #     if temp:
      #       sql += " AND " + col + " LIKE '%" + temp +  "%'"
      #   elif "varchar" not in DATA_TYPES[col]:
      #     if "min" + col in request.form:
      #       sql += " AND " + col + " >= " + str(request.form["min" + col])
      #     if "max" + col in request.form:
      #       sql += " AND " + col + " <= " + str(request.form["max" + col])
          

      session["table"] = "SELECT * FROM " + sql
      # n = pd.read_sql("SELECT count(*) FROM" + sql, cnxn).values[0][0]
      # session["n"] = int(n)
      # sql = "SELECT TOP " + str(PREVIEW_NUM) + " * FROM " + sql
    sql = session["table"]

    n = int(pd.read_sql("SELECT count (*)" + sql.split("*")[1], g.cnxn).values[0][0])

    sql += " ORDER BY f.SAMPLEID OFFSET " + str(index) + " ROWS FETCH NEXT " + str(g.PREVIEW_NUM) + " ROWS ONLY"
    df = pd.read_sql(sql, g.cnxn)
    df = df.loc[:,~df.columns.duplicated()]
    if g.date_column in df.columns:
      df[g.date_column] = pd.to_datetime(df[g.date_column], format = date_format).dt.date
    return render_template('table.html', column_names = df.columns.values, row_data = list(df.values.tolist()),
                          zip = zip, n = n, m = df.shape[0], i = min(n - n % g.PREVIEW_NUM, index + g.PREVIEW_NUM), j = max([index - g.PREVIEW_NUM, 0]), k = index)
  elif request.method == "GET":
    return f"Table name not given please return to /main"

@webApp.route('/')
@webApp.route('/main', methods = ['POST', 'GET'])
@login_required
def main():
  if not current_user.password_changed:
    flash("Please Change your password before starting")
    return redirect(url_for('auth.change'))
  if "table" in session:
    session.pop("table")
  if "tName" in session:
    session.pop("tName")
    session.pop("names")
  names = pd.read_sql("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES", g.cnxn)["TABLE_NAME"]
  return render_template('main.html', names = names, admin = current_user.has_role("Admin") or current_user.has_role("SuperUser"))

@webApp.route('/saved', methods = ['POST', 'GET'])
@login_required
def saved():
  if "name" in request.form:
    name = request.form["name"]
    query = current_user.queries.filter(Queries.name == name).all()[0]
    session["tName"] = query.tName
    session["names"] = query.tables
    session["table"] = query.sql

    return redirect(url_for('webApp.html_table', index = 0), code = 307)

  queries = current_user.queries
  mapping = {q.name:q.sql for q  in queries}
  print(mapping)
  return render_template('saved.html', mapping = mapping)

@webApp.route('/input', methods = ['POST', 'GET'])
@login_required
def input():
  # print(request.form)
  if request.method == 'POST':
    if "table" in session:
      session.pop("table")

    if "tName" in session:
      tName = session["tName"]
      names = session["names"]
    else:
      names = request.form.getlist('table')
      joinT = request.form.getlist('joinT')
      # print(joinT)
      tName = ""
      # if 'metadata' in names:
      #   first = 'metadata'
      #   tName += ' metadata f'
      # else:
      first = names[0]
      tName += ' {s} f'.format(s = first)

      for i in range(1, len(names)):
        tName += " {j} {s} ON f.{p} = {s}.{p}".format(j = joinT[i - 1], s = names[i], p = g.PRIMARY)

      # for n in names:
      #   if n != first:
      #     tName += " JOIN {s} ON f.{p} = {s}.{p}".format(s = n, p = g.PRIMARY)

      names = ", ".join(names)
      session["tName"] = tName
      session["names"] = names
    if "cols" in session:
      session.pop("cols")

      
    # sql = "SELECT TOP 1 * FROM {s}".format(s = tName)

    t_names = names.split(", ")

    if len(t_names) == 1:
      sql = "SELECT DISTINCT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + t_names[0] + "'"
    else:
      sql = "SELECT DISTINCT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN " +  str(tuple(t_names))
    colN = list(pd.read_sql(sql, g.cnxn)["COLUMN_NAME"])
    # colN = list(colN.loc[:,~colN.columns.duplicated()].columns)
    unique_vals = dict()
    for n in colN:
      if "varchar" in g.DATA_TYPES[n] and n not in unique_vals:
        if n not in g.partial_variables:
          sql = "SELECT DISTINCT {n} FROM {s}".format(n = n, s = tName)
          temp = pd.read_sql(sql, g.cnxn)
          unique_vals[n] = temp.iloc[:, 0].to_list()
    
    # names = ", ".join(names)
    # session["tName"] = tName
    # session["names"] = names
    session["cols"] = colN
    return render_template('input.html', names = names, tName = tName, column_names = colN, 
                          vals = unique_vals, partial = g.partial_variables, date = g.date_column, primary = g.PRIMARY)
  if request.method == 'GET':
    return f"Table name not given please return to /main"

# if __name__ == "__main__":
#   app.run(debug = True)