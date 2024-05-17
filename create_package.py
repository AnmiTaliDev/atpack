import os
import json
import subprocess
import shutil
import zipfile

def create_package(package_name, version, description, maintainer, files, scripts, code_archive, dependencies_script, is_console_app):
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
        "is_console_app": is_console_app
    }
    with open(os.path.join(atpack_dir, "manifest.json"), "w") as manifest_file:
        json.dump(manifest_data, manifest_file, indent=4)
    
    # Копирование файлов
    for source, destination in files:
        destination_path = os.path.join(package_dir, destination.lstrip('/'))
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy(source, destination_path)
    
    # Распаковка архива с кодом
    with zipfile.ZipFile(code_archive, 'r') as zip_ref:
        zip_ref.extractall(package_dir)

    # Создание файла .desktop для графических приложений
    if not is_console_app:
        desktop_entry = f"""[Desktop Entry]
Type=Application
Name={package_name}
Comment={description}
Exec=/usr/bin/{package_name}
Icon=
Terminal=false
"""
        desktop_file_path = os.path.join(atpack_dir, f"{package_name}.desktop")
        with open(desktop_file_path, "w") as desktop_file:
            desktop_file.write(desktop_entry)
    
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

is_console_app = input("Является ли приложение консольным? (yes/no): ").strip().lower() == 'yes'

create_package(package_name, version, description, maintainer, files, scripts, code_archive, dependencies_script, is_console_app)
print("Пакет успешно создан.")
