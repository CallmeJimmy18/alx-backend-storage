-- Script creates a trigger that decreases the quantity of an item
-- after adding a new order.
DROP TRIGGER IF EXISTS dec_amount;
DELIMITER $$
CREATE TRIGGER dec_amount
AFTER INSERT on orders
FOR EACH ROW
BEGIN
   UPDATE items
      SET quantity = quantity - NEW.number
      WHERE name = NEW.item_name;
END $$
DELIMITER ;
