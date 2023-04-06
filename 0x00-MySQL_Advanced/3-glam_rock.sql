-- a SQL script that lists all bands with Glam rock
-- as their main style, ranked by their longevity

SELECT `band_name`, 
IFNULL(`split`, YEAR(CURDATE())) - IFNULL(`formed`, 0) AS `lifespan` 
FROM `metal_bands` 
WHERE LOWER(`style`) LIKE '%glam rock%'
ORDER BY 
IFNULL(`split`, YEAR(CURDATE())) - IFNULL(`formed`, 0) DESC;
