from flask import render_template
from app import app
from .models import review
from .forms import ReviewForm

Review = review.Review

# Views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Pitches-Home page'
    return render_template('index.html', title = title)

@app.route('/pitch/<int:pitch_id>')
def pitch(pitch_id):

    '''
    View pitch page function that returns the pitch details page and its data
    '''
    pitch = get_pitch(id)
    title = f'{pitch.title}'
    reviews = Review.get_reviews(pitch.id)

    return render_template('pitch.html',title = title,pitch = pitch,reviews = reviews)


@app.route('/pitch/review/new/<int:id>', methods = ['GET','POST'])
def new_review(id):
    form = ReviewForm()
    pitch = get_pitch(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data
        new_review = Review(pitch.id,title,review)
        new_review.save_review()
        return redirect(url_for('pitch',id = pitch.id ))

    title = f'{pitch.title} review'
    return render_template('new_review.html',title = title, review_form=form, pitch=pitch)