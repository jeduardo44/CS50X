SELECT title
FROM movies
JOIN stars ON stars.movie_id = movies.id
WHERE (
  stars.person_id IN (SELECT id FROM people WHERE name = "Jennifer Lawrence")
  AND
  stars.movie_id IN (
    SELECT id
    FROM movies AS sub_movies
    JOIN stars AS sub_stars ON sub_stars.movie_id = sub_movies.id
    WHERE sub_stars.person_id IN (SELECT id FROM people WHERE name = "Bradley Cooper")
  )
);
