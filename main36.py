
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date, timedelta

engine = create_engine("sqlite:///hotel.db")

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    stars = Column(Integer, nullable=False)

    rooms = relationship(
        "Room",
        back_populates="hotel",
        cascade="all, delete-orphan"
    )


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_number = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=False)
    price_per_night = Column(Float, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)

    hotel = relationship("Hotel", back_populates="rooms")

    bookings = relationship(
        "Booking",
        back_populates="room",
        cascade="all, delete-orphan"
    )


class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)

    bookings = relationship(
        "Booking",
        back_populates="guest",
        cascade="all, delete-orphan"
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)

    guest = relationship("Guest", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")


Base.metadata.create_all(engine)


def add_hotel(name, country, city, stars):
    hotel = Hotel(
        name=name,
        country=country,
        city=city,
        stars=stars
    )

    session.add(hotel)
    session.commit()

    return hotel


def add_room(room_number, floor, price_per_night, hotel_id):
    room = Room(
        room_number=room_number,
        floor=floor,
        price_per_night=price_per_night,
        hotel_id=hotel_id
    )

    session.add(room)
    session.commit()

    return room


def add_guest(first_name, last_name, email, phone):
    guest = Guest(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone
    )

    session.add(guest)
    session.commit()

    return guest


def add_booking(guest_id, room_id, check_in, check_out):
    booking = Booking(
        guest_id=guest_id,
        room_id=room_id,
        check_in=check_in,
        check_out=check_out
    )

    session.add(booking)
    session.commit()

    return booking


def get_all_hotels():
    hotels = session.query(Hotel).all()

    for hotel in hotels:
        print(
            hotel.id,
            hotel.name,
            hotel.country,
            hotel.city,
            hotel.stars
        )


def get_hotel_by_id(hotel_id):
    hotel = session.query(Hotel).filter(Hotel.id == hotel_id).first()

    if hotel:
        print(
            hotel.id,
            hotel.name,
            hotel.country,
            hotel.city,
            hotel.stars
        )
    else:
        print("Hotel not found")


def get_all_rooms():
    rooms = session.query(Room).all()

    for room in rooms:
        print(
            room.id,
            room.room_number,
            room.floor,
            room.price_per_night,
            room.hotel.name
        )


def get_guest_by_email(email):
    guest = session.query(Guest).filter(Guest.email == email).first()

    if guest:
        print(
            guest.id,
            guest.first_name,
            guest.last_name,
            guest.email,
            guest.phone
        )
    else:
        print("Guest not found")


def update_room_price(room_id, new_price):
    room = session.query(Room).filter(Room.id == room_id).first()

    if room:
        room.price_per_night = new_price
        session.commit()
        print("Room price updated")
    else:
        print("Room not found")


def delete_guest(guest_id):
    guest = session.query(Guest).filter(Guest.id == guest_id).first()

    if guest:
        session.delete(guest)
        session.commit()
        print("Guest deleted")
    else:
        print("Guest not found")


def delete_room(room_id):
    room = session.query(Room).filter(Room.id == room_id).first()

    if room:
        session.delete(room)
        session.commit()
        print("Room deleted")
    else:
        print("Room not found")


if session.query(Hotel).count() == 0:
    hotel1 = add_hotel(
        "Grand Hotel",
        "Georgia",
        "Tbilisi",
        5
    )

    hotel2 = add_hotel(
        "Tbilisi Palace",
        "Georgia",
        "Tbilisi",
        4
    )

    hotel3 = add_hotel(
        "Batumi Hotel",
        "Georgia",
        "Batumi",
        5
    )

    room1 = add_room(101, 1, 80, hotel1.id)
    room2 = add_room(102, 1, 120, hotel1.id)
    room3 = add_room(201, 2, 200, hotel1.id)

    room4 = add_room(101, 1, 70, hotel2.id)
    room5 = add_room(102, 1, 90, hotel2.id)
    room6 = add_room(201, 2, 150, hotel2.id)

    room7 = add_room(101, 1, 60, hotel3.id)
    room8 = add_room(102, 1, 110, hotel3.id)
    room9 = add_room(201, 2, 180, hotel3.id)

    guest1 = add_guest(
        "Giorgi",
        "Katamadze",
        "giorgi@gmail.com",
        "555111111"
    )

    guest2 = add_guest(
        "Nika",
        "Beridze",
        "nika@gmail.com",
        "555222222"
    )

    guest3 = add_guest(
        "Ana",
        "Maisuradze",
        "ana@gmail.com",
        "555333333"
    )

    guest4 = add_guest(
        "Luka",
        "Kapanadze",
        "luka@gmail.com",
        "555444444"
    )

    guest5 = add_guest(
        "Mari",
        "Gelashvili",
        "mari@gmail.com",
        "555555555"
    )

    today = date.today()

    add_booking(
        guest1.id,
        room1.id,
        today - timedelta(days=10),
        today + timedelta(days=2)
    )

    add_booking(
        guest1.id,
        room2.id,
        today + timedelta(days=5),
        today + timedelta(days=10)
    )

    add_booking(
        guest2.id,
        room3.id,
        today - timedelta(days=3),
        today + timedelta(days=4)
    )

    add_booking(
        guest3.id,
        room4.id,
        today + timedelta(days=1),
        today + timedelta(days=5)
    )

    add_booking(
        guest3.id,
        room5.id,
        today + timedelta(days=10),
        today + timedelta(days=15)
    )

    add_booking(
        guest4.id,
        room6.id,
        today - timedelta(days=5),
        today + timedelta(days=1)
    )

    add_booking(
        guest5.id,
        room7.id,
        today + timedelta(days=20),
        today + timedelta(days=25)
    )


print("\n--- QUERY 1 ---")

hotels_5_stars = session.query(Hotel).filter(
    Hotel.stars == 5
).all()

for hotel in hotels_5_stars:
    print(hotel.name)


print("\n--- QUERY 2 ---")

tbilisi_hotels = session.query(Hotel).filter(
    Hotel.city == "Tbilisi"
).all()

for hotel in tbilisi_hotels:
    print(hotel.name)


print("\n--- QUERY 3 ---")

cheap_rooms = session.query(Room).filter(
    Room.price_per_night < 100
).all()

for room in cheap_rooms:
    print(
        room.hotel.name,
        room.room_number,
        room.price_per_night
    )


print("\n--- QUERY 4 ---")

hotel = session.query(Hotel).filter(
    Hotel.name == "Grand Hotel"
).first()

if hotel:
    for room in hotel.rooms:
        print(
            room.room_number,
            room.price_per_night
        )


print("\n--- QUERY 5 ---")

guest = session.query(Guest).filter(
    Guest.email == "giorgi@gmail.com"
).first()

if guest:
    for booking in guest.bookings:
        print(
            booking.id,
            booking.room.room_number,
            booking.check_in,
            booking.check_out
        )


print("\n--- QUERY 6 ---")

future_bookings = session.query(Booking).filter(
    Booking.check_out > date.today()
).all()

for booking in future_bookings:
    print(
        booking.id,
        booking.guest.first_name,
        booking.room.room_number,
        booking.check_out
    )


print("\n--- QUERY 7 ---")

most_expensive_room = session.query(Room).order_by(
    Room.price_per_night.desc()
).first()

if most_expensive_room:
    print(
        most_expensive_room.hotel.name,
        most_expensive_room.room_number,
        most_expensive_room.price_per_night
    )


print("\n--- QUERY 8 ---")

room_counts = session.query(
    Hotel.name,
    func.count(Room.id)
).join(
    Room
).group_by(
    Hotel.id
).all()

for hotel_name, room_count in room_counts:
    print(
        f"{hotel_name} - {room_count} rooms"
    )


print("\n--- QUERY 9 ---")

hotels_with_3_rooms = session.query(
    Hotel.name,
    func.count(Room.id)
).join(
    Room
).group_by(
    Hotel.id
).having(
    func.count(Room.id) >= 3
).all()

for hotel_name, room_count in hotels_with_3_rooms:
    print(
        f"{hotel_name} - {room_count} rooms"
    )


print("\n--- QUERY 10 ---")

guests_with_many_bookings = session.query(
    Guest.first_name,
    Guest.last_name,
    func.count(Booking.id)
).join(
    Booking
).group_by(
    Guest.id
).having(
    func.count(Booking.id) > 1
).all()

for first_name, last_name, booking_count in guests_with_many_bookings:
    print(
        f"{first_name} {last_name} - {booking_count} bookings"
    )


print("\n--- RELATIONSHIPS ---")

hotel = session.query(Hotel).first()

if hotel:
    print(f"\nHotel: {hotel.name}")

    for room in hotel.rooms:
        print(
            "Room:",
            room.room_number,
            "Price:",
            room.price_per_night
        )


guest = session.query(Guest).first()

if guest:
    print(
        f"\nGuest: {guest.first_name} {guest.last_name}"
    )

    for booking in guest.bookings:
        print(
            "Booking:",
            booking.id,
            "Room:",
            booking.room.room_number,
            "Hotel:",
            booking.room.hotel.name
        )


booking = session.query(Booking).first()

if booking:
    print("\nBooking:", booking.id)
    print(
        "Guest:",
        booking.guest.first_name,
        booking.guest.last_name
    )
    print(
        "Room:",
        booking.room.room_number
    )
    print(
        "Hotel:",
        booking.room.hotel.name
    )
