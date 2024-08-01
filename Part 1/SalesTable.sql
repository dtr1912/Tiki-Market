DROP TABLE IF EXISTS Sales;
CREATE TABLE Sales (
                    SellerID INT NOT NULL,
					Category VARCHAR(25),
					Sales DECIMAL(10,2),
					PRIMARY KEY (SellerID)
);

INSERT INTO Sales(SellerID, Category, Sales)
VALUES (1, 'Book', 258),
       (2, 'Electronics', 299),
	   (3, 'Electronics', 123),
	   (4, 'Book', 272),
	   (5, 'FMCG', 485),
	   (6, 'Book', 187),
	   (7, 'FMCG', 349),
	   (8, 'FMCG', 61),
	   (9, 'Electronics', 321),
	   (10, 'FMCG', 20);

