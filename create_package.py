import os
import json
import subprocess
import shutil

def create_package(package_name, version, description, maintainer, files, scripts, code_archive, dependencies_script):
    # Создание директории пакета
    package_dir = f"{package_name}-{version}"
    os.makedirs(package_dir, exist_ok=True)
    
    # Создание директории ATPack
    atpack_dir = os.path.join(package_dir, "ATPack")
    os.makedirs(atpack_dir, exist_ok=True)
    
    # Создание файла manifest
    manifest_data = {
        "name": package_name,
        "version": version,
        "description": description,
        "maintainer": maintainer,
        "files": files,
        "scripts": scripts,
        "code_archive": code_archive,
        "dependencies_script": dependencies_script
    }
    with open(os.path.join(atpack_dir, "manifest.json"), "w") as manifest_file:
        json.dump(manifest_data, manifest_file, indent=4)
    
    # Копирование файлов
    for source, destination in files:
        destination_path = os.path.join(package_dir, destination.lstrip('/'))
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy(source, destination_path)
    
    # Копирование архива с кодом
    shutil.copy(code_archive, os.path.join(package_dir, os.path.basename(code_archive)))
    
    # Копирование скрипта для установки зависимостей
    if dependencies_script:
        shutil.copy(dependencies_script, os.path.join(package_dir, os.path.basename(dependencies_script)))
    
    # Упаковка в .ar
    subprocess.run(["ar", "rc", f"{package_name}_{version}.ar", package_dir])

    # Переименование файла в .atpnr
    os.rename(f"{package_name}_{version}.ar", f"{package_name}_{version}.atpnr")

# Пример использования
package_name = input("Введите название пакета: ")
version = input("Введите версию пакета: ")
description = input("Введите описание пакета: ")
maintainer = input("Введите информацию о сопровождающем: ")

files = [
    (input("Введите путь к файлу: "), input("Введите путь установки файла: "))
    for _ in range(int(input("Введите количество файлов: ")))
]

scripts = {}
for script_name in ["preinstall", "postinstall", "preremove", "postremove"]:
    script_path = input(f"Введите путь к скрипту {script_name} (или оставьте пустым): ")
    if script_path:
        with open(script_path) as script_file:
            scripts[script_name] = script_file.read()

code_archive = input("Введите путь к архиву с кодом (.zip): ")
dependencies_script = input("Введите путь к файлу с командами для установки зависимостей (.sh): ")

create_package(package_name, version, description, maintainer, files, scripts, code_archive, dependencies_script)
print("Пакет успешно создан.")
