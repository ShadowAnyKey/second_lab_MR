SELECT DISTINCT p.*
FROM providers p
JOIN souvenirprocurements sp ON p.id = sp.idprovider
JOIN procurementsouvenirs ps ON sp.id = ps.idprocurement
JOIN souvenirs s ON ps.idsouvenir = s.id
JOIN souvenirscategories sc ON s.idcategory = sc.id
WHERE sc.name = 'Название категории';

--Например
SELECT DISTINCT p.*
FROM providers p
JOIN souvenirprocurements sp ON p.id = sp.idprovider
JOIN procurementsouvenirs ps ON sp.id = ps.idprocurement
JOIN souvenirs s ON ps.idsouvenir = s.id
JOIN souvenirscategories sc ON s.idcategory = sc.id
WHERE sc.name = 'Брелоки';