SELECT 
    Supplies.SupplyName,
    Orders.Date,
    OrderDetails.OrderID,
    OrderDetails.SupplyID
FROM
    OrderDetails
        JOIN
    Orders ON Orders.OrderID = OrderDetails.OrderID
        JOIN
    Supplies ON OrderDetails.SupplyID = Supplies.SupplyID
WHERE
    OrderDetails.Amount > 0 # unused supplies still exists
        AND DATEDIFF(CURRENT_DATE(), Orders.Date) >= Supplies.LastsFor # supplies are rotten
	