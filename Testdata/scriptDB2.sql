CREATE TABLE scriptDB2 (
  customer_id INT PRIMARY KEY,
    name VARCHAR(255),
    monthly_savings DECIMAL(10, 2)
);

INSERT INTO scriptDB2 (customer_id, name, monthly_savings)
VALUES
(1, 'Alice Johnson', 500),
(2, 'Bob Smith', 1000),
(3, 'Carol White', 750),
(4, 'David Green', 600),
(5, 'Emma Black', 800);
