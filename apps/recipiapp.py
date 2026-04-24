from flask import Flask,render_template,url_for,redirect,flash

app = Flask(__name__)

app.config.from_pyfile('settings.py')

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
db.init_app(app)
from flask_migrate import Migrate
Migrate(app,db)

from flask_login import LoginManager,login_manager

login_manager = LoginManager()
# login_manager.login_view = 'index'
login_manager.login_view = 'authapp.index'
login_manager.login_message = ''
login_manager.init_app(app)

from apps import models,forms
from apps.mainapp import models as modelrecipi
from sqlalchemy import select
import random

@app.route('/',methods=['GET','POST'])
def index():
    form = forms.SignupForm()
    #サインアップのsubmitボタンが押された時
    if form.validate_on_submit():
        user = models.User(username=form.username.data,
                           password=form.password.data)
        #ユーザーネームが重複しているか否か
        if user.is_duplicate_username():
            flash("登録済みのユーザーネームです")
            return redirect(url_for('index'))
    
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    stmt = select(modelrecipi.UserRecipi)
    entry = db.session.execute(stmt).scalars().all()
    if len(entry) >= 3:
        res = random.sample(entry, 3)
    else:
        res = entry
    # return render_template('index.html',form=form,user_recipes=entry)
    return render_template('index.html',form=form,user_recipes=res)





# @app.route('/delete/')
# @login_required
# def delete():
    # stmt = select(user_model.User).filter_by(id=user_id)
    # user_id_list = db.session.execute(stmt).scalars().all()
    # user = user_model.query.filter_by(id = user_id).first_or_404()
    # return render_template('base.html')
    # print('aiueo')
    # print(stmt)

#セッションに保存されている情報を取得する
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(models.User,user_id)

#ブループリント
from apps.authapp.views import authapp
app.register_blueprint(authapp,url_prefix='/auth')
#ブループリント
from apps.mainapp.views import mainapp
app.register_blueprint(mainapp,url_prefix='/main')



# from sqlalchemy import MetaData

# convention = {
#     "ix": 'ix_%(column_0_label)s',
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(constraint_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s"
# }

# metadata = MetaData(naming_convention=convention)
# db = SQLAlchemy(app, metadata=metadata)
