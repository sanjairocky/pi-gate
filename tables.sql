CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT (30) NOT NULL UNIQUE,
    mobile TEXT (10) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS address (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    address TEXT (120) NOT NULL,
    description TEXT (50),
    lat INTEGER,
    long INTEGER,
    map_loc TEXT (100),
    name TEXT (10) NOT NULL
);
CREATE TABLE IF NOT EXISTS user_address (
    user_id INTEGER(9999) NOT NULL,
    address_id INTEGER(99999) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(address_id) REFERENCES address(id)
);
CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT (30) NOT NULL UNIQUE,
    description TEXT (100) NOT NULL,
    parent_id INTEGER (999) NOT NULL,
    address_id INTEGER (99999) NOT NULL,
    created_by INTEGER (9999) NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES store (id),
    FOREIGN KEY (address_id) REFERENCES address (id),
    FOREIGN KEY (created_by) REFERENCES user (id)
);
CREATE TABLE IF NOT EXISTS store_role (
    id INTEGER(9) PRIMARY KEY NOT NULL,
    name TEXT(9) NOT NULL UNIQUE,
    description TEXT(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS user_store_role (
    user_id INTEGER(9999) NOT NULL,
    store_id INTEGER(999) NOT NULL,
    role_id INTEGER(9) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(store_id) REFERENCES store(id),
    FOREIGN KEY(role_id) REFERENCES store_role(id)
);
CREATE TABLE IF NOT EXISTS store_permission (
    name TEXT(30) PRIMARY KEY NOT NULL UNIQUE,
    description TEXT(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS store_role_permission (
    role_id INTEGER(9) NOT NULL,
    permission TEXT(30) NOT NULL,
    FOREIGN KEY(role_id) REFERENCES store_role(id),
    FOREIGN KEY(permission) REFERENCES store_permission(name)
);
CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT (50) NOT NULL UNIQUE,
    description TEXT (100) NOT NULL,
    barcode TEXT NOT NULL UNIQUE,
    mrp FLOAT NOT NULL,
    unit_id INTEGER (6) NOT NULL,
    quantity FLOAT NOT NULL,
    FOREIGN KEY (unit_id) REFERENCES unit (id)
);
CREATE TABLE IF NOT EXISTS inventory (
    product_id INTEGER(9999) NOT NULL,
    store_id INTEGER(999) NOT NULL,
    quantity FLOAT(1000) NOT NULL,
    cost_price FLOAT NOT NULL,
    selling_price FLOAT NOT NULL,
    updated_by INTEGER(9999) NOT NULL,
    updated_on DATETIME NOT NULL,
    FOREIGN KEY(product_id) REFERENCES product(id),
    FOREIGN KEY(store_id) REFERENCES store(id),
    FOREIGN KEY(updated_by) REFERENCES user(id)
);
CREATE TABLE IF NOT EXISTS unit (
    id INTEGER(6) PRIMARY KEY NOT NULL,
    name TEXT(20) NOT NULL UNIQUE,
    description TEXT(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS order_status (
    id INTEGER(9) PRIMARY KEY NOT NULL,
    name TEXT(30) NOT NULL,
    description TEXT(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS order_type (
    id INTEGER(9) PRIMARY KEY NOT NULL,
    name TEXT(30) NOT NULL,
    description TEXT(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS order (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    txn_src INTEGER NOT NULL,
    created_by INTEGER (9999) NOT NULL,
    user_id INTEGER (9999) NOT NULL,
    created_on DATETIME NOT NULL,
    updated_on DATETIME NOT NULL,
    updated_by INTEGER (9999) NOT NULL,
    status_id INTEGER (9) NOT NULL,
    total_amount FLOAT NOT NULL,
    type_id INTEGER (9) NOT NULL,
    comments TEXT NOT NULL,
    store_id INTEGER (999) NOT NULL,
    address_id INTEGER (99999) NOT NULL,
    FOREIGN KEY (created_by) REFERENCES user (id),
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (updated_by) REFERENCES user (id),
    FOREIGN KEY (status_id) REFERENCES order_status (id),
    FOREIGN KEY (type_id) REFERENCES order_type (id),
    FOREIGN KEY (store_id) REFERENCES store (id),
    FOREIGN KEY (address_id) REFERENCES address (id)
);
CREATE TABLE IF NOT EXISTS order_item (
    product_id INTEGER(9999) NOT NULL,
    order_id TEXT NOT NULL,
    quantity FLOAT NOT NULL,
    total_amount FLOAT NOT NULL,
    s_gst DECIMAL NOT NULL,
    c_gst DECIMAL NOT NULL,
    FOREIGN KEY(product_id) REFERENCES product(id),
    FOREIGN KEY(order_id) REFERENCES order(id)
);
CREATE TABLE IF NOT EXISTS store_transaction_type (
    id INTEGER(9) PRIMARY KEY NOT NULL,
    name TEXT(10) NOT NULL UNIQUE,
    description TEXT(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS store_user_transaction (
    store_id INTEGER(999) NOT NULL,
    user_id INTEGER(9999) NOT NULL,
    amount INTEGER(99999) NOT NULL,
    comments TEXT NOT NULL,
    transaction_type_id INTEGER(9) NOT NULL,
    FOREIGN KEY(store_id) REFERENCES store(id),
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(transaction_type_id) REFERENCES store_transaction_type(id)
);
CREATE TABLE IF NOT EXISTS product_tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    product_id INTEGER (9999) NOT NULL,
    name TEXT (100) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product (id)
);
CREATE TABLE IF NOT EXISTS related_product (
    from INTEGER (9999) NOT NULL,
        to INTEGER (9999) NOT NULL,
        FOREIGN KEY (
            from
        ) REFERENCES product (id),
        FOREIGN KEY (to) REFERENCES product (id)
);
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT (20) NOT NULL UNIQUE,
    description TEXT (50) NOT NULL
);
CREATE TABLE IF NOT EXISTS product_category (
    catagory_id INTEGER NOT NULL,
    product_id INTEGER(9999) NOT NULL,
    comments TEXT(50) NOT NULL,
    FOREIGN KEY(catagory_id) REFERENCES category(id),
    FOREIGN KEY(product_id) REFERENCES product(id)
);
CREATE TABLE IF NOT EXISTS user_store_due (
    user_id INTEGER(9999) NOT NULL,
    store_id INTEGER(999) NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(store_id) REFERENCES store(id)
);
CREATE TABLE IF NOT EXISTS coupon (
    id TEXT(15) PRIMARY KEY NOT NULL,
    description TEXT NOT NULL,
    amount INTEGER(6) NOT NULL,
    percent INTEGER (2) NOT NULL
);
CREATE TABLE IF NOT EXISTS coupon_category (
    category_id INTEGER NOT NULL,
    coupon_id TEXT(15) NOT NULL,
    FOREIGN KEY(category_id) REFERENCES category(id),
    FOREIGN KEY(coupon_id) REFERENCES coupon(id)
);