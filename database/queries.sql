CREATE TABLE amazon.user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE amazon.category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE amazon.product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INT,
    user_id INT,
    FOREIGN KEY (category_id) REFERENCES amazon.category(id),
    FOREIGN KEY (user_id) REFERENCES amazon.user(id)
);


INSERT INTO amazon.user (id, name, email, password)
VALUES
    (100, 'James Smith', 'james@example.com', 'james123'),
    (101, 'John Johnson', 'john@example.com', 'john123'),
    (102, 'William Brown', 'brown@example.com', 'brown123');

INSERT INTO amazon.category(id, name) VALUES(1, 'Consoles'), (2, 'Video Games'), (3, 'Home');

INSERT INTO amazon.product (name, price, stock, image_url, description, category_id, user_id)
VALUES
    ("Call of Duty: Modern Warfare", 59.99, 100, "image1.jpghttps://www.bigw.com.au/medias/sys_master/images/images/h45/h34/45446615859230.jpg", "The most thrilling first-person shooter game of the year.", 1, 100),
    ("PlayStation 5", 499.99, 50, "https://images-na.ssl-images-amazon.com/images/I/619BkvKW35L._SL1500_.jpg", "Sony's latest console with stunning graphics and amazing performance.", 2, 100),
    ("Robot Vacuum Cleaner", 199.99, 30, "https://m.media-amazon.com/images/I/61eRk8uocmS.jpg", "Automatically clean your home with this powerful robot vacuum cleaner.", 3, 100);
 
 commit;