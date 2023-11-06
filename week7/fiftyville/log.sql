-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports WHERE year =2021 AND month=7 AND day=28 AND street = "Humphrey Street"; -- analyze crimes that occurred in the date and place suggested.

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time –
-- each of their interview transcripts mentions the bakery.

SELECT transcript FROM interviews WHERE year =2021 AND month=7 AND day=28 AND transcript LIKE "%bakery%"; -- to check the information in interviews related to bakery in the timetable of crime scene;

-- Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

SELECT name FROM people
WHERE license_plate IN (
    SELECT license_plate FROM bakery_security_logs
    WHERE activity ="exit" AND hour = 10 AND minute >= 15 and minute <= 25 and day=28 and year=2021 and month=7
    ); -- our suspects: name of people that owns a car that left bakery within 10 minutes: Vanessa, Barry, Iman, Sofia, Luca, Diana, Kelsey, Bruce;

--------------------------------------------------------------------------------------------------------------------------------------------
-- I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
-- I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

SELECT name FROM people
WHERE id in (
    SELECT person_id from bank_accounts
    WHERE account_number IN (
        SELECT account_number FROM atm_transactions
        WHERE day =28 and month =7 and year =2021 and transaction_type ="withdraw" and atm_location = "Leggett Street"
        )
        ); -- name of people that withdrew money with given conditions: Iman, Luca, Diana, Bruce
--------------------------------------------------------------------------------------------------------------------------------
-- As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
-- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.

SELECT city
FROM airports
WHERE id IN (
    SELECT destination_airport_id
    FROM flights
    WHERE year =2021 AND month=7 AND day=29 and origin_airport_id in (
        SELECT id from airports WHERE full_name="Fiftyville Regional Airport")
        ORDER BY hour,minute LIMIT 1
        ); -- to discover the destination of the earliest flight with origin in fiftyville in the next day of the crime

-- New York City;

SELECT name FROM people
WHERE passport_number in (
    SELECT passport_number FROM passengers
    WHERE flight_id IN (
        SELECT id FROM flights
        WHERE year =2021 AND month=7 AND day=29 and origin_airport_id in (
            SELECT id from airports
            WHERE full_name="Fiftyville Regional Airport"
            )
            ORDER BY hour LIMIT 1
            )
            ); -- name of people that flew with given conditions: Luca, Bruce

SELECT name from PEOPLE
WHERE phone_number in (
    SELECT caller FROM phone_calls
    WHERE day=28 and month=7 and year =2021 AND duration < 60
    ); -- name of people who made calls with the given conditions: Bruce

SELECT name
FROM people
WHERE name IN (
    SELECT name FROM people
    WHERE phone_number in (
        SELECT receiver FROM phone_calls
        WHERE year = 2021 AND day = 28 AND MONTH=7 and duration <60  AND caller IN (
            SELECT phone_number FROM people
            WHERE name = "Bruce"
            )
            )
            ); -- Name of people that Bruce calls in given conditions: Robin