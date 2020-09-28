import os
import functools
import secrets
from flask import render_template,redirect,url_for,abort,flash,request
from . import main
from flask_login import login_required,current_user
from ..models import User,Comment,Pitch,Votes
from .. import db,photos
from .forms import UpdateProfile,UploadPitch,CommentsForm
from flask import current_app


@main.route('/')
def index():

    title = 'Pitches | Hub'
    page=request.args.get('page',1,type=int)
    all_pitch=Pitch.query.order_by(Pitch.posted.desc()).paginate(page=page,per_page=10)
  
    return render_template('index.html',pitches=all_pitch, title = title)

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

@main.route('/upload/pitch',methods=['GET','POST'])
@login_required
def upload_pitch():
    pitch=UploadPitch()
    if current_user is None:
        abort(404)
    if pitch.validate_on_submit():
        pitch=Pitch(pitch_category=pitch.category.data,pitch=pitch.pitch.data,user=current_user)
        db.session.add(pitch)
        db.session.commit()
        flash('Pitch Uploaded')
        return redirect(url_for('main.index'))
    return render_template('profile/update_pitch.html',pitch=pitch,title='Create Pitch',legend='Create Pitch')

@main.route('/<int:pname>/comment',methods=['GET','POST'])
@login_required
def comment(pname):
    comment=CommentsForm()
    image=url_for('static',filename='profile/'+ current_user.profile_pic_path)
    pitch=Pitch.query.filter_by(id=pname).first()
    comment_query=Comment.query.filter_by(pitch_id=pitch.id).all()
    
    if request.args.get('likes'):
        pitch.upvotes=pitch.upvotes+int(1)
        db.session.add(pitch)
        db.session.commit()
        return redirect(url_for('main.comment',pname=pname))

    
    elif request.args.get('dislike'):
        pitch.downvotes=pitch.downvotes+int(1)
        db.session.add(pitch)
        db.session.commit()
        return redirect(url_for('main.comment',pname=pname))

    if comments.validate_on_submit():
        comment=Comment(comment=comments.comment.data,pitch_id=pitch.id,user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.comment',pname=pname))
    
    return render_template('pitch.html',comment=comments,pitch=pitch,comments=comment_query,title='Pitch Comment',image=image)

@main.route('/<int:pname>/update',methods=['GET','POST'])
@login_required
def update(pname):
    pitches=UploadPitch()
    pitch=Pitch.query.get(pname)
    if pitch.user != current_user:
        abort(403)
    if pitches.validate_on_submit():
        pitch.pitch_category=pitches.category.data
        pitch.pitch=pitches.pitch.data
        db.session.commit()
        flash('Successfully Updated!')
        return redirect(url_for('main.profile',uname=pitch.user.username))
    elif request.method=='GET':
        pitches.category.data=pitch.pitch_category
        pitches.pitch.data=pitch.pitch

    return render_template('profile/update_pitch.html',pitch=pitches,legend="Update Pitch")

@main.route('/<int:pitch_id>/delete',methods=['POST'])
@login_required
def delete_pitch(pitch_id):
    pitch=Pitch.query.get(pitch_id)
    if pitch.user != current_user:
        abort(403)
    
    db.session.delete(pitch)
    db.session.commit()

    return redirect(url_for('main.profile',uname=pitch.user.username))


@main.route('/profile/user/<string:username>')
def posted(username):
    user=User.query.filter_by(username=username).first_or_404()
    image=url_for('static',filename='profile/'+ user.profile_pic_path)
    page=request.args.get('page',1,type=int)
    all_pitch=Pitch.query.filter_by(user=user)\
            .order_by(Pitch.posted.desc())\
            .paginate(page=page,per_page=10)

    return render_template('posted_by.html',pitches=all_pitch,title=user.username,user=user,image=image)

@main.route('/pitch/upvote/<int:id>')
@login_required
def upvote(id):
    '''
    View function that add one to the vote_number column in the votes table
    '''
    pitch_id = Pitch.query.filter_by(id=id).first()

    if pitch_id is None:
         abort(404)

    new_vote = Votes(vote=int(1), user_id=current_user.id, pitches_id=pitch_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_pitch', id=id))



@main.route('/pitch/downvote/<int:id>')
@login_required
def downvote(id):
    pitch_id = Pitch.query.filter_by(id=id).first()

    new_vote = Votes(vote=int(2), user_id=current_user.id, pitches_id=pitch_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_pitch', id=id))

@main.route('/pitch/downvote/<int:id>')
@login_required
def vote_count(id):

    votes = Votes.query.filter_by(user_id=current_user.id).all()

    total_votes = votes.count()

    return total_votes

@main.route('/like/<int:pitch_id>/<action>')
@login_required
def like_action(comment_id, action):
    comment = Comment.query.filter_by(id=post_id).first_or_404()
    if action == 'vote':
        current_user.vote_comment(comment)
        db.session.commit()
    if action == 'downvote':
        current_user.unlike_comment(comment)
        db.session.commit()
    return redirect(request.referrer) 