from datetime import datetime

from apps.recipiapp import db
# from apps.models import User

class UserRecipi(db.Model):
    __tablename__='recipes'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    username = db.Column(db.String(index=True))
    title = db.Column(db.String(50),nullable=False)
    create_at = db.Column(db.DateTime,default=datetime.now)
    image_path = db.Column(db.String)
    material = db.Column(db.String)
    how_to = db.Column(db.String)
    p = db.Column(db.Integer,nullable=False)
    f = db.Column(db.Integer,nullable=False)
    c = db.Column(db.Integer,nullable=False)
    kcal = db.Column(db.Integer,nullable=False)
    url = db.Column(db.String)

class LikeRecipi(db.Model):
    __tablename__='likerecipes'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,nullable=False)
    recipi_id = db.Column(db.Integer,nullable=False)
    like_now = db.Column(db.Integer)

# recipi_id = db.Column(db.Integer,db.ForeignKey(UserRecipi.id),nullable=False)


