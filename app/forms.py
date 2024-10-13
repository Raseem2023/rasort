from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class UploadFileForm(FlaskForm):
    file = FileField('Загрузите файл с номерами', validators=[
        FileRequired(),
        FileAllowed(['csv', 'txt'], 'Только файлы .csv и .txt!')
    ])
    submit = SubmitField('Загрузить')

class UploadBlacklistForm(FlaskForm):
    file = FileField('Загрузите файл с блэклистом', validators=[
        FileRequired(),
        FileAllowed(['csv', 'txt'], 'Только файлы .csv и .txt!')
    ])
    submit = SubmitField('Загрузить блэклист')
