from flask import Blueprint, request, url_for, render_template, session,redirect, flash, jsonify
from modules.DB import DB

db = DB()

bp_modificar = Blueprint("bp_modificar",__name__, template_folder='templates', static_folder='static')

@bp_modificar.route('/user/modificar')
def Modificar():
    return render_template('modificar/modificar.html')