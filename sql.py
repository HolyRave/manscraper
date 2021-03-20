query = '''SELECT s.id_contact, CONCAT(c.name, ' ', c.surname) AS `Переводчик`, CONCAT(c2.name, ' ', c2.surname) AS `Админ`, s2.telegram
FROM staff s
LEFT JOIN (
	SELECT id_contact, SUM(balance) AS balance FROM fast_translators_balance ftb JOIN staff s ON s.id = ftb.id_translator 
	WHERE ftb.date >= DATE(DATE_SUB(NOW(), INTERVAL 3 DAY)) AND ftb.date <= DATE(NOW())
	GROUP BY id_contact 
) b ON b.id_contact = s.id_contact
LEFT JOIN (
	SELECT id_contact, MAX(`date`) AS max_date
	FROM fast_translators_balance ftb JOIN staff s ON s.id = ftb.id_translator 
	GROUP BY id_contact 
) l ON l.id_contact = s.id_contact
JOIN staff s_admin ON s.id_responsible = s_admin.id
JOIN staff s_top ON s_admin.id_responsible = s_top.id
JOIN contacts c ON c.id = s.id_contact
JOIN staff s2 ON s2.id = s.id_responsible
JOIN contacts c2 ON c2.id = s2.id_contact
WHERE s.date_fired IS NULL AND s.id_position IS NULL AND (s.id_contact != 144 AND s.id_contact != 138) AND (b.balance <= 0.11 OR b.balance IS NULL)
AND s.id_contact != s_admin.id_contact
AND s.id_contact != s_top.id_contact
AND s.date_start_work <= ADDDATE(CURDATE(), interval -5 DAY)
AND s.id_responsible != -3'''
