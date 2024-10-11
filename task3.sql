SELECT s.*
FROM souvenirs s
JOIN souvenirscategories sc ON s.idcategory = sc.id
WHERE sc.name IN ("cписок категорий")
ORDER BY s.rating ASC;

--Например
SELECT s.*
FROM souvenirs s
JOIN souvenirscategories sc ON s.idcategory = sc.id
WHERE sc.name IN ('Брелоки', 'Фонарики')
ORDER BY s.rating ASC;