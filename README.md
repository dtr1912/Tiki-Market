# TIKI MARKETPLACE REPORT
📚 Table of Contents
[Part 1: Problem Solving by SQL](#part-1-problem-solving-by-sql)

[Question 1](#question-1)

[Question 2](#question-2)

[Part 2: Logical and Problem Solving](#part-2-logical-and-proble-solving)

[Part 3: Case Study](#part-3-case-study)

## PART 1: PROBLEM SOLVING BY SQL
### QUESTION 1
A. Write a SQL query to find the best seller by each category. #sales

#sales
|   SellerID | Category    |   Sales |
|-----------:|:------------|--------:|
|          1 | Book        |     258 |
|          2 | Electronics |     299 |
|          3 | Electronics |     123 |
|          4 | Book        |     272 |
|          5 | FMCG        |     485 |
|          6 | Book        |     187 |
|          7 | FMCG        |     349 |
|          8 | FMCG        |      61 |
|          9 | Electronics |     321 |
|         10 | FMCG        |      20 |

```sql 
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
    rnk = 1;
```

Result:

|   SellerID | Category    |   Sales |
|-----------:|:------------|--------:|
|          4 | Book        |     272 |
|          9 | Electronics |     321 |
|          5 | FMCG        |     485 |




B. Write a SQL query to find of 3 best sellers in (a), how many award did they received in 2017
#award
|   Award_Year | Award           |   SellerID |
|-------------:|:----------------|-----------:|
|         2017 | Best Seller     |          9 |
|         2018 | Best Seller     |          5 |
|         2017 | Best Operations |          5 |
|         2018 | Best Quality    |         10 |
|         2018 | Best Operations |          6 |
|         2017 | Best Seller     |          4 |
|         2017 | Best Operations |          5 |
|         2017 | Best Quality    |          7 |
|         2017 | Best Quality    |         10 |

```sql
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
    b.Category;
```

Result:
|   SellerID | Category    |   Sales |
|-----------:|:------------|--------:|
|          4 | Book        |     272 |
|          9 | Electronics |     321 |
|          5 | FMCG        |     485 |


### QUESTION 2
You have one sample dataset attached to this test: #product_history: records of product’s status & stock changes from May – October 2018 (First 10 rows)

#product_history
| date       |   product_id | product_status   |   stock |
|:-----------|-------------:|:-----------------|--------:|
| 2018-10-30 |         1001 | Off              |      59 |
| 2018-10-30 |         1002 | On               |      35 |
| 2018-10-30 |         1003 | On               |      54 |
| 2018-10-30 |         1004 | Off              |      40 |
| 2018-10-30 |         1005 | On               |       5 |
| 2018-10-30 |         1006 | Off              |      20 |
| 2018-10-30 |         1007 | On               |      69 |
| 2018-10-30 |         1008 | On               |      67 |
| 2018-10-30 |         1009 | Off              |       1 |
| 2018-10-30 |         1010 | Off              |      83 |

A. Write a SQL query to find the number of product that were available for sales at the end of each month
```sql
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
    p.date ASC;
```
Result:

| date       |   num_stock |
|:-----------|------------:|
| 5/31/2018  |         237 |
| 6/30/2018  |         418 |
| 7/31/2018  |         255 |
| 8/31/2018  |         347 |
| 9/30/2018  |         226 |
| 10/30/2018 |         230 |

B. Average stock is calculated as: Total stock in a month/ total date in a month. Write a SQL query to find Product ID with the most “average stock” by month.
```sql
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
    mon;
```
Result:
|   mon | month_name   |   product_id |   avg_stock |
|------:|:-------------|-------------:|------------:|
|     5 | May          |         1009 |          59 |
|     6 | June         |         1008 |          60 |
|     7 | July         |         1007 |          56 |
|     8 | August       |         1007 |          59 |
|     8 | August       |         1009 |          59 |
|     9 | September    |         1009 |          59 |
|    10 | October      |         1001 |          56 |

## PART 2: LOGICAL AND PROBLEM SOLVING
### QUESTION :
A Seller wants to sell cosmetics on Tiki.vn. However, he concerns about the total volume he would make via Tiki.vn. Supposed you have accessed to Tiki’s data warehouse (sales record, items record…), how do you estimate the total sales he is going to have via selling on Tiki.vn? Feel free to make assumptions in the answer.

**Anwser:**

- Historical analytics to estimate total revenue:
  - Filter the data by the cosmetics category for analysis.
  - Analyze sales performance:
    - Revenue and profit
    - Average Order Value (AOV) per product
    - Number of orders
    - Conversion rate = number of viewers / number of buyers
- Analyze platform costs, shipping costs, return rate, and inventory status.
- Analyze customer experience: reviews, ratings, and delivery time.
- Additionally, to estimate sales revenue, we can analyze the customer segments targeted by the seller.
- Seasonal analytics to understand how revenue varies at different times and to determine which products should be promoted and sold at specific times to optimize revenue. For example, after analyzing the data, it is found that during the winter in the north, moisturizing products are sold more than in the summer due to the dry climate => Action: intensify marketing for high-moisture products and prepare additional inventory to meet order demand.
## PART 3: CASE STUDY
### QUESTION :
Please refer to the sample dataset tiki_test.csv attached. 
A standard Seller on Tiki usually go through these below stages: - Sign-up -> Seller’s Account Activated by Tiki Team -> Listing Product -> Stocking to make product(s) available for sales -> Having transaction
Based on the data file provided, please tell us what is going on with Tiki’s Marketplace. 
How was it performed? What are your recommendations to make it better? 
For this section, your tasks are cleaning, processing, aggregating and visualizing the outputs of one classifier to draw conclusions about its performance.

[For more details, [see at slide summary] (https://github.com/dtr1912/Tiki-Market/blob/main/Tiki%20Market.pptx).]

