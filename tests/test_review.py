from app.models import Review,User
from app import db

def setUp(self):
    self.user_nelly = User(username = 'nelly',password = 'potato', email = 'nelly@gmail.com')
    self.new_review = Review(pitch_id=12345,pitch_title='Review for pitches',image_path="https://image.tmdb.org/t/p/w500/jdjdjdjn",pitch_review='This pitch is the best thing since sliced bread',user = self.user_nelly )

def tearDown(self):
    Review.query.delete()
    User.query.delete()

def test_check_instance_variables(self):
    self.assertEquals(self.new_review.pitch_id,12345)
    self.assertEquals(self.new_review.pitch_review,'This pitch is the best thing since sliced bread')
    self.assertEquals(self.new_review.user,self.user_nelly)

def test_save_review(self):
    self.new_review.save_review()
    self.assertTrue(len(Review.query.all())>0)

def test_get_review_by_id(self):
    self.new_review.save_review()
    got_reviews = Review.get_reviews(12345)
    self.assertTrue(len(got_reviews) == 1)