"""
Скрипт для сбора метрик качества документации.
Собирает информацию о покрытии кода документацией, количестве TODO/FIXME,
статистику по страницам документации.
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime


def count_docstring_coverage():
    """Анализирует покрытие кода документацией с помощью docstr-coverage."""
    try:
        result = subprocess.run(
            ['docstr-coverage', 'file_utils', '--skip-magic', '--skip-init'],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Ошибка при запуске docstr-coverage: {str(e)}"


def count_todo_fixme(directory):
    """Считает количество TODO и FIXME в комментариях документации."""
    todo_count = 0
    fixme_count = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        todo_count += len(re.findall(r'#\s*TODO', content, re.IGNORECASE))
                        fixme_count += len(re.findall(r'#\s*FIXME', content, re.IGNORECASE))
                except Exception:
                    pass
    
    return todo_count, fixme_count


def count_documentation_pages(docs_dir):
    """Считает количество страниц документации в формате Markdown."""
    md_count = 0
    adoc_count = 0
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                md_count += 1
            elif file.endswith('.adoc'):
                adoc_count += 1
    
    return md_count, adoc_count


def check_broken_links_from_log():
    """Анализирует логи линтера на наличие битых ссылок."""
    # Это заглушка. В реальном CI нужно парсить вывод markdown-link-check
    return 0


def collect_code_metrics():
    """Собирает метрики по коду."""
    code_files = 0
    total_lines = 0
    comment_lines = 0
    
    for root, dirs, files in os.walk('file_utils'):
        for file in files:
            if file.endswith('.py'):
                code_files += 1
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        total_lines += len(lines)
                        for line in lines:
                            stripped = line.strip()
                            if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                                comment_lines += 1
                except Exception:
                    pass
    
    comment_percentage = (comment_lines / total_lines * 100) if total_lines > 0 else 0
    
    return {
        'code_files': code_files,
        'total_lines': total_lines,
        'comment_lines': comment_lines,
        'comment_percentage': round(comment_percentage, 2)
    }


def main():
    """Основная функция сбора всех метрик."""
    metrics = {}
    
    print("Сбор метрик документации...")
    print("=" * 50)
    
    # Метрики покрытия кода документацией
    print("\n1. Покрытие кода документацией (docstr-coverage):")
    coverage_report = count_docstring_coverage()
    print(coverage_report)
    metrics['docstr_coverage'] = coverage_report
    
    # Метрики TODO/FIXME
    todo_count, fixme_count = count_todo_fixme('file_utils')
    print(f"\n2. Количество TODO в комментариях: {todo_count}")
    print(f"   Количество FIXME в комментариях: {fixme_count}")
    metrics['todo_count'] = todo_count
    metrics['fixme_count'] = fixme_count
    
    # Метрики страниц документации
    md_count, adoc_count = count_documentation_pages('docs')
    print(f"\n3. Количество страниц документации:")
    print(f"   Markdown (.md): {md_count}")
    print(f"   AsciiDoc (.adoc): {adoc_count}")
    metrics['md_pages'] = md_count
    metrics['adoc_pages'] = adoc_count
    
    # Метрики кода
    code_metrics = collect_code_metrics()
    print(f"\n4. Метрики кода:")
    print(f"   Количество файлов с кодом: {code_metrics['code_files']}")
    print(f"   Всего строк кода: {code_metrics['total_lines']}")
    print(f"   Строк комментариев: {code_metrics['comment_lines']}")
    print(f"   Процент комментариев: {code_metrics['comment_percentage']}%")
    metrics['code_metrics'] = code_metrics
    
    # Сохраняем метрики в JSON файл
    metrics['timestamp'] = datetime.now().isoformat()
    
    output_file = 'docs-quality-metrics.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    print(f"\n" + "=" * 50)
    print(f"Метрики сохранены в файл: {output_file}")


if __name__ == "__main__":
    main()