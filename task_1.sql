-- Кількість чатів в залежності від рівня астролога

SELECT a.astrologer_level, COUNT(c.chat_id) AS chats_number
FROM chats c
         JOIN astrologers a ON c.astrologer_id = a.astrologer_id
GROUP BY a.astrologer_level;

--Ім'я астролога, кількість користувачів, які з ним спілкувалися,
-- кількість чатів з максимальною оцінкою та максимальну тривалість чату з астрологом;

SELECT a.astrologer_name,
       COUNT(DISTINCT (user_id)) AS users_number,
       COUNT(*) FILTER (WHERE r.rating = 5) AS max_rating_chats_number,
       MAX(c.session_duration)     AS max_session_duration
FROM chats c
         JOIN ratings r ON c.chat_id = r.chat_id
         JOIN astrologers a ON c.astrologer_id = a.astrologer_id
GROUP BY a.astrologer_name;

--Ім'я астролога, середній рейтинг астролога, суму зароблених ним грошей та долю його заробітку від усієї заробленої суми.
-- Обмежте результат виконання запиту п'ятьма астрологами, доля заробітку яких була найвища.

SELECT a.astrologer_name, AVG(r.rating) AS average_rating,
SUM(cp.price * c.session_duration) AS astrologer_income,
SUM(cp.price * c.session_duration) / (SELECT SUM(cp.price * c.session_duration)FROM astrologers a
JOIN chats c ON a.astrologer_id = c.astrologer_id
JOIN chat_pricing cp ON cp.astrologer_level = a.astrologer_level) AS part_in_total_income
FROM astrologers a
JOIN chats c ON a.astrologer_id = c.astrologer_id
JOIN ratings r ON r.chat_id = c.chat_id
JOIN chat_pricing cp ON cp.astrologer_level = a.astrologer_level
GROUP BY a.astrologer_name
ORDER BY part_in_total_income DESC LIMIT 5;