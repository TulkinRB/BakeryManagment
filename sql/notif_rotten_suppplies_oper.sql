UPDATE OrderDetails 
SET 
    amount = 0
WHERE
    OrderID = %s AND SupplyID = %s