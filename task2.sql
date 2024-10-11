SELECT
    sp.ID AS ProcurementID,
    sp.Date AS ProcurementDate,
    p.Name AS ProviderName,
    ps.Name AS StatusName,
    s.ID AS SouvenirID,
    s.Name AS SouvenirName,
    s.ShortName AS SouvenirShortName,
    psou.Amount,
    psou.Price
FROM
    souvenirprocurements sp
    JOIN providers p ON sp.IdProvider = p.ID
    JOIN procurementstatuses ps ON sp.IdStatus = ps.ID
    JOIN procurementsouvenirs psou ON sp.ID = psou.IdProcurement
    JOIN souvenirs s ON psou.IdSouvenir = s.ID
WHERE
    sp.Date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD';

--Например
SELECT
    sp.ID AS ProcurementID,
    sp.Date AS ProcurementDate,
    p.Name AS ProviderName,
    ps.Name AS StatusName,
    s.ID AS SouvenirID,
    s.Name AS SouvenirName,
    s.ShortName AS SouvenirShortName,
    psou.Amount,
    psou.Price
FROM
    souvenirprocurements sp
    JOIN providers p ON sp.IdProvider = p.ID
    JOIN procurementstatuses ps ON sp.IdStatus = ps.ID
    JOIN procurementsouvenirs psou ON sp.ID = psou.IdProcurement
    JOIN souvenirs s ON psou.IdSouvenir = s.ID
WHERE
    sp.Date BETWEEN '2023-01-01' AND '2023-12-31';