### Это форк оригинального парсера, переписанный на асинхронку и работаюший на сентябрь 2022

### Сбор данных с сайта объявлений об аренде и продаже недвижимости Циан`

Cianparser - это библиотека Python 3 для парсинга сайта  [Циан](http://cian.ru).
С его помощью можно получить достаточно подробные и структурированные данные по краткосрочной и долгосрочной аренде, продаже квартир, домов, танхаусов итд.

### Установка
```python
pip install cianparser
```

### Использование

Пример запуска программы в файле testing.py


```
               Start collecting information from pages..
Setting [=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>] 100%
1 page: [=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>] 100%
2 page: [=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>] 100%

{'accommodation': 'flat',
 'all_floors': 29,
 'author': 'ID 579515',
 'comm_meters': 51,
 'commissions': 0,
 'district': 'Vahitovskij',  # deprecated
 'floor': 11,
 'how_many_rooms': 2,
 'kitchen_meters': 18,
 'link': 'https://kazan.cian.ru/rent/flat/260751194/',
 'price_per_month': 25000,
 'square_meters': 51,
 'street': ' Scherbakovskij pereulok',  # deprecated
 'year_of_construction': 2014}
```

### Конфигурация
Функция *parse* имеет следующий аргументы:
* accommodation - вид жилья, к примеру, квартира, комната, дом, часть дома, таунхаус ("flat", "room", "house", "house-part", "townhouse")
* location - локация объявления, к примеру, Казань (для просмотра доступных мест используйте cianparser.list_cities())
* rooms - количество комнат, к примеру, 1, (1,3, "studio"), "studio, "all"; по умолчанию любое ("all")
* start_page - страница, с которого начинается сбор данных, по умолчанию, 1
* end_page - страница, с которого заканчивается сбор данных, по умолчанию, 100
* deal_type - тип сделки: rent or sale
#### В настоящее время функция *parse* принимает *accommodation* только с значением "flat"

### Признаки, получаемые в ходе сбора данных с предложений по долгосрочной аренде.
* Link - ссылка на это объявление
* District - район, в которой расположена квартира  # deprecated
* Price_per_month - стоимость аренды в месяц
* Commissions - коммиссиия, взымаемая в ходе первичной аренды
* kitchen_meters - количество квадратных метров кухни
* How_many_rooms - количество комнат, от 1 до 4х
* Floor - этаж, на котором расположена квартира
* Square_meters - общее количество квадратных метров
* Street - улица, в которой расположена квартира  # deprecated
* Author - автор объявления
* All_floors - общее количество этажей в здании, на котором расположена квартира
* Year_of_construction - год постройки здания, на котором расположена квартира

В некоторых объявлениях отсутсвуют данные по некоторым признакам (год постройки, жилые кв метры, кв метры кухни).
В этом случае проставляется значение -1.

### Пример исследования получаемых данных
В данном проекте можно увидеть некоторые результаты анализа полученных данных на примере сведений об объявленияъ по аренде недвижимости в городе Казань:

https://github.com/lenarsaitov/cian-data-analysis
