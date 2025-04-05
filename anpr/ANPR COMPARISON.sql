-- Create database
CREATE DATABASE ANPR_Comparison;
USE ANPR_Comparison;

-- Table for Traditional ANPR
CREATE TABLE traditional_anpr (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(20),
    weather_condition ENUM('Sunny', 'Rainy', 'Harsh'),
    image_quality ENUM('High', 'Medium', 'Low'),
    processing_time FLOAT,  -- in seconds
    false_positive INT,
    false_negative INT
);

-- Table for YOLO v11 ANPR
CREATE TABLE yolo_v11_anpr (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(20),
    weather_condition ENUM('Sunny', 'Rainy', 'Harsh'),
    image_quality ENUM('High', 'Medium', 'Low'),
    processing_time FLOAT,  -- in seconds
    false_positive INT,
    false_negative INT
);

-- Insert sample data into Traditional ANPR
INSERT INTO traditional_anpr (license_plate, weather_condition, image_quality, processing_time, false_positive, false_negative)
VALUES 
('ABC123', 'Sunny', 'High', 1.5, 2, 3),
('XYZ789', 'Rainy', 'Medium', 2.1, 3, 4),
('LMN456', 'Harsh', 'Low', 3.2, 5, 6),
('PQR111', 'Sunny', 'Medium', 1.8, 2, 2),
('DEF222', 'Rainy', 'Low', 2.5, 4, 5),
('GHI333', 'Harsh', 'High', 3.0, 3, 4);

-- Insert sample data into YOLO v11 ANPR (Better Performance)
INSERT INTO yolo_v11_anpr (license_plate, weather_condition, image_quality, processing_time, false_positive, false_negative)
VALUES 
('ABC123', 'Sunny', 'High', 0.8, 0, 1),
('XYZ789', 'Rainy', 'Medium', 1.2, 1, 2),
('LMN456', 'Harsh', 'Low', 1.9, 2, 2),
('PQR111', 'Sunny', 'Medium', 1.0, 0, 0),
('DEF222', 'Rainy', 'Low', 1.5, 1, 1),
('GHI333', 'Harsh', 'High', 1.7, 1, 1);


SELECT 
    t.weather_condition,
    t.image_quality AS traditional_image_quality,
    y.image_quality AS yolo_image_quality,
    
    AVG(t.processing_time) AS traditional_avg_processing_time,
    AVG(y.processing_time) AS yolo_avg_processing_time,
    
    SUM(t.false_positive) AS traditional_false_positives,
    SUM(y.false_positive) AS yolo_false_positives,
    
    SUM(t.false_negative) AS traditional_false_negatives,
    SUM(y.false_negative) AS yolo_false_negatives
    
FROM traditional_anpr t
JOIN yolo_v11_anpr y ON t.weather_condition = y.weather_condition
GROUP BY t.weather_condition, t.image_quality, y.image_quality;
