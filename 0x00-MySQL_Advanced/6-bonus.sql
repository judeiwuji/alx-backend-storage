-- a SQL script that creates a stored procedure AddBonus
-- that adds a new correction for a student.
DELIMITER $$
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    SELECT `id` FROM `projects` WHERE `name` = project_name LIMIT 1 INTO @project_id;

    IF NOT EXISTS(SELECT `id` FROM `projects` WHERE `name` = project_name LIMIT 1) THEN
        INSERT INTO `projects` (`name`) VALUES(project_name);
        SET @project_id = LAST_INSERT_ID();
    END IF;
    INSERT INTO `corrections` (`user_id`, `project_id`, `score`)
    VALUES (user_id, @project_id, score);
END$$
DELIMITER ;
