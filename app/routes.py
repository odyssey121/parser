from app import app
from app.form import MainForm
from flask import render_template, request, flash, redirect, url_for

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()
    if form.validate_on_submit():
        flash('Site name {}, container tag {}'.format(
            form.site_name.data, form.container_tag.data))
        return redirect('/')
    return render_template('index.html', token='test')

