-- Question 1:
-- a. Write a SQL query to find the best seller by each category.
WITH rnk AS(
    SELECT
		SellerID,
		Category, 
		Sales,
		RANK() OVER(PARTITION BY Category ORDER BY Sales DESC) AS rnk
	FROM 
	    Sales
)
SELECT 
    SellerID, 
	Category,
	Sales
FROM 
    rnk
WHERE 
    rnk = 1

-- b. Write a SQL query to find of 3 best sellers in (a), how many award did they received in  2017.
WITH rnk AS(
    SELECT
		SellerID,
		Category, 
		Sales,
		RANK() OVER(PARTITION BY Category ORDER BY Sales DESC) AS rnk
	FROM 
	    Sales
), 
best_seller AS(
    SELECT 
		SellerID,
		Category,
		Sales  
    FROM 
        rnk
    WHERE 
	    rnk = 1   
)
SELECT 
    b.SellerID,
	b.Category,
	COUNT(a.Award) AS 'Award in 2017'
FROM   
    best_seller AS b
LEFT JOIN 
    Awards AS a ON b.SellerID = a.SellerID
WHERE 
    Award_Year = 2017
GROUP BY 
    b.SellerID,
    b.Category
-- Question 2

-- a. Write a SQL query to find the number of product that were available for sales at the end of each month

WITH end_month AS(
SELECT 
    MAX(date) AS end_month
FROM 
    product_history
GROUP BY
    MONTH(date)
)
SELECT 
    p.date,
	SUM(stock) AS num_stock
FROM 
    product_history p
JOIN 
    end_month e ON p.date = e.end_month
WHERE 
    product_status = 'On'
GROUP BY
    p.date
ORDER BY 
    p.date ASC
-- b. Average stock is calculated as: Total stock in a month/ total date in a month. Write a SQL query to find Product ID with the most “average stock” by month.
WITH avg_stock AS(
SELECT
    MONTH(date) AS mon,
    DATENAME(MONTH, date) AS month_name,
    product_id,
    SUM(stock)/COUNT(date) AS avg_stock

FROM 
    product_history
GROUP BY
    MONTH(date),
    DATENAME(MONTH, date),
	product_id
),
rnk AS(
SELECT
    mon,
	month_name,
	product_id,
	avg_stock,
	RANK() OVER(PARTITION BY mon ORDER BY avg_stock DESC) AS rnk 
FROM 
    avg_stock

)
SELECT
    mon,
	month_name,
	product_id,
	avg_stock
FROM 
    rnk 
WHERE 
    rnk =1
ORDER BY 
    mon