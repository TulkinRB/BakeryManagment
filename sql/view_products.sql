SELECT 
    ProductID AS ID,
    ProductName AS `Name`,
    CategoryName AS Category,
    SUM(Amount) AS Amount,
    CONCAT(LastsFor, ' Days') AS `Lasts For`,
    CONCAT(Price, '₪') AS Price,
    Description
FROM
    Products
        LEFT JOIN
    Categories ON Categories.CategoryID = Products.CategoryID
        LEFT JOIN
    BakingDetails ON BakingDetails.ProductID = Products.ProductID
GROUP BY Products.ProductID