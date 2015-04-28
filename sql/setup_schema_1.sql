-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema user13-db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema user13-db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `user13-db` DEFAULT CHARACTER SET latin1 ;
USE `user13-db` ;

-- -----------------------------------------------------
-- Table `user13-db`.`Allergans`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Allergans` (
  `AllerganID` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `AllerganName` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`AllerganID`),
  UNIQUE INDEX `AllerganName_UNIQUE` (`AllerganName` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`Ingredients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Ingredients` (
  `IngredientID` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `IngredientName` VARCHAR(20) NOT NULL,
  `AmountUnit` ENUM('Unit','kg','litre') NOT NULL,
  PRIMARY KEY (`IngredientID`),
  UNIQUE INDEX `IngredientName_UNIQUE` (`IngredientName` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`AllergansInfo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`AllergansInfo` (
  `IngredientID` INT(10) UNSIGNED NOT NULL,
  `AllerganID` INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`IngredientID`, `AllerganID`),
  INDEX `fk_Ingredients_has_Allergans_Allergans1_idx` (`AllerganID` ASC),
  INDEX `fk_Ingredients_has_Allergans_Ingredients1_idx` (`IngredientID` ASC),
  CONSTRAINT `fk_Ingredients_has_Allergans_Allergans1`
    FOREIGN KEY (`AllerganID`)
    REFERENCES `user13-db`.`Allergans` (`AllerganID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Ingredients_has_Allergans_Ingredients1`
    FOREIGN KEY (`IngredientID`)
    REFERENCES `user13-db`.`Ingredients` (`IngredientID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`Categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Categories` (
  `CategoryID` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `CategoryName` VARCHAR(25) NOT NULL,
  `Description` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`CategoryID`),
  UNIQUE INDEX `CategoryName_UNIQUE` (`CategoryName` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = 'Categories of products the bakery sell';


-- -----------------------------------------------------
-- Table `user13-db`.`Incomes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Incomes` (
  `IncomeID` INT UNSIGNED NOT NULL,
  `Amount` INT UNSIGNED NOT NULL,
  `Description` VARCHAR(65) NULL,
  `Date` DATE NOT NULL,
  PRIMARY KEY (`IncomeID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`Suppliers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Suppliers` (
  `SupplierID` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `SupplierName` VARCHAR(25) NOT NULL,
  `Email` VARCHAR(25) NOT NULL,
  `PhoneNumber` VARCHAR(12) NOT NULL,
  `Address` VARCHAR(35) NOT NULL,
  `ContactName` VARCHAR(15) NOT NULL,
  `PaymentTerms` INT(7) UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (`SupplierID`),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC),
  UNIQUE INDEX `PhoneNumber_UNIQUE` (`PhoneNumber` ASC),
  UNIQUE INDEX `Address_UNIQUE` (`Address` ASC),
  UNIQUE INDEX `SupplierName_UNIQUE` (`SupplierName` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = 'All the suppliers for the materials used for baking';


-- -----------------------------------------------------
-- Table `user13-db`.`Outcomes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Outcomes` (
  `OutcomeID` INT UNSIGNED NOT NULL,
  `Amount` INT UNSIGNED NOT NULL,
  `Description` VARCHAR(65) NULL,
  `Date` DATE NOT NULL,
  PRIMARY KEY (`OutcomeID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`Orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Orders` (
  `OrderID` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `SupplierID` INT(10) UNSIGNED NOT NULL,
  `Date` DATE NOT NULL,
  `OutcomeID` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`OrderID`),
  INDEX `fk_Orders_Suppliers1_idx` (`SupplierID` ASC),
  INDEX `fk_Orders_Outcomes1_idx` (`OutcomeID` ASC),
  CONSTRAINT `fk_Orders_Suppliers1`
    FOREIGN KEY (`SupplierID`)
    REFERENCES `user13-db`.`Suppliers` (`SupplierID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Orders_Outcomes1`
    FOREIGN KEY (`OutcomeID`)
    REFERENCES `user13-db`.`Outcomes` (`OutcomeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`Supplies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Supplies` (
  `SupplyID` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `IngredientID` INT(10) UNSIGNED NOT NULL,
  `SupplierID` INT(10) UNSIGNED NOT NULL,
  `LastsFor` INT UNSIGNED NOT NULL,
  `Price` DECIMAL(5,2) UNSIGNED NOT NULL,
  PRIMARY KEY (`SupplyID`),
  INDEX `IngredientType_INDEX` (`IngredientID` ASC),
  INDEX `Supplier_INDEX` (`SupplierID` ASC),
  INDEX `fk_OrderDetails` (`SupplyID` ASC, `SupplierID` ASC),
  CONSTRAINT `fk_Supplies_Ingredients1`
    FOREIGN KEY (`IngredientID`)
    REFERENCES `user13-db`.`Ingredients` (`IngredientID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Supplies_Suppliers`
    FOREIGN KEY (`SupplierID`)
    REFERENCES `user13-db`.`Suppliers` (`SupplierID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`OrderDetails`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`OrderDetails` (
  `OrderID` INT(10) UNSIGNED NOT NULL,
  `SupplyID` INT(10) UNSIGNED NOT NULL,
  `Amount` INT UNSIGNED NOT NULL,
  `OriginalAmount` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`OrderID`, `SupplyID`),
  INDEX `fk_Supplies_has_Orders_Orders1_idx` (`OrderID` ASC),
  INDEX `fk_Supplies_has_Orders_Supplies1_idx` (`SupplyID` ASC),
  CONSTRAINT `fk_Supplies_has_Orders_Orders1`
    FOREIGN KEY (`OrderID`)
    REFERENCES `user13-db`.`Orders` (`OrderID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Supplies_has_Orders_Supplies1`
    FOREIGN KEY (`SupplyID`)
    REFERENCES `user13-db`.`Supplies` (`SupplyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`Products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Products` (
  `ProductID` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `ProductName` VARCHAR(30) NOT NULL,
  `CategoryID` INT(10) UNSIGNED NOT NULL,
  `LastsFor` INT UNSIGNED NOT NULL,
  `Price` DECIMAL(5,2) UNSIGNED NOT NULL,
  `Description` VARCHAR(65) NULL DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  UNIQUE INDEX `ProductName_UNIQUE` (`ProductName` ASC),
  INDEX `fk_Products_Categories1_idx` (`CategoryID` ASC),
  CONSTRAINT `fk_Products_Categories1`
    FOREIGN KEY (`CategoryID`)
    REFERENCES `user13-db`.`Categories` (`CategoryID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`ProductsRecepies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`ProductsRecepies` (
  `ProductID` INT(10) UNSIGNED NOT NULL,
  `IngredientID` INT(10) UNSIGNED NOT NULL,
  `Amount` FLOAT UNSIGNED NOT NULL,
  PRIMARY KEY (`ProductID`, `IngredientID`),
  INDEX `fk_Products_has_Ingredients_Ingredients1_idx` (`IngredientID` ASC),
  INDEX `fk_Products_has_Ingredients_Products1_idx` (`ProductID` ASC),
  CONSTRAINT `fk_Products_has_Ingredients_Ingredients1`
    FOREIGN KEY (`IngredientID`)
    REFERENCES `user13-db`.`Ingredients` (`IngredientID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Products_has_Ingredients_Products1`
    FOREIGN KEY (`ProductID`)
    REFERENCES `user13-db`.`Products` (`ProductID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`Sales`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Sales` (
  `SaleID` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `Date` DATE NOT NULL,
  `IncomeID` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`SaleID`),
  INDEX `fk_Sales_Incomes1_idx` (`IncomeID` ASC),
  CONSTRAINT `fk_Sales_Incomes1`
    FOREIGN KEY (`IncomeID`)
    REFERENCES `user13-db`.`Incomes` (`IncomeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`SaleDetails`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`SaleDetails` (
  `SaleID` INT(10) UNSIGNED NOT NULL,
  `ProductID` INT(10) UNSIGNED NOT NULL,
  `Amount` DECIMAL(6,2) UNSIGNED NOT NULL,
  `Discount` DECIMAL(2,2) UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (`SaleID`, `ProductID`),
  INDEX `fk_Sales_has_Products_Products1_idx` (`ProductID` ASC),
  INDEX `fk_Sales_has_Products_Sales1_idx` (`SaleID` ASC),
  CONSTRAINT `fk_Sales_has_Products_Products1`
    FOREIGN KEY (`ProductID`)
    REFERENCES `user13-db`.`Products` (`ProductID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Sales_has_Products_Sales1`
    FOREIGN KEY (`SaleID`)
    REFERENCES `user13-db`.`Sales` (`SaleID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `user13-db`.`Bakings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Bakings` (
  `BakingID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `Time` DATETIME NOT NULL,
  PRIMARY KEY (`BakingID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `user13-db`.`BakingDetails`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`BakingDetails` (
  `ProductID` INT(10) UNSIGNED NOT NULL,
  `BakingID` INT UNSIGNED NOT NULL,
  `Amount` INT UNSIGNED NOT NULL,
  `OriginalAmount` INT UNSIGNED NULL,
  PRIMARY KEY (`ProductID`, `BakingID`),
  INDEX `fk_Products_has_Bakings_Bakings1_idx` (`BakingID` ASC),
  INDEX `fk_Products_has_Bakings_Products1_idx` (`ProductID` ASC),
  CONSTRAINT `fk_Products_has_Bakings_Products1`
    FOREIGN KEY (`ProductID`)
    REFERENCES `user13-db`.`Products` (`ProductID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Products_has_Bakings_Bakings1`
    FOREIGN KEY (`BakingID`)
    REFERENCES `user13-db`.`Bakings` (`BakingID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

USE `user13-db` ;

-- -----------------------------------------------------
-- Placeholder table for view `user13-db`.`Money`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user13-db`.`Money` (`SUM(Incomes.Amount) - SUM(Outcomes.Amount)` INT);

-- -----------------------------------------------------
-- View `user13-db`.`Money`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `user13-db`.`Money`;
USE `user13-db`;
CREATE  OR REPLACE VIEW `Money` AS
    SELECT 
        SUM(Incomes.Amount) - SUM(Outcomes.Amount)
    FROM
        Incomes,
        Outcomes;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
