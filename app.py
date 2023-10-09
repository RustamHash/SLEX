from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd


from models.dBase import User, db
from models.UserLogin import UserLogin

from forms.forms import LoginForm, AuthForm, EditUserForm

# <editor-fold desc="Конфигурация">
app = Flask(__name__)
app.config['SECRET_KEY'] = r'\x08t}\tJ\xca\xff:Lk\xdc\x19\x07\x00/\xd6I\x83\xa8\x96Vb\x95\x1f\xb5\xac"\xd2tm\xc4\xed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vl_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "error"


# </editor-fold>

# <editor-fold desc="Работа с БД">
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


user_list = None


@app.before_request
def before_request():
    db.create_all()
    global user_list
    user_list = User.query.all()


# </editor-fold>


@app.route('/')
@login_required
def index():  # put application's code here
    return render_template('index.html')


# <editor-fold desc="Панель администратора">
@app.route('/Админка', methods=['GET', 'POST'])
@login_required
def admin():
    print(current_user.role)
    if current_user.role:
        return render_template('admin/admin.html', title="Админка")
    else:
        flash('У вас не достаточно прав для доступа', 'error')
    return redirect(url_for('index'))


@app.route('/Добавить пользователя', methods=['GET', 'POST'])
def create_user():
    form = AuthForm()
    if form.validate_on_submit():
        _username = form.username.data
        _password = str(form.password.data)
        _role = form.role.data
        user = User.get_user_name(_username)
        if user is None:
            user = User()
            user.username = _username
            user.password = _password
            user.role = _role
            user.add_user()
            flash('Пользователь успешно добавлен', 'success')
            return render_template('admin/admin.html', title="Админка")
    else:
        flash('Ошибка ввода данных', 'error')
    return render_template('admin/create_user.html', form=form)


@app.route('/Редактировать пользователя', methods=['GET', 'POST'])
def edit_user():
    _user_list = User.get_users()
    form = EditUserForm(default={'admin':True})

    if request.method == 'POST':
        params = request.form.to_dict(flat=False)
        print(params)
        df = pd.DataFrame.from_dict(params, orient='index')
        return render_template('admin/edit_user.html', title="Редактирование", params=df.to_html())
    return render_template('admin/edit_user.html', title="Редактирование", user_list=_user_list, form=form)


@app.route('/Удалить пользователя', methods=['GET', 'POST'])
def delete_user():
    pass


# </editor-fold>

# <editor-fold desc="Вход/Выход в приложение">
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    form.username.choices = user_list
    # if form.validate_on_submit():
    if request.method == 'POST':
        _username = form.username.data
        _password = generate_password_hash(str(form.password.data))
        user = User.get_user_name(_username)
        print(check_password_hash(_password, str(user.password)))
        if check_password_hash(_password, str(user.password)):
            flash('Вы успешно авторизовались', 'success')
            user_login = UserLogin().create(user.user_id)
            login_user(user_login)
            return redirect(url_for('index'))
        else:
            flash('Неверный пароль', 'error')
    return render_template('login.html', form=form)


@app.route("/logout/")
def logout():
    flash(f"Пользователь: {current_user} успешно вышел!", "success")
    logout_user()
    return redirect(url_for("login"))


# </editor-fold>

# <editor-fold desc="Обработка ошибок">
@app.errorhandler(404)
def page_not_found(e):
    flash(f'Страница еще не придумана!!! КУДА ТЫ ЖМЕШЬ???', 'error')
    return render_template('index.html'), 404


# </editor-fold>


if __name__ == '__main__':
    db.create_all()
    app.run()
