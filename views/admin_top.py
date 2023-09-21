from flask import Blueprint, render_template, request, redirect, session, json
import DB.admin_top_db as db

admin_top = Blueprint('admin_top', __name__)


