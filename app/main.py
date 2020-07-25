import os

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from dotenv import load_dotenv

from . import db
from .models import Url
from service.validation import is_valid_url
from service.convert import encode, decode

main = Blueprint('main', __name__)
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/shorten', methods=['POST'])
@login_required
def shorten():
    url = request.form.get('url')
    if not is_valid_url(url):
        flash('Not valid URL')
        return redirect(url_for('dashboard'))

    new_url = Url(long_url=url)
    db.session.add(new_url)
    db.session.commit()

    shorten_url = encode(new_url.id)
    flash(os.getenv('HOST_URL') + '/longten?shorten_url=' + shorten_url)
    return redirect(url_for('main.dashboard'))

@main.route('/longten')
@login_required
def longten():
    shorten_url = request.args.get('shorten_url')
    url_id = decode(shorten_url)
    target_url = Url.query.filter_by(id=url_id).first()

    return redirect(target_url.long_url)
