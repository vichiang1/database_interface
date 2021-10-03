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

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore


db = SQLAlchemy()
security = Security()

def create_app():
    app = Flask(__name__)

    # app.config["SECRET_KEY"] = 'development'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # app.config["DEBUG"] = True
    # app.config["SECURITY_PASSWORD_SALT"] = "thisisasecret"
    # app.config["SECURITY_TRACKABLE"] = True

    app.config.from_object('config.Config')

    db.init_app(app)

    # print(app.config["server_url"])

    from .models import Users, Roles, user_datastore
    security.init_app(app, user_datastore)
    
    with app.app_context():
        db.create_all()

    from .webApp import webApp as webApp_blueprint
    app.register_blueprint(webApp_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app