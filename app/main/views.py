from flask import render_template,request,redirect,url_for
from . import main
from .forms import ReviewForm
from ..models import Review
from flask_login import login_required

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