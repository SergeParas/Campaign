-- Schéma de base de données pour l'application de campagne de satisfaction
-- Compatible MySQL

create database campaign;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE campaign (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner_id INT,
    FOREIGN KEY (owner_id) REFERENCES user(id) ON DELETE SET NULL
);

CREATE TABLE question (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(500) NOT NULL,
    campaign_id INT NOT NULL,
    FOREIGN KEY (campaign_id) REFERENCES campaign(id) ON DELETE CASCADE
);

CREATE TABLE response (
    id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_id INT NOT NULL,
    guest_identifier VARCHAR(128),
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaign(id) ON DELETE CASCADE
);

CREATE TABLE answer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    response_id INT NOT NULL,
    question_id INT NOT NULL,
    answer_text TEXT,
    FOREIGN KEY (response_id) REFERENCES response(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
);

use mysql;
GRANT INSERT, UPDATE, DELETE ON campaign.* TO `gema`@`localhost` ;
GRANT SELECT on campaign.* TO 'gema'@'localhost';
FLUSH PRIVILEGES;
 SHOW GRANTS FOR 'gema'@'localhost';