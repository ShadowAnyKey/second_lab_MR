SELECT sp.*, ps.name AS status_name
FROM souvenirprocurements sp
JOIN procurementstatuses ps ON sp.idstatus = ps.id
WHERE sp.date BETWEEN 'начальная_дата' AND 'конечная_дата'
ORDER BY ps.name;

--Например
SELECT sp.*, ps.name AS status_name
FROM souvenirprocurements sp
JOIN procurementstatuses ps ON sp.idstatus = ps.id
WHERE sp.date BETWEEN '2023-01-01' AND '2023-10-31'
ORDER BY ps.name;