from flask import Blueprint
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
load_dotenv()

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

mainapp = Blueprint(
    'mainapp',
    __name__,
    template_folder='templates_main',
    static_folder='static_main'
)

from flask import render_template,url_for,redirect,request
from flask_login import login_required,logout_user
from sqlalchemy import select
from flask_paginate import Pagination,get_page_parameter
#ログイン後に表示される画面のルーティング
@mainapp.route('/top',methods=['GET','POST'])
@login_required
def index():
    flag = False
    keyword = None
    #レシピデータベースに入っている全ての情報を取得
    sort = request.args.get("sort")
    stmt = select(modelrecipi.UserRecipi)

    if sort == "p_desc":
        stmt = stmt.order_by(modelrecipi.UserRecipi.p.desc())
    elif sort == "p_asc":
        stmt = stmt.order_by(modelrecipi.UserRecipi.p.asc())

    elif sort == "f_desc":
        stmt = stmt.order_by(modelrecipi.UserRecipi.f.desc())
    elif sort == "f_asc":
        stmt = stmt.order_by(modelrecipi.UserRecipi.f.asc())

    elif sort == "c_desc":
        stmt = stmt.order_by(modelrecipi.UserRecipi.c.desc())
    elif sort == "c_asc":
        stmt = stmt.order_by(modelrecipi.UserRecipi.c.asc())

    elif sort == "kcal_desc":
        stmt = stmt.order_by(modelrecipi.UserRecipi.kcal.desc())
    elif sort == "kcal_asc":
        stmt = stmt.order_by(modelrecipi.UserRecipi.kcal.asc())

    else:
    # デフォルト（新しい順）
        stmt = stmt.order_by(modelrecipi.UserRecipi.create_at.desc())
    # stmt = select(modelrecipi.UserRecipi).order_by(modelrecipi.UserRecipi.create_at.desc())
    entries = db.session.execute(stmt).scalars().all()
    print(entries)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    pagination = Pagination(page=page,total=len(entries),per_page=9)
    res = entries[(page-1)*9:page*9]
    # g = current_user
    current_username = current_user.username
    print(current_username)
    # print(type(current_user))
    print('[top]')
    #カレントユーザーがいいねしたレシピのidがあるテーブルを取ってくる
    user_id = current_user.id
    like_recipi_id_list = []
    stmt = select(modelrecipi.LikeRecipi).filter_by(user_id=user_id)
    
    user_like_list = db.session.execute(stmt).scalars().all()

    #いいねしたレシピのidをリストにまとめる
    for user_like in user_like_list:
        like_recipi_id_list.append(user_like.recipi_id)
    print('start')
    print(like_recipi_id_list)
    print('end')
    like_id_dict = {}
    print(type(like_id_dict))
    for like_recipi_id in like_recipi_id_list:
        like_id_dict[like_recipi_id] = True
        print(type(like_id_dict[like_recipi_id]))
    print(like_id_dict)
    
    
    if request.method == 'POST':
        flag = True
        key_recipi = []
        keyword = request.form['kensaku']
        for recipi in entries:
            if (keyword in recipi.title) or (keyword in recipi.material): 
                key_recipi.append(recipi)


        res = key_recipi[(page-1)*9:page*9]
        pagination = Pagination(page=page,total=len(key_recipi),per_page=9)
                # key_recipi = []
        print(key_recipi)
        # return render_template('top.html',user)
    
    
    
    return render_template('top.html',user_recipis=res,pagination=pagination,username=current_username,keyword=keyword,flag=flag,like_id_dict=like_id_dict)

#imagesフォルダー内の画像ファイルのパスを返す機能
from flask import send_from_directory

@mainapp.route('/images/<path:filename>')
def image_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],filename)


@mainapp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authapp.index'))

import uuid
from pathlib import Path
from flask_login import current_user
from flask import current_app

from apps.recipiapp import db
from apps.mainapp import forms
from apps.mainapp import models as modelrecipi

# @mainapp.route('/upload',methods=['GET','POST'])
# @login_required
# def upload():
#     form = forms.UploadImageForm()
#     if form.validate_on_submit():
#         file = form.image.data
#         suffix = Path(file.filename).suffix
#         imagefile_uuid = str(uuid.uuid4()) + suffix
#         image_path = Path(current_app.config['UPLOAD_FOLDER']) / imagefile_uuid
#         file.save(str(image_path))

