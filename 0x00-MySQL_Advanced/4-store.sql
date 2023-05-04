-- Create trigger to update item quantity after adding new order

CREATE TRIGGER decrease_item_quantity
AFTER INSERT ON orders
FOR EACH ROW UPDATE items
-- NEW has the updated data for table

SET quantity = quantity - NEW.number
WHERE items.name = NEW.item_name;