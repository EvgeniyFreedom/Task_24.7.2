from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос API ключа возвращает статус 200 и в результате содержится ключ 'key'"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

def test_get_all_pets_with_valid_key(filter=""):
    """Проверяем, что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем API ключ и сохраняем в переменную auth_key. Далее используя этот ключ
        запрашиваем список всех питомцев и проверяем что список не пустой."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0

def test_add_new_pets_with_valid_key(name="Киса", animal_type="кошка", age="1", pet_photo="images/Kisa.jpg"):
    """Проверяем, что можно добавить питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, pet_photo, name, animal_type, age)
    assert status == 200
    assert len(result) > 0

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name="Мишка", animal_type="Кот", age="1"):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)
        assert status == 200
        assert result["name"] == name
    else:
        raise Exception("There is no my pets")

# Тест 1: Успешное создание питомца без фото
def test_create_pet_simpl_success():
    """Проверяем успешное создание питомца без фотографии"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name = "Мишка"
    animal_type = "Кот"
    age = "1"
    status, result = pf.create_pet_simpl(auth_key, name, animal_type, age)
    assert status == 200
    assert "name" in result and result["name"] == name
    assert "animal_type" in result and result["animal_type"] == animal_type
    assert "age" in result and result["age"] == age

# Тест 2: Успешное добавление фото к питомцу
def test_successful_add_photo_of_pet(pet_photo = "images/Mishka.jpg"):
    """Проверяем успешное добавление фотографии к питомцу"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Создаем питомца если нет
    _, my_pets = pf.get_list_of_pets(auth_key,"my_pets")
    pet_id = my_pets["pets"][0]["id"]
    status, result = pf.add_photo_of_pet(auth_key,pet_id,pet_photo)
    assert status == 200
    assert result["pet_photo"] != ""

# Тест 3: Создание питомца без авторизации
def test_create_pet_no_auth_key():
    """Проверяем, что нельзя создать питомца без авторизации"""
    auth_key = {"key": ""}
    name = "Мишка"
    animal_type = "Кот"
    age = "2"
    status, result = pf.create_pet_simpl(auth_key, name, animal_type, age)
    assert status == 403

# Тест 4: Создание питомца с неверным типом возраста
def test_create_pet_invalid_age_type():
    """Проверяем обработку неверного типа возраста"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name = "Мишка"
    animal_type = "Кот"
    age = "два"  # неправильный тип
    status, result = pf.create_pet_simpl(auth_key, name, animal_type, age)
    assert status == 400

# Тест 5: Создание питомца с пустым именем
def test_create_pet_empty_name():
    """Проверяем обработку пустого имени"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name = ""
    animal_type = "Кот"
    age = "1"
    status, result = pf.create_pet_simpl(auth_key, name, animal_type, age)
    assert status == 400

# Тест 6: Создание питомца с неверным ключом авторизации
def test_create_pet_invalid_auth_key():
    """Проверяем обработку неверного ключа авторизации"""
    auth_key = {"key": "invalid_key"}
    name = "Кот"
    animal_type = "Мишка"
    age = "5"
    status, result = pf.create_pet_simpl(auth_key, name, animal_type, age)
    assert status == 403

# Тест 7: Загрузка файла не изображения
def test_upload_non_image_file():
    """Проверяем обработку загрузки файла не изображения"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets["pets"]
    non_image_file = "files/document.txt"  # текстовый файл
    status, result = pf.pets_set_photo(auth_key, pet_id, non_image_file)
    assert status == 400

# Тест 8: Создание питомца без указания типа животного
def test_create_pet_no_animal_type():
    """Проверяем обработку отсутствия типа животного"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name = "Кот"
    # пропущено animal_type
    age = "2"
    status, result = pf.create_pet_simpl(auth_key, name, None, age)
    assert status == 400

# Тест 9: Создание питомца с None именем
def test_create_pet_name_none():
    """Проверяем обработку None в качестве имени"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name = None
    animal_type = "Кот"
    age = "1"
    status, result = pf.create_pet_simpl(auth_key, name, animal_type, age)
    assert status == 400

# Тест 10: Добавление фото к несуществующему питомцу
def test_add_photo_to_nonexistent_pet():
    """Проверяем обработку попытки добавить фото к несуществующему питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), "images/Mishka.jpg")
    invalid_pet_id = "00000000-0000-0000-0000-000000000000"  # несуществующий ID
    status, result = pf.add_photo_of_pet(auth_key, invalid_pet_id, pet_photo)
    assert status == 400