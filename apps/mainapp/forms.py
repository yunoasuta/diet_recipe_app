from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,FloatField
from wtforms import validators
from flask_wtf import file

class CustomFloatField(FloatField):
    default_error_messages = {
        'invalid': '数字のみ入力してください。',
    }

class UploadImageForm(FlaskForm):
    title = StringField("料理名",validators=[validators.DataRequired(message="入力ミス"),
                        validators.length(max=200,message="200文字以内で入力して下さい")])
    material = TextAreaField("材料")
    how_to = TextAreaField("作り方")
    p = CustomFloatField("p",validators=[validators.DataRequired(message="入力ミス"),
                                   validators.NumberRange(min=0, message="0以上の数字を入力してください。")])
    f = CustomFloatField("f",validators=[validators.DataRequired(message="入力ミス"),
                                   validators.NumberRange(min=0, message="0以上の数字を入力してください。")])
    c = CustomFloatField("c",validators=[validators.DataRequired(message="入力ミス"),
                                   validators.NumberRange(min=0, message="0以上の数字を入力してください。")])
    kcal = CustomFloatField("カロリー",validators=[validators.DataRequired(message="入力ミス"),
                                             validators.NumberRange(min=0, message="0以上の数字を入力してください。")])
    url = StringField("参照元url")
    image = file.FileField(validators=[file.FileRequired("画像ファイルを選択して下さい"),
                                       file.FileAllowed(['png','jpg','jpeg'],'サポートされていないファイル形式です。')])
    submit = SubmitField('投稿する')

class EditForm(FlaskForm):
    title = StringField("料理名",validators=[validators.DataRequired(message="入力ミス"),
                        validators.length(max=200,message="200文字以内で入力して下さい")])
    material = TextAreaField("材料")
    how_to = TextAreaField("作り方")
    p = CustomFloatField("p",validators=[validators.DataRequired(message="入力ミス"),
                                   validators.NumberRange(min=0, message="0以上の数字を入力してください。")])
    f = CustomFloatField("f",validators=[validators.DataRequired(message="入力ミス"),
                                   validators.NumberRange(min=0, message="0以上の数字を入力してください。")])
    c = CustomFloatField("c",validators=[validators.DataRequired(message="入力ミス"),
                                   validators.NumberRange(min=0, message="0以上の数字を入力してください。")])
    kcal = CustomFloatField("カロリー",validators=[validators.DataRequired(message="入力ミス"),
                                             validators.NumberRange(min=0, message="0以上の数字を入力してください。")])
    url = StringField("参照元url")
    image = file.FileField(validators=[file.FileAllowed(['png','jpg','jpeg'],'サポートされていないファイル形式です。')])
    submit = SubmitField('更新する')

class SearchForm(FlaskForm):
    serch_input = StringField("検索")
    submit = SubmitField('検索')


# class Delete_Form(FlaskForm):
    # submit = SubmitField('削除')
    
    

    
    