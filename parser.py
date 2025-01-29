import requests
from bs4 import BeautifulSoup
import time


base_url = input('Введите URL каталога: ')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

username_entries = []

try:
    n = int(input('Введите количество страниц для обработки: '))
except ValueError:
    print('Некорректное число страниц. Завершение программы.')
    exit()

for page in range(1, n + 1):
    print(f'Обрабатываю страницу {page}...')
    catalog_url = f'{base_url}&page={page}'
    
    try:
        response = requests.get(catalog_url, headers=headers)
        if response.status_code != 200:
            print(f'Ошибка при загрузке страницы {page}: {response.status_code}')
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find('body', class_='flex min-h-screen flex-col justify-between')

        if not body:
            print(f'Не найдено body на странице {page}')
            continue

        rows = body.find_all('tr', class_='bg-white hover:bg-bg-base-secondary')
        channel_links = []

        for row in rows:
            main = row.find('a', class_='channel-name__title truncate cursor-pointer font-semibold text-text-base-primary first-letter:uppercase hover:text-text-accent')
            if main and 'href' in main.attrs:
                channel_links.append(f'https://telemetr.io{main["href"]}')
        
        print(f'Найдено {len(channel_links)} каналов на странице {page}')

        # Обход каналов
        for link in channel_links:
            try:
                channel_response = requests.get(link, headers=headers)
                if channel_response.status_code != 200:
                    print(f'Ошибка при открытии канала {link}: {channel_response.status_code}')
                    continue

                channel_soup = BeautifulSoup(channel_response.content, 'html.parser')
                div_element = channel_soup.find('div', class_='-ml-[60px] mt-2 text-sm sm:ml-0')

                if div_element:
                    p_element = div_element.find('p')
                    if p_element:
                        a_elements = p_element.find_all('a')
                        usernames = [a.get_text(strip=True) for a in a_elements if a.get_text(strip=True).startswith('@')]
                        
                        if usernames:
                            username_entries.append(' '.join(usernames))  # Записываем в одну строку, если несколько username
                            print(f'Канал {link}: Найдены {", ".join(usernames)}')
                        else:
                            print(f'Канал {link}: Юзернеймы не найдены.')
                    else:
                        print(f'Канал {link}: Элемент <p> не найден.')
                else:
                    print(f'Канал {link}: Div с юзернеймами не найден.')

            except requests.RequestException as e:
                print(f'Ошибка при обработке {link}: {e}')
            
            time.sleep(0.1)  # Задержка между запросами

    except requests.RequestException as e:
        print(f'Ошибка при загрузке страницы {page}: {e}')

# Записываем юзернеймы в файл
with open('usernames.txt', 'w', encoding='utf-8') as file:
    for username in username_entries:
        file.write(f'{username}\n')

print('Сбор юзернеймов завершен, файл usernames.txt создан.')

# Удаление строк с "bot"
with open('usernames.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

filtered_lines = [line for line in lines if 'bot' not in line.lower()]

with open('usernames.txt', 'w', encoding='utf-8') as file:
    file.writelines(filtered_lines)

print('Строки с "bot" удалены из usernames.txt.')
