import os
import re

from pandas import DataFrame

# Регулярные выражения для поиска ссылок
pattern_tme = r'((?:t\.me/(?:s/)?)([a-zA-Z0-9_]+)\b)'  # Паттерн для t.me и t.me/s
pattern_at = r'(@([a-zA-Z0-9_]+)\b)'  # Паттерн для @

def parse_links(df: DataFrame):
    unique_matches = set()
    rows = df.shape[0]
    for row in range(1, rows-1):
        cell = df.iat[row,3]
        if type(cell) != str:
           continue

        content = cell.splitlines()
        for i, line in enumerate(content):
            # Ищем совпадения для t.me и t.me/s
            line_matches_tme = re.findall(pattern_tme, line)
            for match in line_matches_tme:
                # Если это t.me/s/, берём всё после второго /
                if 's/' in match[0]:
                    cleaned_match = match[0].split('s/')[1].rstrip('.,')  # Берём часть после s/
                else:
                    cleaned_match = match[1].rstrip('.,')  # Берём часть после t.me/ (вторую группу)

                unique_matches.add(cleaned_match)  # Добавляем полное совпадение в множество

                # Проверяем, заканчивается ли совпадение на '_'
                if cleaned_match.endswith('_'):
                    # Если следующая строка существует, добавляем к совпадению первое слово
                    if i + 1 < len(content):
                        next_line = content[i + 1]
                        first_word = next_line.split()[0] if next_line else ''  # Получаем первое слово
                        new_match = cleaned_match + first_word  # Объединяем
                        unique_matches.discard(cleaned_match)  # Удаляем старый вариант
                        unique_matches.add(new_match)  # Добавляем новый вариант

            # Проверка на наличие слова "телеграм" или "telegram" не далее 15 символов слева от @
            for match in re.finditer(pattern_at, line):
                start_index = match.start()  # Начало совпадения
                if start_index >= 15:  # Проверяем, чтобы не выходить за пределы строки
                    left_context = line[start_index - 15:start_index]  # Получаем 15 символов слева
                else:
                    left_context = line[:start_index]  # Если строка короче 15 символов

                # Проверяем, содержится ли "телеграм" или "telegram" в левом контексте
                if 'телеграм' in left_context.lower() or 'telegram' in left_context.lower():
                    cleaned_match = match.group(0).rstrip('.,')  # Удаляем . и , в конце
                    cleaned_match = cleaned_match.lstrip('@')  # Убираем символ @
                    unique_matches.add(cleaned_match)  # Добавляем полное совпадение в множество

                    # Проверяем, заканчивается ли совпадение на '_'
                    if cleaned_match.endswith('_'):
                        # Если следующая строка существует, добавляем к совпадению первое слово
                        if i + 1 < len(content):
                            next_line = content[i + 1]
                            first_word = next_line.split()[0] if next_line else ''  # Получаем первое слово
                            new_match = cleaned_match + first_word  # Объединяем
                            unique_matches.discard(cleaned_match)  # Удаляем старый вариант
                            unique_matches.add(new_match)  # Добавляем новый вариант
    return unique_matches

def write_links(matches, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    # Сохранение результата в output.txt с добавлением https://t.me/
    with open(file_name, 'w', encoding='utf-8') as output_file:
        for match in matches:
            output_file.write(f'https://t.me/{match}\n')  # Добавляем префикс

    print(f"Найдено {len(matches)} уникальных совпадений. Результат сохранён в {file_name}")


