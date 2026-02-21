-- crear_base_datos.sql
-- Ejecuta este script con un usuario con privilegios de administración (ej. root)

CREATE DATABASE IF NOT EXISTS negocio;
USE negocio;

-- Crear usuario danielcreux con solo SELECT (si no existe)
CREATE USER IF NOT EXISTS 'negocio'@'localhost' IDENTIFIED BY 'negocio';
GRANT SELECT ON empresa.* TO 'negocio'@'localhost';
FLUSH PRIVILEGES;

-- Crear tablas (requiere privilegios CREATE, por eso lo hace el admin)
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    direccion VARCHAR(100),
    poblacion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha DATE NOT NULL,
    total DECIMAL(10,2),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Crear vistas
CREATE VIEW IF NOT EXISTS seleccion_clientes AS
SELECT id, nombre, apellido, direccion, poblacion
FROM clientes;

CREATE VIEW IF NOT EXISTS clientes_resumido AS
SELECT 
    id,
    CONCAT(nombre, ' ', apellido) AS nombre_completo,
    direccion,
    poblacion,
    apellido
FROM clientes;

-- Insertar datos de ejemplo
INSERT INTO clientes (nombre, apellido, direccion, poblacion) VALUES
('Juan', 'Pérez', 'Calle Mayor 10', 'Madrid'),
('María', 'López', 'Avda. Central 5', 'Barcelona'),
('Carlos', 'Jiménez', 'Plaza Nueva 3', 'Valencia'),
('Ana', 'Jimeno', 'Calle Sol 22', 'Sevilla'),
('Luis', 'García', 'Paseo Marítimo 8', 'Málaga');

INSERT INTO productos (nombre, precio) VALUES
('Portátil', 850.00),
('Ratón', 25.50),
('Teclado', 45.00);

INSERT INTO pedidos (cliente_id, fecha, total) VALUES
(1, '2025-02-01', 850.00),
(2, '2025-02-03', 70.50),
(3, '2025-02-05', 45.00);