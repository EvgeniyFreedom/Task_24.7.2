import requests
import json

class PetFriends:
    """Библиотека для работы с API PetFriends (https://petfriends.skillfactory.ru/)."""

    def __init__(self):
        """Инициализация базового URL API."""
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):
        """Получение API ключа для авторизации"""

        headers = {
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url+"api/key", headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        """Получение списка питомцев"""

        headers = {"auth_key": auth_key["key"]}
        filter = {"filter": filter}
        res = requests.get(self.base_url+"api/pets", headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key, pet_photo, name, animal_type, age):
        """Добавление нового питомца с фотографией"""

        data = {
            "name": name,
            "animal_type": animal_type,
            "age": age,
        }
        headers = {"auth_key": auth_key["key"]}
        file = {"pet_photo": (pet_photo, open(pet_photo, "rb"), "images/jpg")}
        res = requests.post(self.base_url + "api/pets", headers=headers, data=data, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Удаление питомца по ID."""

        headers = {"auth_key": auth_key["key"]}
        res = requests.delete(self.base_url + "api/pets/" + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Обновление информации о питомце."""

        headers = {"auth_key": auth_key["key"]}
        data = {
            "name": name,
            "age": age,
            "animal_type": animal_type
        }
        res = requests.put(self.base_url + "api/pets/" + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def create_pet_simpl(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        """Создание питомца без фотографии"""

        headers = {"auth_key": auth_key["key"]}
        data = {
            "name": name,
            "animal_type": animal_type,
            "age": age
        }
        res = requests.post(self.base_url + "api/create_pet_simple", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Добавление фотографии к существующему питомцу."""

        headers = {"auth_key": auth_key["key"]}
        file = {"pet_photo": (pet_photo, open(pet_photo, "rb"), "image/jpg")}
        res = requests.post(self.base_url + "api/pets/set_photo/" + pet_id, headers=headers, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result