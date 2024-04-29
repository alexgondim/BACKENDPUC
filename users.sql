-- Use o banco de dados userdb
USE userdb;

-- Criação da tabela users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Inserção de dados de exemplo
INSERT INTO users (username, email, hashed_password, full_name) VALUES
('user1', 'user1@example.com', 'hashedpass1', 'User One'),
('user2', 'user2@example.com', 'hashedpass2', 'User Two');

-- Verificar a inserção
SELECT * FROM users;
