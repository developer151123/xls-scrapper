import os
import re
from typing import NamedTuple

import xlsxwriter
from pandas import DataFrame

# Регулярные выражения для поиска ссылок
pattern_tme = r'((?:t\.me/(?:s/)?)([a-zA-Z0-9_]+)\b)'  # Паттерн для t.me и t.me/s
pattern_tme_only = r'((?:t\.me/))'  # Паттерн для t.me и t.me/s с окончанием на /
pattern_at = r'(@([a-zA-Z0-9_]+)\b)'  # Паттерн для @
pattern_next_line = r'(([a-zA-Z0-9_+]+)\b)'  # Паттерн для next line

class TelegramLink(NamedTuple):
    match: str
    justification: str
    date: str

def parse_links(df: DataFrame):
    telegram_links = []
    unique_matches = set()
    rows = df.shape[0]
    for row in range(1, rows):
        for col in range(3, 4):
            cell = df.iat[row,col]
            if type(cell) != str:
               continue

            content = cell.splitlines()
            for i, line in enumerate(content):
                pattern_found = False

                # Ищем совпадения для t.me и t.me/s
                line_matches_tme = re.findall(pattern_tme, line)
                for match in line_matches_tme:
                    pattern_found = True
                    # Если это t.me/s/, берём всё после второго /
                    if 's/' in match[0]:
                        cleaned_match = match[0].split('s/')[1].rstrip('.,')  # Берём часть после s/
                    else:
                        cleaned_match = match[1].rstrip('.,')  # Берём часть после t.me/ (вторую группу)

                    final_match = cleaned_match

                    # Проверяем, заканчивается ли совпадение на '_'
                    if cleaned_match.endswith('_'):
                        # Если следующая строка существует, добавляем к совпадению первое слово
                        if i + 1 < len(content):
                            next_line = content[i + 1]
                            first_word = next_line.split()[0] if next_line else ''  # Получаем первое слово
                            new_match = cleaned_match + first_word  # Объединяем
                            final_match = new_match
                    else: # Cовпадение не заканчивается на '_'
                        # Если следующая строка существует и есть продолжение
                        if i + 1 < len(content):
                            next_line = content[i + 1]
                            next_line_matches = re.match(pattern_next_line, next_line)
                            if next_line_matches:
                                first_word = next_line.split()[0] if next_line else ''  # Получаем первое слово
                                new_match = cleaned_match + first_word  # Объединяем
                                final_match = new_match

                    if len(final_match) > 0:
                        telegram_links.append(TelegramLink(final_match, df.iat[row,5], df.iat[row,7]))

                # Проверка на наличие слова "телеграм" или "telegram" не далее 15 символов слева от @
                for match in re.finditer(pattern_at, line):
                    pattern_found = True
                    final_match = ""
                    start_index = match.start()  # Начало совпадения
                    if start_index >= 15:  # Проверяем, чтобы не выходить за пределы строки
                        left_context = line[start_index - 15:start_index]  # Получаем 15 символов слева
                    else:
                        left_context = line[:start_index]  # Если строка короче 15 символов

                    # Проверяем, содержится ли "телеграм" или "telegram" в левом контексте
                    if 'телеграм' in left_context.lower() or 'telegram' in left_context.lower() or start_index == 0:
                        cleaned_match = match.group(0).rstrip('.,')  # Удаляем . и , в конце
                        cleaned_match = cleaned_match.lstrip('@')  # Убираем символ @
                        final_match = cleaned_match

                        # Проверяем, заканчивается ли совпадение на '_'
                        if cleaned_match.endswith('_'):
                            # Если следующая строка существует, добавляем к совпадению первое слово
                            if i + 1 < len(content):
                                next_line = content[i + 1]
                                first_word = next_line.split()[0] if next_line else ''  # Получаем первое слово
                                new_match = cleaned_match + first_word  # Объединяем
                                final_match = cleaned_match

                    if len(final_match) > 0:
                        telegram_links.append(TelegramLink(final_match, df.iat[row,5], df.iat[row,7]))

                if pattern_found:
                    continue

                line_matches_tme_only = re.findall(pattern_tme_only, line)
                for match in line_matches_tme_only:
                    pattern_found = True
                    # Если это t.me/s/, берём всё после второго /
                    if 's/' in match[0]:
                        cleaned_match = match[0].split('s/')[1].rstrip('.,')  # Берём часть после s/
                    else:
                        cleaned_match = match[1].rstrip('.,')  # Берём часть после t.me/ (вторую группу)

                    final_match = cleaned_match
                    # Если следующая строка существует и есть продолжение
                    if i + 1 < len(content):
                        next_line = content[i + 1]
                        next_line_matches = re.match(pattern_next_line, next_line)
                        if next_line_matches:
                            first_word = next_line.split()[0] if next_line else ''  # Получаем первое слово
                            new_match = cleaned_match + first_word  # Объединяем
                            final_match = new_match
                            if len(final_match) > 0:
                                telegram_links.append(TelegramLink(final_match, df.iat[row, 5], df.iat[row, 7]))

    return telegram_links

def write_links(links, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    worksheet.set_column('A:A', 100)
    worksheet.set_column('B:B', 200)
    worksheet.set_column('C:C', 50)

    worksheet.write('A1', 'Kанал')
    worksheet.write('B1', 'Решение')
    worksheet.write('C1', 'Дата')

    row = 1
    for link in links:
        worksheet.write(row, 0, f'https://t.me/{link.match}')
        worksheet.write(row, 1, link.justification)
        worksheet.write(row, 2, str(link.date)[:10])
        row += 1

    workbook.close()

    print(f"Найдено {len(links)} уникальных совпадений. Результат сохранён в {file_name}")