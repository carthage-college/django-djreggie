SELECT
    student_id, COUNT(student_id) 
FROM
    cc_stg_undergrad_candidacy
GROUP BY
    student_id
HAVING
    COUNT(student_id) > 1
