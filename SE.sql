CREATE DATABASE `SE`;

USE `SE`;


CREATE TABLE Member (
    `MID` INT PRIMARY KEY AUTO_INCREMENT,
    `Type` INT NOT NULL,
    `Account` VARCHAR(255) NOT NULL UNIQUE,
    `Password` VARCHAR(255) NOT NULL,
    `Name` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
);

-- 添加角色(兩位客戶、兩位廠商、一位物流)
INSERT INTO Member (`Type`, `Account`, `Password`, `Name`) VALUES 
(1, 'user1', '1234', '客戶1'),
(1, 'user2', '5678', '客戶2'),
(2, 'user3', '1234', '廠商1'),
(2, 'user4', '5678', '廠商2'),
(3, 'logistics', 'logistics1', '物流');

CREATE TABLE Item (
    `IID` INT PRIMARY KEY AUTO_INCREMENT,
    `Name` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    `Description` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    `Price` INT NOT NULL
);

-- 添加商品
INSERT INTO Item (`Name`, `Description`, `Price`) VALUES 
('商品1', '商品1的描述', 100),
('商品2', '商品2的描述', 200),
('商品3', '商品3的描述', 300),
('商品4', '商品4的描述', 400),
('商品5', '商品5的描述', 500);
('商品6', '商品6的描述', 600);
('商品7', '商品7的描述', 700);
('商品8', '商品8的描述', 800);
('商品9', '商品9的描述', 900);
('商品10', '商品10的描述', 1000);

CREATE TABLE ORel (
    `OID1` INT NOT NULL,
    `OID2` INT NOT NULL,
    `Type` INT NOT NULL,
    `Content` INT NOT NULL,
    `State` INT,
    `Since` DATETIME NOT NULL,
    `ORID` INT PRIMARY KEY AUTO_INCREMENT
);

-- 添加商品關係
INSERT INTO ORel (`OID1`, `OID2`, `Type`, `Content`, `Since`) VALUES 
(3, 1, 1, 0, '2020-01-01 00:00:00'),
(3, 2, 1, 0, '2020-01-01 00:00:00'),
(3, 3, 1, 0, '2020-01-01 00:00:00'),
(3, 4, 1, 0, '2020-01-01 00:00:00'),
(3, 5, 1, 0, '2020-01-01 00:00:00');
(4, 6, 1, 0, '2020-01-01 00:00:00');
(4, 7, 1, 0, '2020-01-01 00:00:00');
(4, 8, 1, 0, '2020-01-01 00:00:00');
(4, 9, 1, 0, '2020-01-01 00:00:00');
(4, 10, 1, 0, '2020-01-01 00:00:00');