#         upload_data = modelrecipi.UserRecipi(
#             username = current_user.username,
#             title = form.title.data,
#             material = form.material.data,
#             how_to = form.how_to.data,
#             p = int(form.p.data),
#             f = int(form.f.data),
#             c = int(form.c.data),
#             kcal = int(form.kcal.data),
#             url = form.url.data,
#             image_path = imagefile_uuid
#         )
#         db.session.add(upload_data)
#         db.session.commit()
#         # return None
#         return redirect(url_for('mainapp.index'))
    
#     return render_template('upload.html',form = form)
@mainapp.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    form = forms.UploadImageForm()
    if form.validate_on_submit():
        file = form.image.data
        # Cloudinaryにアップロード
        result = cloudinary.uploader.upload(file)
        image_url = result['secure_url']  # CloudinaryのURLを取得

        upload_data = modelrecipi.UserRecipi(
            username = current_user.username,
            title = form.title.data,
            material = form.material.data,
            how_to = form.how_to.data,
            p = int(form.p.data),
            f = int(form.f.data),
            c = int(form.c.data),
            kcal = int(form.kcal.data),
            url = form.url.data,
            image_path = image_url  # UUIDの代わりにURLを保存
        )
        db.session.add(upload_data)
        db.session.commit()
        return redirect(url_for('mainapp.index'))
    
    return render_template('upload.html',form=form)

@mainapp.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    recipi = db.session.get(modelrecipi.UserRecipi,id)
    if recipi is None or recipi.username != current_user.username:
        return redirect(url_for('mainapp.index'))
    form = forms.EditForm()
    if form.validate_on_submit():
        recipi.title = form.title.data
        recipi.material = form.material.data
        recipi.how_to = form.how_to.data
        recipi.p = int(form.p.data)
        recipi.f = int(form.f.data)
        recipi.c = int(form.c.data)
        recipi.kcal = int(form.kcal.data)
        recipi.url = form.url.data
        # if form.image.data:
        #     file = form.image.data
        #     suffix = Path(file.filename).suffix
        #     imagefile_uuid = str(uuid.uuid4()) + suffix
        #     image_path = Path(current_app.config['UPLOAD_FOLDER']) / imagefile_uuid
        #     file.save(str(image_path))
        #     recipi.image_path = imagefile_uuid
        if form.image.data:
            file = form.image.data
            # Cloudinaryにアップロード
            result = cloudinary.uploader.upload(file)
            image_url = result['secure_url']
            recipi.image_path = image_url  # URLを保存
        db.session.commit()
        return redirect(url_for('mainapp.show_detail',id=id))
    elif request.method == 'GET':
        form.title.data = recipi.title
        form.material.data = recipi.material
        form.how_to.data = recipi.how_to
        form.p.data = recipi.p
        form.f.data = recipi.f
        form.c.data = recipi.c
        form.kcal.data = recipi.kcal
        form.url.data = recipi.url
    return render_template('edit.html',form=form, recipi=recipi)

@mainapp.route('/detail/<int:id>')
@login_required
def show_detail(id):
    detail = db.session.get(modelrecipi.UserRecipi,id)
    print(detail)
    is_owner = detail.username == current_user.username
    return render_template('detail.html',detail=detail, is_owner=is_owner)

# from apps import models as user_model

@mainapp.route('/userpage/<username>')
@login_required
def userpage(username):
    stmt = select(modelrecipi.UserRecipi).filter_by(username=username)
    user_recipi = db.session.execute(stmt).scalars().all()
    page = request.args.get(get_page_parameter(),type=int,default=1)
    res = user_recipi[(page-1)*9:page*9]
    pagination = Pagination(page=page,total=len(user_recipi),per_page=9)
    return render_template('userpage.html',user_recipes=res,pagination=pagination)

@mainapp.route('/mypage/<username>')
@login_required
def mypage(username):
    stmt = select(modelrecipi.UserRecipi).filter_by(username=username)
    current_user_recipi = db.session.execute(stmt).scalars().all()
    page = request.args.get(get_page_parameter(),type=int,default=1)
    res = current_user_recipi[(page-1)*9:page*9]
    pagination = Pagination(page=page,total=len(current_user_recipi),per_page=9)
    return render_template('mypage.html',user_recipes=res,pagination=pagination)


