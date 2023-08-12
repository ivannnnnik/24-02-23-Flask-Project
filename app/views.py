from flask import (
    render_template,
    request,
    redirect,
    url_for,
)
from flask_login import login_required, login_user, logout_user, current_user

from app import app, login_manager, db
from constants import PORT
from .UserLogin import UserLogin
from .forms import CreateUserForm, CreateCinema
from .models import Films, Users, Cinemas, Orders



@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return UserLogin().from_db(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this page"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    message = None
    if request.method == "POST":
        password = request.form["password"]
        email = request.form["email"]
        user = Users.query.filter_by(email=email, password=password).first_or_404()
        if user:
            user = UserLogin().create(user)
            login_user(user, remember=True)  # Создали пользователя и залогинили
            return redirect("/")
        else:
            message = "Неверное имя пользователя, email или пароль"
    context = {"message": message}
    return render_template("login.html", **context)


@app.route("/profile")
@login_required
def profile():
    user_id = current_user.get_id()
    user = Users.query.get(user_id)
    context = {
        'user': user
    }
    return render_template("profile.html", **context)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/signin", methods=["GET", "POST"])
def create_user():
    message = None
    form = CreateUserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if not Users.query.filter_by(email=form.email.data).first():
                email = form.email.data
                name = form.name.data
                password = form.password.data
                Users.add_user(name, email, password)
                return redirect(url_for("success"))
            else:
                return redirect(url_for("unsuccess"))
        else:
            message = "Некорректный email"
    context = {
        "message": message,
    }
    return render_template("form_users.html", form=form, **context)


@app.route("/form_users/success")
def success():
    return render_template("success.html")


@app.route("/form_users/unsuccess")
def unsuccess():
    return render_template("unsuccess.html")


@app.route("/add_film", methods=["POST", "GET"])
@login_required
def add_film():
    message = None
    cinemas = Cinemas.query.all()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cinema_id = request.form['cinema_id']
        price = request.form['price']
        date_premiere = request.form['date_premiere']
        count_ticket = request.form['count_ticket']
        if not Films.query.filter_by(name=name).first():
            Films.add_films(name, description, cinema_id, price, date_premiere, count_ticket)
            message = "Фильм добавлен"
            return redirect(url_for("films"))
        else:
            message = "Такой фильм уже существует"

    context = {
        "message": message,
        "cinemas": cinemas
    }
    return render_template("send_films.html", **context)


@app.route("/films")
@login_required
def films():
    films = Films.query.all()
    context = {
        "films": films
    }
    return render_template("form_films.html", **context)


@app.route('/buy_ticket')
@login_required
def buy():
    films = Films.query.all()
    context = {
        'films': films
    }
    return render_template("buy_ticket.html", **context)


@app.route('/buy_ticket/<film_id>', methods=['GET', 'POST'])
@login_required
def buy_cnt_ticket(film_id):
    film = Films.query.get(film_id)
    taken_tickets = Orders.query.filter_by(film_id=film_id).all()
    tickets = list(range(1, film.count_ticket + 1 - len(taken_tickets)))
    if request.method == 'POST':
        cnt_of_tickets = request.form['seat']
        return redirect(url_for("buy_ticket", cnt_of_tickets=int(cnt_of_tickets), film_id=int(film_id)))
    context = {
        'film': film,
        'tickets': tickets,
    }
    return render_template("cnttickets.html", **context)


@app.route('/buy_ticket/<film_id>/<cnt_of_tickets>', methods=['GET', 'POST'])
@login_required
def buy_ticket(film_id, cnt_of_tickets):
    cnt_of_tickets = cnt_of_tickets
    film = Films.query.get(film_id)
    taken_tickets = Orders.query.filter_by(film_id=film_id).all()
    tickets = [seat for seat in range(1, film.count_ticket + 1) if seat not in taken_tickets]
    mas_of_cnt_of_tickets = list(range(1, int(cnt_of_tickets) + 1))

    # TODO
    if request.method == 'POST':
        taken_seat = []
        for seats in range(1, int(cnt_of_tickets) + 1):
            s = 'seat'
            s += str(seats)  # seat1
            seat = request.form[s]  # seat1
            seat = int(seat[6:])  # Место 2
            Orders.add_order(film_id, seat, film.price)
            taken_seat.append(seat)
        data = list(range(1, film.count_ticket + 1))
        context_2 = {
            'data': data,
            'taken_seat': taken_seat
        }
        return render_template("order_made.html", **context_2)
    # TODO
    taken_tickets = Orders.taken_seats(film_id)
    data = list(range(1, movie_count_ticket + 1))
    context = {
        'mas_of_cnt_of_tickets': mas_of_cnt_of_tickets,
        'movie_name': movie_name,
        'movie_id': movie_id,
        'movie_cinema': movie_cinema,
        'movie_price': movie_price,
        'movie_count_ticket': movie_count_ticket,
        'tickets': tickets,
        'cnt_of_tickets': cnt_of_tickets,
        'data': data,
        'taken_tickets': taken_tickets

    }
    return render_template("order.html", **context)


@app.route("/add_cinema", methods=["POST", "GET"])
@login_required
def add_cinemas():
    # cinemas = db.get_cinemas()
    message = None
    form = CreateCinema()
    cinemas = Cinemas.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            Cinemas.add_cinema(
                form.name.data,
                form.address.data,
                form.district.data
            )
            return redirect(url_for("cinemas"))
        else:
            message = "Не хватает данных"
    context = {
        "message": message,
        "cinemas": cinemas
    }
    return render_template("cinemas.html", form=form, **context)


@app.route("/cinemas")
@login_required
def cinemas():
    message = None
    cinemas = Cinemas.get_cinemas()
    context = {
        "message": message,
        "cinemas": cinemas
    }
    return render_template("list_cinemas.html", **context)


@app.route("/cinema/delete")
def delete_cinema():
    id = request.args['cinema_id']
    Cinemas.delete_cinema(int(id))
    data = {
        'status': 'Кинотеатр успешно удален !',
        'id': id
    }
    return data


@app.route('/adding_cinema', methods=['POST'])
def adding_cinema():
    cinema_name = request.form['cinema_name']
    cinema_address = request.form['cinema_address']
    cinema_district = request.form['cinema_district']
    # TODO Функция создает и возвращает объект
    obj = Cinemas.add_cinema(
        request.form['cinema_name'],
        request.form['cinema_address'],
        request.form['cinema_district']
    )

    obj = Cinemas.get_cinema(cinema_name, cinema_address, cinema_district)
    data = {
        'status': 'success',
        'obj': obj,
        'id': obj[0]['id']
    }
    return data


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=PORT)
