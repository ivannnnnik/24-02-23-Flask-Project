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
    def get_film_by_id(cls, id):
        film = cls.query.filter_by(id=id).first()
        if film:
            return {"id": film.id, "name": film.name, "description": film.description, "cinema_id": film.cinema_id,
                    "price": film.price, "date_premiere": film.date_premiere, "count_ticket": film.count_ticket}
        else:
            return False

    @classmethod
    def take_films(cls):
        films = cls.query.all()
        data = []
        for film in films:
            film_data = {
                "id": film.id,
                "name": film.name,
                "description": film.description,
                "cinema_id": film.cinema_id,
                "price": film.price,
                "date_premiere": film.date_premiere,
                "count_ticket": film.count_ticket
            }
            data.append(film_data)
        return data

    @classmethod
    def get_films(cls):
        films = cls.query.all()
        data = []
        for film in films:
            film_data = [film.id, film.name, film.description, film.cinema_id, film.price, film.date_premiere,
                         film.count_ticket]
            data.append(film_data)
        return data

    @classmethod
    def is_film_unq(cls, name):
        film = cls.query.filter_by(name=name).first()
        if film:
            return False
        return True


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

    @classmethod
    def get_user_by_id(cls, user_id):
        user = cls.query.filter_by(id=user_id).first()
        if user:
            return {"user_id": user.id, "name": user.name, "email": user.email, "password": user.password}
        else:
            return False

    @classmethod
    def get_user_by_email(cls, user_email):
        user = cls.query.filter_by(email=user_email).first()
        if user:
            return {"user_id": user.id, "name": user.name, "email": user.email, "password": user.password}
        else:
            return False

    @classmethod
    def get_users(cls):
        users = cls.query.all()
        data = []
        for user in users:
            user_data = [user.id, user.name, user.email, user.password]
            data.append(user_data)
        return data

    @classmethod
    def is_email_unq(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return False
        return True

    # @property
    # def is_user_real(self, email, password):
    #     user = self.query.filter_by(email=email, password=password).first()
    #     if user:
    #         return True
    #     return False


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
    def get_cinema(cls, name, address, district):
        cinema = cls.query.filter_by(name=name, address=address, district=district).first()
        if cinema:
            return {"id": cinema.id, "name": cinema.name, "address": cinema.address, "district": cinema.district}
        else:
            return False

    @classmethod
    def get_cinema_ids(cls):
        cinemas = cls.query.all()
        ids = [cinema.id for cinema in cinemas]
        return ids

    @classmethod
    def get_cinemas(cls):
        cinemas = cls.query.all()
        data = []
        for cinema in cinemas:
            cinema_data = [cinema.id, cinema.name, cinema.address, cinema.district]
            data.append(cinema_data)
        return data

# user = Users(name="kate", email="k@mail.ru",password="11111111")
# db.session.add(user)
# db.session.commit()
# user = Users(name="j", email="jjj@mail.ru", password="999999999")
# db.session.add(user)
# db.session.commit()
# cinema = Cinemas(name="h", address="pp",district="ll")
# db.session.add(cinema)
# db.session.commit()

# print(Cinemas.get_cinema("h","pp","ll"))
# print(Films.get_film_by_id(1))
# print(Cinemas.get_cinema_ids())
# print(Films.get_films())
# print(Users.get_users())
# print(Users.is_email_unq("jjjppp@mail.ru"))
# print(Films.is_film_unq("Брат"))
# print(Cinemas.get_cinemas())
# print(Users.is_user_real("jjj@mail.ru", "999999999"))
# print(Orders.taken_seats(1))
# Films.add_films('uttu','uttu',1,10,'01-01-2000',20)
# Films.delete_film('uttu')
# Users.add_user("kateee", "k@mail.ru","11111111")
# Users.delete_user("kateee")
# Cinemas.add_cinema('uttu','uttu','uttu')
print(Users.get_user_by_id(1))
