
USE complaint_db;

CREATE TABLE complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    contact VARCHAR(15),
    type VARCHAR(50),
    description TEXT
);
