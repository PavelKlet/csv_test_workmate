Пример вывода команд
==
![](media/aggregation_avg_and_bran_eq_filter.png)
filter eq apple + aggregate avg rating. Результат avg выделен зеленым.
---
![](media/filter_brand_lt_xiaomi.png)
Фильтрация строкового формата (больше/меньше) осуществляется лексикографически, числа сравниваются по величине
---
![](media/liter_price_lt_asc_desc.png)
asc/desc сортировки с фильтрацией price lt
---
pytest -v пример запуска тестов 