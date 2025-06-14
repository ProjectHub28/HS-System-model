from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from urllib.parse import urlparse
from app import db
from .forms import LoginForm, RegistrationForm, CameraForm
from .models import User, Camera
from flask_login import login_user, logout_user, current_user, login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Add a simple index route for now (can be expanded later)
@main_bp.route('/')
@main_bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main_bp.route('/add_camera', methods=['GET', 'POST'])
@login_required
def add_camera():
    form = CameraForm()
    if form.validate_on_submit():
        camera = Camera(name=form.name.data, rtsp_url=form.rtsp_url.data, owner=current_user)
        db.session.add(camera)
        db.session.commit()
        flash('Your camera has been added!')
        return redirect(url_for('main.cameras'))
    return render_template('add_camera.html', title='Add Camera', form=form)

@main_bp.route('/cameras')
@login_required
def cameras():
    user_cameras = current_user.cameras.all()
    return render_template('cameras.html', title='Your Cameras', cameras=user_cameras)

@main_bp.route('/edit_camera/<int:camera_id>', methods=['GET', 'POST'])
@login_required
def edit_camera(camera_id):
    camera = Camera.query.get_or_404(camera_id)
    if camera.owner != current_user:
        abort(403)
    form = CameraForm()
    if form.validate_on_submit():
        camera.name = form.name.data
        camera.rtsp_url = form.rtsp_url.data
        db.session.commit()
        flash('Your camera has been updated!')
        return redirect(url_for('main.cameras'))
    elif request.method == 'GET':
        form.name.data = camera.name
        form.rtsp_url.data = camera.rtsp_url
    return render_template('edit_camera.html', title='Edit Camera', form=form, camera=camera)

@main_bp.route('/delete_camera/<int:camera_id>', methods=['POST'])
@login_required
def delete_camera(camera_id):
    camera = Camera.query.get_or_404(camera_id)
    if camera.owner != current_user:
        abort(403)
    db.session.delete(camera)
    db.session.commit()
    flash('Your camera has been deleted.')
    return redirect(url_for('main.cameras'))

@main_bp.route('/arm_system', methods=['POST'])
@login_required
def arm_system():
    current_user.is_system_armed = True
    db.session.commit()
    flash('System Armed.')
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/disarm_system', methods=['POST'])
@login_required
def disarm_system():
    current_user.is_system_armed = False
    db.session.commit()
    flash('System Disarmed.')
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')
