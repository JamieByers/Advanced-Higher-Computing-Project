CREATE DATABASE products_database;

USE products_database;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    buyer_protection_price DECIMAL(10,2) NOT NULL DEFAULT 0.0,
    postage DECIMAL(10,2) NOT NULL DEFAULT 0.0,
    brand VARCHAR(255),
    colour VARCHAR(100),
    size VARCHAR(100),
    quality VARCHAR(100),
    `condition` VARCHAR(100), 
    location VARCHAR(255),
    payment_options TEXT,
    views INT DEFAULT 0,
    description TEXT,
    url VARCHAR(500) UNIQUE,
    uploaded VARCHAR(255),
    search_input VARCHAR(255)
);
