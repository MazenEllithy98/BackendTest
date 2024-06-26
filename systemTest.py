# System
# Develop an application, where a user can Post a story to their timeline. Story has a title and body. Each user can see other users’ timeline
# where they can find their stories' history. Another feature is to allow users to review a post, 
# giving it a rate out of 5 and a comment (mandatory). Additionally users can see top posts, rated by average rate. 

# Requirements:
# 1- API to add a post 
# 2- API to List User Posts with pagination 
# 3- API to List Top Posts with pagination
# 4- API to add a review to Post, make sure that multiple users can add a review to the same post at the same time. 
# 5- Test cases for the system with coverage for the parts you see are critical. 
# 6- Seed database with 50k posts, more than 20k reviews. 
# 7- No need for authentication or much user details, just a table with id and username. 
# 8- Provide ERD.
# Make sure to have all requests below 100ms on an average machine. 


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import random
from marshmallow import Schema, fields, post_load

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
fake = Faker()

# Define the database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    posts = db.relationship('Post', backref='user', lazy=True)

    def __init__(self, username):
        self.username = username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    average_rate = db.Column(db.Float, nullable=False, default=0)
    reviews = db.relationship('Review', backref='post', lazy=True)

    def __init__(self, title, body, user_id, average_rate=0):
        self.title = title
        self.body = body
        self.user_id = user_id
        self.average_rate = average_rate

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __init__(self, rate, comment, post_id):
        self.rate = rate
        self.comment = comment
        self.post_id = post_id

def seed_database():
    num_users = 1000  # Adjust as needed
    num_posts = 50000  # Adjust as needed
    num_reviews = 20000  # Adjust as needed

    # Seed Users
    for _ in range(num_users):
        username = fake.user_name()
        user = User(username=username)
        db.session.add(user)

    # Seed Posts
    for _ in range(num_posts):
        title = fake.sentence()
        body = fake.paragraph()
        user_id = random.randint(1, num_users)
        post = Post(title=title, body=body, user_id=user_id)
        db.session.add(post)

    # Seed Reviews
    for _ in range(num_reviews):
        rate = random.randint(1, 5)
        comment = fake.paragraph()
        post_id = random.randint(1, num_posts)
        review = Review(rate=rate, comment=comment, post_id=post_id)
        db.session.add(review)

    db.session.commit()
class UserSchema(Schema):
    class Meta:
        fields = ['id', 'username']

class PostSchema(Schema):
    class Meta:
        fields = ['id', 'title', 'body', 'average_rate']

    user_id = fields.Int()
    reviews = fields.Nested('ReviewSchema', many=True)

    @post_load
    def make_post(self, data, **kwargs):
        return Post(**data)

class ReviewSchema(Schema):
    class Meta:
        fields = ['id', 'rate', 'comment']

    post_id = fields.Int()

    @post_load
    def make_review(self, data, **kwargs):
        return Review(**data)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    post = Post(
        title=data['title'],
        body=data['body'],
        user_id=data['user_id'],
        average_rate=0
    )
    db.session.add(post)
    db.session.commit()
    id = post.id
    return post_schema.jsonify(post)

@app.route('/api/posts/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('size', 10, type=int)
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).paginate(page, page_size, False)
    return posts_schema.jsonify(posts.items)

@app.route('/api/top_posts', methods=['GET'])
def get_top_posts():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('size', 10, type=int)
    posts = Post.query.order_by(Post.average_rate.desc()).paginate(page, page_size, False)
    return posts_schema.jsonify(posts.items)

@app.route('/api/reviews/<int:post_id>', methods=['GET'])
def get_reviews(post_id):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('size', 10, type=int)
    post = Post.query.get_or_404(post_id)
    reviews = Review.query.filter_by(post_id=post_id).paginate(page, page_size, False)
    return reviews_schema.jsonify(reviews.items)

@app.route('/api/reviews/average_rate', methods=['POST'])
def update_average_rate():
    data = request.get_json()
    post_id = data['post_id']
    new_rate = data['rate']
    post = Post.query.get_or_404(post_id)
    current_reviews_count = len(post.reviews)
    post.average_rate = ((post.average_rate * current_reviews_count) + new_rate) / (current_reviews_count + 1)
    db.session.commit()
    return post_schema.jsonify(post)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True)


#ERD 
# User
# - id (PK)
# - username

# Post
# - id (PK)
# - title
# - body
# - user_id (FK to User)
# - average_rate

# Review
# - id (PK)
# - rate
# - comment
# - post_id (FK to Post)
