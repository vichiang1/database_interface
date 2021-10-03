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

from flask import Flask, render_template, make_response, url_for, request, send_file, session, Blueprint, redirect
import os
from . import db
from .models import Users, user_datastore
from flask_security.utils import hash_password, verify_password
from flask_security import roles_accepted, current_user, login_required

auth = Blueprint('auth', __name__)

ROLES = ["Admin", "SuperUser", "User"]

@auth.route('/register', methods = ['POST', 'GET'])
@roles_accepted('Admin', "SuperUser")
def register():
    if request.method == 'POST':
        if user_datastore.get_user(request.form.get('email')) == None:

            user_datastore.find_or_create_role(name = request.form.get('role'))
            user_datastore.create_user(
                email=request.form.get('email'),
                password=hash_password(request.form.get('password')),
                roles = [request.form.get('role')]
            )
            db.session.commit()
            return render_template('register.html', success = True)
        else:
            return render_template('register.html', success = False)
    return render_template('register.html')

@auth.route('/change', methods = ['POST', 'GET'])
@login_required
def change():
    if request.method == 'POST':
        if verify_password(request.form.get('password'), current_user.password):

            current_user.password = hash_password(request.form.get('new_password'))
            current_user.password_changed = True
            db.session.commit()
            return render_template('change.html', success = True)
        else:
            return render_template('change.html', success = False)
    return render_template('change.html')

@auth.route('/manage', methods = ['POST', 'GET'])
@roles_accepted('Admin', "SuperUser")
def manage():
    # Admin can delete everyone while SuperUser can only delete normal Users
    if request.method == 'POST':

        u = user_datastore.get_user(request.form["user"])
        admin_role = u.has_role("Admin")
        super_role = u.has_role("SuperUser")

        msg = None
        if admin_role:
            msg = "Cannot Modify Admin Account"
        elif request.form["type"] == "delete":
            if super_role:
                if current_user.has_role("Admin"):
                    user_datastore.delete_user(u)
                    msg = "Super User Account deleted"
                else:
                    msg = "Fail, only Admin can delete super user account"
            else:
                user_datastore.delete_user(u)
                success = True
        elif request.form["type"] == "deactivate":
            if super_role:
                if current_user.has_role("Admin"):
                    success = user_datastore.delete_user(u)
                    if success:
                        msg = "Super user account deactivated"
                    else:
                        msg = "Fail, account already deactivated or its your acount"
                else:
                    msg = "Only admin can delete super user account"
            else:
                success = user_datastore.deactivate_user(u)
                if success:
                    msg = "User account deactivated"
                else:
                    msg = "Fail, account already deactivated or its your acount"
        else:
            if super_role:
                if current_user.has_role("Admin"):
                    success = user_datastore.activate_user(u)
                    if success:
                        msg = "Super user account activated"
                    else:
                        msg = "Fail, Account already activated"
                else:
                    msg = "Fail, Only admin can activate super user account"
            else:
                success = user_datastore.activate_user(u)
                if success:
                    msg = "User account activated"
                else:
                    msg = "Fail, account already activated"

        db.session.commit()
        all_users = Users.query.all()
        all_users = [user.email for user in all_users]
        return render_template('manage.html', users = all_users, message = msg)

            

    else:
        all_users = Users.query.all()
        all_users = [u.email for u in all_users]

        return render_template('manage.html', users = all_users)