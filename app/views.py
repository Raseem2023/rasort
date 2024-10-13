from flask import render_template, redirect, url_for, flash, request, send_file
from app import app, db
from app.models import PhoneNumber, Blacklist  # Импортируем модели PhoneNumber и Blacklist
from app.forms import UploadFileForm, UploadBlacklistForm
from app.utils import import_phone_numbers, import_blacklist, filter_blacklist, export_cleaned_data, export_global_database
import os

@app.route('/')
def index():
    return render_template('index.html')

# Раздел 1: Загрузка нового файла с номерами
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file_path = f"/tmp/{file.filename}"
        file.save(file_path)

        # Импорт номеров из загруженного файла
        result = import_phone_numbers(file_path)

        # Фильтрация по черному списку
        deleted_count = filter_blacklist()

        flash(f"Добавлено: {result['added']}, Дубликатов: {result['duplicates']}, Удалено по блэклисту: {deleted_count}")
        return render_template('result.html', result=result, deleted_count=deleted_count)

    return render_template('upload.html', form=form)

# Раздел 2: Загрузка блэклиста
@app.route('/upload_blacklist', methods=['GET', 'POST'])
def upload_blacklist():
    form = UploadBlacklistForm()
    if form.validate_on_submit():
        file = form.file.data
        file_path = f"/tmp/{file.filename}"
        file.save(file_path)

        # Импорт блэклиста
        result = import_blacklist(file_path)
        
        # Подсчет общего количества номеров в блэклисте
        total_blacklist = Blacklist.query.count()

        flash(f"Добавлено номеров в блэклист: {result['added']}, Дубликатов: {result['duplicates']}. Всего номеров в блэклисте: {total_blacklist}")
        return render_template('result_blacklist.html', result=result, total_blacklist=total_blacklist)

    return render_template('upload_blacklist.html', form=form)

# Раздел 3: Скачать последний очищенный файл
@app.route('/download/cleaned')
def download_cleaned():
    file_path = export_cleaned_data()
    return send_file(file_path, as_attachment=True)

# Раздел 4: Скачать всю глобальную базу данных
@app.route('/download/global')
def download_global():
    file_path = export_global_database()
    return send_file(file_path, as_attachment=True)

# Очистка черного списка
@app.route('/clear_blacklist')
def clear_blacklist():
    Blacklist.query.delete()  # Удаляем все записи из таблицы Blacklist
    db.session.commit()
    flash("Черный список успешно очищен.")
    return redirect(url_for('index'))

# Очистка глобальной базы номеров
@app.route('/clear_global_database')
def clear_global_database():
    PhoneNumber.query.delete()  # Удаляем все записи из таблицы PhoneNumber
    db.session.commit()
    flash("Глобальная база номеров успешно очищена.")
    return redirect(url_for('index'))
