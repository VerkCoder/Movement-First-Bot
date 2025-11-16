import os
import json
import sys
from config import PATH_TO_USERS_FILE, PATH_TO_PROJECTS_FILE, MEDIA_FOLDER_NAME

def check_config():
    """Проверяет наличие и корректность конфигурационного файла"""
    required_config_vars = [
        'API_TELEGRAM',
        'MODERATORS_CHAT_ID', 
        'SCHOOL_AUTH_PSWD',
        'PATH_TO_USERS_FILE',
        'PATH_TO_PROJECTS_FILE',
        'MEDIA_FOLDER_NAME',
        'NON_DISPLAY_CHARACTER',
        'POLLING_TIMEOUT',
        'REWARD_COEFFICIENT_FOR_THE_PHOTO',
        'USER_IN_LEADERBOARD',
        'MEMBERS_IN_MEMBERSLIST',
        'NOT_AUTHORIZED_MESSAGE',
        'NOT_MODERATOR_MESSAGE'
    ]
    
    missing_vars = []
    for var in required_config_vars:
        if not hasattr(sys.modules['config'], var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Ошибка конфигурации: отсутствуют переменные: {', '.join(missing_vars)}")
        return False
    print("✅ Конфигурационный файл проверен успешно")
    return True

def check_data_files():
    """Проверяет наличие и корректность файлов данных"""
    # Проверяем файл пользователей
    if not os.path.exists(PATH_TO_USERS_FILE):
        print(f"📁 Создаю файл пользователей: {PATH_TO_USERS_FILE}")
        try:
            with open(PATH_TO_USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"❌ Ошибка создания файла пользователей: {e}")
            return False
    else:
        # Проверяем что файл валидный JSON
        try:
            with open(PATH_TO_USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Файл пользователей проверен: {len(data)} пользователей")
        except json.JSONDecodeError:
            print(f"❌ Файл пользователей поврежден: {PATH_TO_USERS_FILE}")
            return False
    
    # Проверяем файл проектов
    if not os.path.exists(PATH_TO_PROJECTS_FILE):
        print(f"📁 Создаю файл проектов: {PATH_TO_PROJECTS_FILE}")
        try:
            with open(PATH_TO_PROJECTS_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                            "education": {},
                            "science": {},
                            "profession": {},
                            "culture": {},
                            "volunteering": {},
                            "patriotism": {},
                            "sport": {},
                            "other": {}
                        },
                        f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"❌ Ошибка создания файла проектов: {e}")
            return False
    else:
        # Проверяем что файл валидный JSON
        try:
            with open(PATH_TO_PROJECTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            project_count = sum(len(projects) for projects in data.values())
            print(f"✅ Файл проектов проверен: {project_count} проектов")
        except json.JSONDecodeError:
            print(f"❌ Файл проектов поврежден: {PATH_TO_PROJECTS_FILE}")
            return False
    
    # Проверяем папку для медиа
    if not os.path.exists(MEDIA_FOLDER_NAME):
        print(f"📁 Создаю папку для медиа: {MEDIA_FOLDER_NAME}")
        try:
            os.makedirs(MEDIA_FOLDER_NAME, exist_ok=True)
        except Exception as e:
            print(f"❌ Ошибка создания папки медиа: {e}")
            return False
    else:
        print(f"✅ Папка медиа проверена: {MEDIA_FOLDER_NAME}")
    
    return True

def run_initialization():
    """Запускает все проверки инициализации"""
    print("🔍 Запуск проверки инициализации...")
    print("=" * 50)
    
    success = True
    
    # Проверяем конфигурацию
    if not check_config():
        success = False
    
    # Проверяем файлы данных
    if not check_data_files():
        success = False
    
    print("=" * 50)
    if success:
        print("🎉 Все проверки пройдены успешно! Бот готов к запуску.")
        return True
    else:
        print("❌ Обнаружены ошибки инициализации. Пожалуйста, исправьте их перед запуском бота.")
        return False

if __name__ == "__main__":
    run_initialization()