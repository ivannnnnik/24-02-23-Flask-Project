from app import db, login_manager


class Films(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    cinema_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    date_premiere = db.Column(db.Date)
    count_ticket = db.Column(db.Integer)

    @classmethod
    def add_films(cls, name, description, cinema_id, price, date_premiere, count_ticket):
        new_film = cls(name=name, description=description, cinema_id=cinema_id, price=price,
                       date_premiere=date_premiere, count_ticket=count_ticket)
        db.session.add(new_film)
        db.session.commit()
        print(f"Добавлен новый фильм: {name}")

    @classmethod
    def delete_film(cls, name):
        film = cls.query.filter_by(name=name).first()
        if film:
            db.session.delete(film)
            db.session.commit()
            print(f"Фильм {name} удален")
        else:
            print(f"Фильм {name} не найден")

    @classmethod
    def get_films(cls):
        films = cls.query.all()
        data = []
        for film in films:
            film_data = [film.id, film.name, film.description, film.cinema_id, film.price, film.date_premiere,
                         film.count_ticket]
            data.append(film_data)
        return films


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))

    @classmethod
    def add_user(cls, name, email, password):
        user = cls(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        print(f"Добавлен новый пользователь: {name}")

    @classmethod
    def delete_user(cls, name):
        user = cls.query.filter_by(name=name).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"Пользователь {name} удален")
        else:
            print(f"Пользователь {name} не найден")


class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer)
    number = db.Column(db.Integer)
    price = db.Column(db.Integer)

    @classmethod
    def add_order(cls, film_id, number, price):
        order = cls(film_id=film_id, number=number, price=price)
        db.session.add(order)
        db.session.commit()
        print(f"Добавлен новый заказ")

    @classmethod
    def taken_seats(cls, film_id):
        data = []
        orders = cls.query.filter_by(film_id=film_id).all()
        for order in orders:
            data.append(order.number)
        return data


class Cinemas(db.Model):
    __tablename__ = 'cinemas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(128))
    district = db.Column(db.String(128))

    @classmethod
    def add_cinema(cls, name, address, district):
        cinema = cls(name=name, address=address, district=district)
        db.session.add(cinema)
        db.session.commit()
        print(f"Добавлен новый кинотеатр: {name}")
        return cinema

    @classmethod
    def delete_cinema(cls, id):
        cinema = cls.query.filter_by(id=id).first()
        if cinema:
            db.session.delete(cinema)
            db.session.commit()
            print(f"Кинотеатр {id} удален")
        else:
            print(f"Кинотеатр {id} не найден")

    @classmethod
    def get_cinemas(cls):
        cinemas = cls.query.all()
        data = []
        for cinema in cinemas:
            cinema_data = [cinema.id, cinema.name, cinema.address, cinema.district]
            data.append(cinema_data)
        return data