@mainapp.route('/delete/<username>')
@login_required
def delete(username):
    print('[delete]')
    print(username)
    stmt = select(modelrecipi.UserRecipi).filter_by(username=username)
    current_user_recipi = db.session.execute(stmt).scalars().all()
    print(current_user_recipi)
    # stmt,a = select(user_model.User).filter_by(id)
    # user_id_list = db.session.execute(stmt).scalars().all()
    # user = user_model.query.filter_by(id).first_or_404()
    return render_template('delete.html',user_recipes=current_user_recipi)
    # print('aiueo')
    # print(stmt)

@mainapp.route('/delete_recipi/<int:id>')
@login_required
def delete_recipi(id):
    print('[delete_recipi]')
    print(id)
    # form=forms.Delete_Form
    # if form.validate_on_submit():
    entry=db.session.get(modelrecipi.UserRecipi,id)
    db.session.delete(entry)
    db.session.commit()
    stmt = select(modelrecipi.LikeRecipi).filter_by(recipi_id=id)
    like_this_recipes = db.session.execute(stmt).scalars().all()
    for like_this_recipi in like_this_recipes:
        db.session.delete(like_this_recipi)
        db.session.commit()
    
    return redirect(url_for('mainapp.delete',username=current_user.username))

    
# @mainapp.route('/top/<keyword>')
# @login_required
# def search_recipi(keyword):
#     print(keyword)

@mainapp.route('/like_view')
@login_required
def like_view():
        like_recipi_id_list = []
        user_id = current_user.id
        #カレントユーザーのいいねしたレシピ一覧を取ってくる
        stmt = select(modelrecipi.LikeRecipi).filter_by(user_id=user_id)
        user_like_list = db.session.execute(stmt).scalars().all()
        #いいねしたレシピ一覧のレシピidをリストにまとめる
        for user_like in user_like_list:
            like_recipi_id_list.append(user_like.recipi_id)
        # print(user_like_list.recipi_id)
        #いいねしたレシピ一覧のidのレシピを全て取ってくる
        # like_recipes = db.session.query(modelrecipi.UserRecipi).filter(modelrecipi.UserRecipi.id.in_(like_recipi_id_list))
        stmt = select(modelrecipi.UserRecipi).filter(modelrecipi.UserRecipi.id.in_(like_recipi_id_list))
        like_recipes = db.session.execute(stmt).scalars().all()
        page = request.args.get(get_page_parameter(),type=int,default=1)
        res = like_recipes[(page-1)*9:page*9]
        pagination = Pagination(page=page,total=len(like_recipes),per_page=9)
        # for recipi_id in like_recipi_id_list:
        #     stmt = select(modelrecipi.LikeRecipi).filter_by(recipi_id=recipi_id)
        #     user_like_list = db.session.execute(stmt).scalars().all()
        return render_template('like.html',like_recipes=res,pagination=pagination)

@mainapp.route('/like_delete/<int:id>')
@login_required
def like_delete(id):
        stmt = select(modelrecipi.LikeRecipi).filter_by(user_id=current_user.id,recipi_id=id)
        user_like_list = db.session.execute(stmt).scalars().all()
        for user_like in user_like_list:
            db.session.delete(user_like)
            db.session.commit()
        
        return redirect(url_for('mainapp.like_view'))



import json

@mainapp.route('/like_post',methods=["POST"])
def like_post():
    if request.method == "POST":
        like_num = request.form["like_num"]
        recipi_id = request.form["recipi_id"]
        user_id = current_user.id
        stmt = select(modelrecipi.LikeRecipi).filter_by(recipi_id=recipi_id,user_id=user_id)
        user_like_recipi = db.session.execute(stmt).scalars().all()
        if len(user_like_recipi) == 0:
            like_data = modelrecipi.LikeRecipi(
                user_id = user_id,
                recipi_id = recipi_id,
                like_now = like_num
            )
            db.session.add(like_data)
            db.session.commit()
            message = like_num + '_success'
        else:
            for u_like_recipi in user_like_recipi:
                db.session.delete(u_like_recipi)
                db.session.commit()
            message = 'delete'

        dict = {"answer": message}
    return json.dumps(dict)


# @mainapp.route('/user-list/<int:user_id>')