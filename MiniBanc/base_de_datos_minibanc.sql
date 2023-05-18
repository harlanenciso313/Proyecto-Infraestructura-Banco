CREATE DATABASE minibancretob;

USE minibancretob;

CREATE TABLE Movimientos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Valor DECIMAL(10, 2),
    NumeroCuenta VARCHAR(20),
    Fecha DATE,
    TipoTransaccion VARCHAR(20)
);

CREATE TABLE Cuentas (
    NumeroCuenta VARCHAR(20) PRIMARY KEY,
    TipoCuenta VARCHAR(20),
    Saldo DECIMAL(10, 2),
    Titular VARCHAR(100)
);

CREATE TABLE Tipo_Transaccion (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Descripcion VARCHAR(100)
);
INSERT INTO Tipo_transaccion (Descripcion) 
VALUES 
    ('Transferencia'),
    ('Compra en Tienda Digital'),
    ('Pago de nómina');

INSERT INTO Cuentas (NumeroCuenta, TipoCuenta, Saldo, Titular) 
VALUES 
    (121456789, 'Cuenta de Ahorros', 1111000.00, 'Harlan Enciso'),
    (231654721, 'Cuenta Corriente', 565000.10, 'Estela Bugatti'),
    (343453795, 'Cuenta de Ahorros', 222200.50, 'Luis Stark'),
    (453456689, 'Cuenta Corriente', 223750.25, 'Ana Gaucho'),
    (563457674, 'Cuenta Corriente', 750000.55, 'Jesus Nazaret');
    
    