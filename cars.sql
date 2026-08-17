DROP TABLE IF EXISTS cars;

CREATE TABLE cars (
    car_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    release_year INTEGER NOT NULL,
    vin_code VARCHAR(17) NOT NULL UNIQUE,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    engine_volume DECIMAL(3,1) NOT NULL CHECK (engine_volume > 0.5),
    mileage INTEGER,
    is_customs_cleared BOOLEAN NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    is_sold BOOLEAN NOT NULL
);

INSERT INTO cars
(brand, model, release_year, vin_code, engine_volume, mileage, is_customs_cleared, price, description, is_sold)
VALUES
('Toyota', 'Camry', 2020, 'JTNB11HK0K3000001', 2.5, 45000, TRUE, 18500.00, 'კარგ მდგომარეობაშია', FALSE),
('BMW', '320i', 2019, 'WBA8E1C50KAH00002', 2.0, 52000, TRUE, 22000.00, 'სერვისზე დროულად დადიოდა', FALSE),
('Mercedes', 'C200', 2021, 'WDDWF8EB0MR000003', 1.5, 30000, TRUE, 28000.00, 'ახალი ავტომობილია', FALSE),
('Audi', 'A4', 2018, 'WAUZZZ8K9JA000004', 2.0, 68000, FALSE, 16500.00, 'ჩამოსაყვანია', FALSE),
('Honda', 'Civic', 2022, '2HGFC2F59NH000005', 1.5, 22000, TRUE, 21000.00, 'ძალიან კარგ მდგომარეობაშია', FALSE),
('Ford', 'Focus', 2017, '1FADP3F20HL000006', 1.6, 85000, TRUE, 9500.00, 'ეკონომიური ავტომობილი', TRUE),
('Volkswagen', 'Golf', 2020, 'WVWZZZ1KZLW000007', 1.4, 41000, TRUE, 15500.00, 'კარგ მდგომარეობაშია', FALSE),
('Lexus', 'RX350', 2019, 'JTJBZMCA5K2000008', 3.5, 60000, TRUE, 32000.00, 'კომფორტული SUV', FALSE),
('Nissan', 'Altima', 2018, '1N4BL4BV8JC000009', 2.5, 73000, FALSE, 12000.00, 'საჭიროებს მცირე შეკეთებას', TRUE),
('Hyundai', 'Tucson', 2021, 'KM8J3CAL0MU000010', 2.0, 35000, TRUE, 23000.00, 'ოჯახური ავტომობილი', FALSE);

SELECT * FROM cars;