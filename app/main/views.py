from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm, UpdateProfile
from ..models import Review,User
from flask_login import login_required
from .. import db, photos

# Review = review.Review

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Pitches-Home page'
    return render_template('index.html', title = title)

@main.route('/pitch/review/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_review(id):
    form = ReviewForm()
    pitch = get_pitch(id)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
    
@main.route('/pitch/<int:pitch_id>')
def pitch(pitch_id):

    '''
    View pitch page function that returns the pitch details page and its data
    '''
    title = 'Pitches-Home page'
    return render_template('pitch.html', title = title)
    # pitch = get_pitch(id)
    # title = f'{pitch.title}'
    # reviews = Review.get_reviews(pitch.id)

    # return render_template('pitch.html')


# @main.route('/pitch/review/new/<int:id>', methods = ['GET','POST'])
# def new_review(id):
#     
#     

#     if form.validate_on_submit():
#         title = form.title.data
#         review = form.review.data
#         new_review = Review(pitch.id,title,review)
#         new_review.save_review()
#         return redirect(url_for('pitch',id = pitch.id ))

#     title = f'{pitch.title} review'
#     return render_template('new_review.html',title = title, review_form=form, pitch=pitch)