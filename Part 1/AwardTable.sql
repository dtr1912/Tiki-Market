DROP TABLE IF EXISTS Awards;
CREATE TABLE Awards(
                   Award_Year INT,
				   Award VARCHAR(50),
				   SellerID INT
)
INSERT INTO Awards(Award_Year, Award, SellerID)
VALUES (2017, 'Best Seller', 9),
       (2018, 'Best Seller', 5),
	   (2017, 'Best Operations', 5),
	   (2018, 'Best Quality', 10),
	   (2018, 'Best Operations', 6),
	   (2017, 'Best Seller', 4),
	   (2017, 'Best Operations', 5),
	   (2017, 'Best Quality', 7),
	   (2017, 'Best Quality', 10);

SELECT * FROM Awards