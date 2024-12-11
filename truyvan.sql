SELECT * FROM ims.product;
/*tên, giá và số lượng của các sản phẩm có giá từ 100 đến 500*/
SELECT name, price, qty 
FROM ims.product 
WHERE price BETWEEN 100 AND 500;

/*danh sách sản phẩm có số lượng (qty) nhỏ hơn 10*/
SELECT *
FROM ims.product
WHERE qty < 10;

/*các sản phẩm thuộc danh mục (Category) là 'Electronics' và có giá lớn hơn 500*/
SELECT *
FROM ims.product
WHERE Category = 'Electronics' AND price > 500;

/*Đếm số lượng sản phẩm theo từng nhà cung cấp*/
SELECT Supplier, COUNT(*) AS total_products
FROM ims.product
GROUP BY Supplier;


SELECT * FROM ims.category;

SELECT name FROM ims.category;

/*Đếm số lượng sản phẩm thuộc mỗi danh mục*/
SELECT c.name AS category_name, COUNT(p.pid) AS total_products
FROM ims.category c
LEFT JOIN ims.product p ON c.cid = p.Category
GROUP BY c.name;

SELECT * FROM ims.supplier;

/*Lấy tên và contact*/
SELECT name, contact
FROM ims.supplier;

/*Tìm nhà cung cấp có tên chứa từ khóa 'electronics' trong mô tả*/
SELECT *
FROM ims.supplier
WHERE `desc` LIKE '%electronics%';


SELECT * FROM ims.employee;

SELECT name, email FROM ims.employee;

/*lấy nhân viên có lương hơn 80000*/
SELECT *
FROM ims.employee
WHERE salary > 80000;

/*Đếm số lượng nhân viên nam và nữ*/
SELECT gender, COUNT(*) AS count
FROM ims.employee
GROUP BY gender;

/*Lấy danh sách nhân viên theo thứ tự tên (name) từ A đến Z*/
SELECT *
FROM ims.employee
ORDER BY name ASC;

/*Lấy danh sách các nhân viên có ngày sinh (dob) từ năm 1980 đến nay*/
SELECT *
FROM ims.employee
WHERE YEAR(dob) >= 1980;











