SELECT name
FROM people
JOIN stars ON stars.person_id = people.id
WHERE (
  stars.movie_id IN (
    SELECT id
    FROM movies AS sub_movies
    JOIN stars AS sub_stars ON sub_stars.movie_id = sub_movies.id
    WHERE sub_stars.person_id IN (SELECT id FROM people WHERE name = "Kevin Bacon" AND birth = 1958)
  )
  AND people.id NOT IN (
    SELECT id
    FROM people
    WHERE name = "Kevin Bacon" AND birth = 1958
  )
);

