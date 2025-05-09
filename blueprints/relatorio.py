from flask import Blueprint, jsonify, render_template, request
from modules.DB import DB
from sqlalchemy import text
import matplotlib as mt
import pandas as pd

bp_relatorio = Blueprint("bp_relatorio", __name__, template_folder="templates")

@bp_relatorio.route('/user/relatorio')
def Relatorio():

    return render_template("relatorio/relatorio.html")

