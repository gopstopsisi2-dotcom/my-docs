"""
Скрипт для извлечения текстовых строк из Markdown файлов.
Игнорирует блоки кода и изображения.
"""

import os
import re
import json
from pathlib import Path


def extract_text_from_md(filepath):
    """Извлекает текстовые строки из Markdown файла, игнорируя код."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Удаляем блоки кода
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Удаляем инлайн код
    content = re.sub(r'`[^`]+`', '', content)
    # Удаляем изображения
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    # Удаляем ссылки (оставляем текст)
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
    
    # Разбиваем на строки и фильтруем пустые
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    return lines


def scan_docs_directory(docs_path):
    """Сканирует папку docs и собирает все текстовые строки."""
    all_strings = []
    
    for root, dirs, files in os.walk(docs_path):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                strings = extract_text_from_md(filepath)
                for s in strings:
                    if len(s) > 10:  # Игнорируем короткие строки
                        all_strings.append({
                            'file': filepath,
                            'text': s
                        })
    
    return all_strings


def main():
    """Основная функция."""
    # Сканируем русскую версию как базовую
    strings = scan_docs_directory('docs/ru')
    
    # Сохраняем в JSON для перевода
    output = {
        'source_language': 'ru',
        'strings': strings
    }
    
    with open('i18n_strings.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Извлечено {len(strings)} строк для перевода")
    print(f"Файл сохранен: i18n_strings.json")


if __name__ == "__main__":
    main()