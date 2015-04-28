SELECT 
    IngredientID AS ID,
    IngredientName AS `Name`,
    CONCAT_WS(' ', SUM(Amount), AmountUnit) AS Amount
FROM
    Ingredients
        JOIN
    Supplies ON Ingredients.IngredientID = Supplies.IngredientID
        JOIN
    OrderDetails ON OrderDetails.SupplyID = Supplies.SupplyID
GROUP BY IngredientID