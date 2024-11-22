#!/bin/bash

cd /app || exit

#Запускаем c Url
now=$(date)
echo "Конвертор стартовал $now"
url=https://www.mvd.gov.by/ru/news/8642
echo "Текущий документ:" $url
python3 main.py ${url}
