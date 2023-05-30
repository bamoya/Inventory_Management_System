--
-- Create model Category
--
CREATE TABLE `dashboard_category` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NULL, `description` longtext NULL);
--
-- Create model Product
--
CREATE TABLE `dashboard_product` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NULL, `description` longtext NULL, `price` numeric(10, 2) NULL, `quantity` integer UNSIGNED NULL CHECK (`quantity` >= 0), `category_id` bigint NULL);
--
-- Create model PurchaseOrder
--
CREATE TABLE `dashboard_purchaseorder` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `order_number` varchar(100) NULL, `order_date` date NOT NULL, `status` varchar(100) NULL, `staff_id` integer NULL);
--
-- Create model Sale
--
CREATE TABLE `dashboard_sale` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `customer` varchar(100) NULL, `sale_date` date NULL, `total_amount` numeric(10, 2) NULL, `payment_status` varchar(100) NULL);
--
-- Create model Supplier
--
CREATE TABLE `dashboard_supplier` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NULL, `email` varchar(254) NULL, `phone` varchar(20) NULL, `address` varchar(100) NULL);
--
-- Create model Stock
--
CREATE TABLE `dashboard_stock` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `quantity` integer UNSIGNED NULL CHECK (`quantity` >= 0), `date_updated` date NULL, `product_id` bigint NULL UNIQUE);
--
-- Create model SaleItem
--
CREATE TABLE `dashboard_saleitem` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `quantity` integer UNSIGNED NULL CHECK (`quantity` >= 0), `unit_price` numeric(10, 2) NULL, `total_price` numeric(10, 2) NULL, `product_id` bigint NULL, `sale_id` bigint NULL);
--
-- Create model PurchaseOrderItem
--
CREATE TABLE `dashboard_purchaseorderitem` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `quantity` integer UNSIGNED NULL CHECK (`quantity` >= 0), `unit_price` numeric(10, 2) NULL, `total_price` numeric(10, 2) NULL, `product_id` bigint NULL, `purchase_order_id` bigint NULL);
--
-- Add field supplier to purchaseorder
--
ALTER TABLE `dashboard_purchaseorder` ADD COLUMN `supplier_id` bigint NULL , ADD CONSTRAINT `dashboard_purchaseor_supplier_id_31f2b6ff_fk_dashboard` FOREIGN KEY (`supplier_id`) REFERENCES `dashboard_supplier`(`id`);
--
-- Add field supplier to product
--
ALTER TABLE `dashboard_product` ADD COLUMN `supplier_id` bigint NULL , ADD CONSTRAINT `dashboard_product_supplier_id_67953324_fk_dashboard_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `dashboard_supplier`(`id`);
ALTER TABLE `dashboard_product` ADD CONSTRAINT `dashboard_product_category_id_7057505a_fk_dashboard_category_id` FOREIGN KEY (`category_id`) REFERENCES `dashboard_category` (`id`);
ALTER TABLE `dashboard_purchaseorder` ADD CONSTRAINT `dashboard_purchaseorder_staff_id_02f5954a_fk_auth_user_id` FOREIGN KEY (`staff_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `dashboard_stock` ADD CONSTRAINT `dashboard_stock_product_id_ea96db91_fk_dashboard_product_id` FOREIGN KEY (`product_id`) REFERENCES `dashboard_product` (`id`);
ALTER TABLE `dashboard_saleitem` ADD CONSTRAINT `dashboard_saleitem_product_id_e61ffa9d_fk_dashboard_product_id` FOREIGN KEY (`product_id`) REFERENCES `dashboard_product` (`id`);
ALTER TABLE `dashboard_saleitem` ADD CONSTRAINT `dashboard_saleitem_sale_id_a5192cd3_fk_dashboard_sale_id` FOREIGN KEY (`sale_id`) REFERENCES `dashboard_sale` (`id`);
ALTER TABLE `dashboard_purchaseorderitem` ADD CONSTRAINT `dashboard_purchaseor_product_id_adf09a88_fk_dashboard` FOREIGN KEY (`product_id`) REFERENCES `dashboard_product` (`id`);
ALTER TABLE `dashboard_purchaseorderitem` ADD CONSTRAINT `dashboard_purchaseor_purchase_order_id_8d626dbc_fk_dashboard` FOREIGN KEY (`purchase_order_id`) REFERENCES `dashboard_purchaseorder` (`id`);
