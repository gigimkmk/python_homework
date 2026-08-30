
DROP TABLE IF EXISTS services CASCADE;
DROP TABLE IF EXISTS guests CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;
DROP TABLE IF EXISTS hotels CASCADE;



CREATE TABLE hotels (
    hotel_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hotel_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    stars INTEGER NOT NULL CHECK (stars BETWEEN 1 AND 5)
);



CREATE TABLE rooms (
    room_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hotel_id INTEGER NOT NULL,
    room_number INTEGER NOT NULL,
    floor INTEGER NOT NULL,
    price_per_night NUMERIC(10, 2) NOT NULL CHECK (price_per_night > 0),

    FOREIGN KEY (hotel_id)
        REFERENCES hotels(hotel_id)
        ON DELETE CASCADE,

    UNIQUE (hotel_id, room_number)
);



CREATE TABLE guests (
    guest_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    room_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(30) NOT NULL,

    FOREIGN KEY (room_id)
        REFERENCES rooms(room_id)
        ON DELETE CASCADE
);



CREATE TABLE services (
    service_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    room_id INTEGER NOT NULL,
    service_name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),

    FOREIGN KEY (room_id)
        REFERENCES rooms(room_id)
        ON DELETE CASCADE
);



INSERT INTO hotels (hotel_name, city, stars)
VALUES
('Grand Tbilisi Hotel', 'Tbilisi', 5),
('Batumi Sea Hotel', 'Batumi', 4);



INSERT INTO rooms (hotel_id, room_number, floor, price_per_night)
VALUES
(1, 101, 1, 150.00),
(1, 102, 1, 180.00),
(1, 201, 2, 220.00),

(2, 101, 1, 120.00),
(2, 102, 1, 140.00),
(2, 201, 2, 190.00);



INSERT INTO guests (room_id, first_name, last_name, phone)
VALUES
(1, 'Giorgi', 'Beridze', '555111111'),
(1, 'Nika', 'Maisuradze', '555111112'),

(2, 'Ana', 'Kapanadze', '555222221'),
(2, 'Mariam', 'Gelashvili', '555222222'),

(3, 'Luka', 'Jikia', '555333331'),
(3, 'Saba', 'Gogoladze', '555333332'),

(4, 'David', 'Smith', '555444441'),
(4, 'John', 'Brown', '555444442'),

(5, 'Emma', 'Wilson', '555555551'),
(5, 'Olivia', 'Taylor', '555555552'),

(6, 'Daniel', 'Johnson', '555666661'),
(6, 'Michael', 'Davis', '555666662');



INSERT INTO services (room_id, service_name, price)
VALUES
(1, 'Breakfast', 25.00),
(1, 'Room Cleaning', 15.00),

(2, 'Breakfast', 25.00),
(2, 'Laundry', 30.00),

(3, 'Airport Transfer', 50.00),
(3, 'Room Cleaning', 15.00),

(4, 'Breakfast', 20.00),
(4, 'Laundry', 25.00),

(5, 'Breakfast', 20.00),
(5, 'Airport Transfer', 45.00),

(6, 'Room Cleaning', 15.00),
(6, 'Laundry', 25.00);



SELECT
    rooms.room_number,
    rooms.floor,
    rooms.price_per_night,
    hotels.hotel_name
FROM rooms
JOIN hotels
    ON rooms.hotel_id = hotels.hotel_id;



SELECT
    guests.first_name,
    guests.last_name,
    guests.phone,
    rooms.room_number,
    hotels.hotel_name
FROM guests
JOIN rooms
    ON guests.room_id = rooms.room_id
JOIN hotels
    ON rooms.hotel_id = hotels.hotel_id;



SELECT
    guests.first_name,
    guests.last_name,
    guests.phone,
    rooms.room_number
FROM guests
JOIN rooms
    ON guests.room_id = rooms.room_id
JOIN hotels
    ON rooms.hotel_id = hotels.hotel_id
WHERE hotels.hotel_name = 'Grand Tbilisi Hotel';




SELECT
    hotels.hotel_name,
    COUNT(rooms.room_id) AS room_count
FROM hotels
LEFT JOIN rooms
    ON hotels.hotel_id = rooms.hotel_id
GROUP BY hotels.hotel_id, hotels.hotel_name;


SELECT
    rooms.room_number,
    hotels.hotel_name
FROM rooms
JOIN hotels
    ON rooms.hotel_id = hotels.hotel_id
LEFT JOIN services
    ON rooms.room_id = services.room_id
WHERE services.service_id IS NULL;


DELETE FROM rooms
WHERE room_id = 1;



SELECT *
FROM guests
WHERE room_id = 1;


SELECT *
FROM services
WHERE room_id = 1;



UPDATE rooms
SET price_per_night = 250.00
WHERE room_id = 2;




SELECT *
FROM rooms
WHERE room_id = 2;



UPDATE guests
SET room_id = 3
WHERE guest_id = 3;



SELECT
    guests.first_name,
    guests.last_name,
    rooms.room_number,
    hotels.hotel_name
FROM guests
JOIN rooms
    ON guests.room_id = rooms.room_id
JOIN hotels
    ON rooms.hotel_id = hotels.hotel_id
WHERE guests.guest_id = 3;