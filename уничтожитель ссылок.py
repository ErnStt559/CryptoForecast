import os
from bs4 import BeautifulSoup
import re

# Путь к папке с HTML-файлами
folder_path = r"C:\Users\vilny\Desktop\Новая папка (7)"

# Проверяем, является ли URL внешним
def is_external(url: str) -> bool:
    return url is not None and re.match(r'^https?://', url)

# Список атрибутов, которые могут содержать ссылки
url_attrs = ["href", "src", "data-src", "action"]

# Регулярное выражение для поиска внешних ссылок в тексте
url_pattern = re.compile(r'https?://\S+')

# Обработка каждого HTML-файла в папке
for filename in os.listdir(folder_path):
    if filename.lower().endswith('.html'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # Удаляем теги с внешними ссылками в атрибутах
        for tag in soup.find_all(True):
            for attr in url_attrs:
                if attr in tag.attrs and is_external(tag[attr]):
                    tag.decompose()
                    break

        # Удаляем внешние ссылки внутри текста, включая формы []()
        for text_node in soup.find_all(text=True):
            new_text = url_pattern.sub('', text_node)
            new_text = re.sub(r'\[\]\(\)', '', new_text)
            text_node.replace_with(new_text)

        # Удаляем пустые теги
        for tag in soup.find_all():
            if not tag.get_text(strip=True) and not tag.contents:
                tag.decompose()

        # Сохраняем очищенный HTML обратно
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f'Processed {filename}')