SELECT 
    SupplierID AS ID,
    SupplierName AS `Name`,
    Email,
    PhoneNumber AS `Phone Number`,
    Address,
    ContactName AS `Contact Name`,
    CONCAT('net ', PaymentTerms) AS `Payment Terms`
FROM
    Suppliers