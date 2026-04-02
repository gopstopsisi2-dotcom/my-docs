"""
Модуль для работы с файлами.

Предоставляет функции для чтения, записи и получения информации о файлах.
"""

import os
import hashlib
from datetime import datetime
from typing import Union, Optional


def read_file(filepath: str, encoding: str = 'utf-8') -> str:
    """
    Читает содержимое файла и возвращает его в виде строки.

    Args:
        filepath (str): Путь к файлу.
        encoding (str, optional): Кодировка файла. По умолчанию 'utf-8'.

    Returns:
        str: Содержимое файла.

    Raises:
        FileNotFoundError: Если файл не существует.
        PermissionError: Если нет прав на чтение файла.
        UnicodeDecodeError: Если не удалось декодировать файл указанной кодировкой.

    Example:
        >>> content = read_file('config.txt', 'utf-8')
        >>> print(content[:50])
        'server=localhost'
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл {filepath} не найден")
    
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла {filepath}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Не удалось декодировать файл {filepath} с кодировкой {encoding}", e.object, e.start, e.end, e.reason)


def write_file(filepath: str, content: str, encoding: str = 'utf-8') -> int:
    """
    Записывает содержимое в файл.

    Args:
        filepath (str): Путь к файлу.
        content (str): Содержимое для записи.
        encoding (str, optional): Кодировка файла. По умолчанию 'utf-8'.

    Returns:
        int: Количество записанных байт.

    Raises:
        PermissionError: Если нет прав на запись в файл.

    Example:
        >>> bytes_written = write_file('output.txt', 'Hello World')
        >>> print(bytes_written)
        11
    """
    try:
        with open(filepath, 'w', encoding=encoding) as f:
            return f.write(content)
    except PermissionError:
        raise PermissionError(f"Нет прав на запись в файл {filepath}")


def append_to_file(filepath: str, content: str, encoding: str = 'utf-8') -> int:
    """
    Добавляет содержимое в конец файла.

    Args:
        filepath (str): Путь к файлу.
        content (str): Содержимое для добавления.
        encoding (str, optional): Кодировка файла. По умолчанию 'utf-8'.

    Returns:
        int: Количество записанных байт.

    Raises:
        FileNotFoundError: Если файл не существует.
        PermissionError: Если нет прав на запись в файл.

    Example:
        >>> append_to_file('log.txt', 'Новая запись')
        24
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл {filepath} не найден")
    
    try:
        with open(filepath, 'a', encoding=encoding) as f:
            return f.write(content)
    except PermissionError:
        raise PermissionError(f"Нет прав на запись в файл {filepath}")


def get_file_info(filepath: str) -> dict:
    """
    Возвращает информацию о файле.

    Args:
        filepath (str): Путь к файлу.

    Returns:
        dict: Словарь с информацией о файле, содержащий ключи:
            - 'name': имя файла
            - 'size': размер в байтах
            - 'created': дата создания
            - 'modified': дата последнего изменения
            - 'hash_md5': MD5 хеш содержимого

    Raises:
        FileNotFoundError: Если файл не существует.

    Example:
        >>> info = get_file_info('config.txt')
        >>> print(info['name'])
        'config.txt'
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл {filepath} не найден")
    
    stat = os.stat(filepath)
    
    # Вычисляем MD5 хеш содержимого
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    
    return {
        'name': os.path.basename(filepath),
        'size': stat.st_size,
        'created': datetime.fromtimestamp(stat.st_ctime),
        'modified': datetime.fromtimestamp(stat.st_mtime),
        'hash_md5': hash_md5.hexdigest()
    }


def get_file_size(filepath: str) -> int:
    """
    Возвращает размер файла в байтах.

    Args:
        filepath (str): Путь к файлу.

    Returns:
        int: Размер файла в байтах.

    Deprecated:
        Используйте get_file_info() вместо этой функции. Эта функция будет удалена в версии 2.0.0.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл {filepath} не найден")
    return os.path.getsize(filepath)