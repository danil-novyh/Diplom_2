import allure
from data.response_codes import StatusCode
from data.messages import ErrorMessages
from helpers.order_helpers import OrderHelpers


@allure.epic("Order Management")
@allure.feature("Order Creation")
class TestOrderCreation:
    """Тесты создания заказа."""
    
    @allure.title("Создание заказа с авторизацией")
    @allure.description("Проверка, что авторизованный пользователь может создать заказ")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_auth_success(
        self, api_client, created_user_with_login, ingredient_ids
    ):
        """Тест создания заказа авторизованным пользователем."""
        
        _, access_token = created_user_with_login

        valid_ingredients = OrderHelpers.prepare_valid_ingredients(ingredient_ids)
        
        with allure.step("Отправка POST запроса на создание заказа с токеном авторизации"):
            response = api_client.create_order(valid_ingredients, access_token)
        
        with allure.step("Проверка кода ответа 200"):
            assert response.status_code == StatusCode.OK
        
        with allure.step("Проверка, что success = true"):
            assert response.json()["success"] is True
        
        with allure.step("Проверка наличия номера заказа"):
            assert "order" in response.json()
            assert "number" in response.json()["order"]
    
    @allure.title("Создание заказа без авторизации")
    @allure.description("Проверка, что неавторизованный пользователь может создать заказ")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_without_auth_success(self, api_client, ingredient_ids):
        """Тест создания заказа без авторизации."""
        
        valid_ingredients = OrderHelpers.prepare_valid_ingredients(ingredient_ids)

        with allure.step("Отправка POST запроса на создание заказа без токена"):
            response = api_client.create_order(valid_ingredients)
        
        with allure.step("Проверка кода ответа 200"):
            assert response.status_code == StatusCode.OK
        
        with allure.step("Проверка, что success = true"):
            assert response.json()["success"] is True
        
        with allure.step("Проверка наличия номера заказа"):
            assert "order" in response.json()
    
    @allure.title("Создание заказа с валидными ингредиентами")
    @allure.description("Проверка, что заказ создается с корректным списком ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_valid_ingredients_success(
        self, api_client, created_user_with_login, ingredient_ids
    ):
        """Тест создания заказа с валидными ингредиентами."""
        
        _, access_token = created_user_with_login
        
        selected_ingredients = OrderHelpers.prepare_selected_ingredients(
            ingredient_ids, [0, 2, 4]
        )
        
        with allure.step("Отправка POST запроса на создание заказа"):
            response = api_client.create_order(selected_ingredients, access_token)
        
        with allure.step("Проверка кода ответа 200"):
            assert response.status_code == StatusCode.OK
        
        with allure.step("Проверка, что success = true"):
            assert response.json()["success"] is True
        
        with allure.step("Проверка наличия номера заказа"):
            assert "order" in response.json()
            assert "number" in response.json()["order"]
            assert isinstance(response.json()["order"]["number"], int)
            assert response.json()["order"]["number"] > 0
    
    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Проверка, что нельзя создать заказ с пустым списком ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_without_ingredients_fails(
        self, api_client, created_user_with_login
    ):
        """Тест создания заказа без ингредиентов."""
        
        _, access_token = created_user_with_login
        
        empty_ingredients = OrderHelpers.prepare_empty_ingredients()
        
        with allure.step("Отправка POST запроса на создание заказа без ингредиентов"):
            response = api_client.create_order(empty_ingredients, access_token)
        
        with allure.step("Проверка кода ответа 400 Bad Request"):
            assert response.status_code == StatusCode.BAD_REQUEST
        
        with allure.step("Проверка, что success = false"):
            assert response.json()["success"] is False
        
        with allure.step(f"Проверка сообщения об ошибке: '{ErrorMessages.NO_INGREDIENTS}'"):
            assert response.json()["message"] == ErrorMessages.NO_INGREDIENTS
    
    @allure.title("Создание заказа с невалидным хешем ингредиентов")
    @allure.description("Проверка обработки заказа с несуществующими ID ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_with_invalid_ingredient_hash_fails(
        self, api_client, created_user_with_login
    ):
        """Тест создания заказа с невалидными ID ингредиентов."""
        
        _, access_token = created_user_with_login
        
        invalid_ingredients = OrderHelpers.prepare_invalid_ingredients()

        with allure.step("Отправка POST запроса с невалидными ID ингредиентов"):
            response = api_client.create_order(invalid_ingredients, access_token)
        
        with allure.step("Проверка кода ответа 500 Internal Server Error"):
            assert response.status_code == StatusCode.INTERNAL_SERVER_ERROR
    
    @allure.title("Создание заказа с одним ингредиентом")
    @allure.description("Проверка создания минимального заказа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_with_single_ingredient_success(
        self, api_client, created_user_with_login, ingredient_ids
    ):
        """Тест создания заказа с одним ингредиентом."""
        
        _, access_token = created_user_with_login
        
        single_ingredient = OrderHelpers.prepare_single_ingredient(ingredient_ids)
        
        with allure.step("Отправка POST запроса на создание заказа"):
            response = api_client.create_order(single_ingredient, access_token)
        
        with allure.step("Проверка кода ответа 200"):
            assert response.status_code == StatusCode.OK
        
        with allure.step("Проверка, что success = true"):
            assert response.json()["success"] is True
    
    @allure.title("Создание заказа с дублирующимися ингредиентами")
    @allure.description("Проверка, что можно добавлять один ингредиент несколько раз")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_with_duplicate_ingredients_success(
        self, api_client, created_user_with_login, ingredient_ids
    ):
        """Тест создания заказа с повторяющимися ингредиентами."""
        
        _, access_token = created_user_with_login
        
        duplicate_ingredients = OrderHelpers.prepare_duplicate_ingredients(ingredient_ids)
        
        with allure.step("Отправка POST запроса на создание заказа"):
            response = api_client.create_order(duplicate_ingredients, access_token)
        
        with allure.step("Проверка кода ответа 200"):
            assert response.status_code == StatusCode.OK
        
        with allure.step("Проверка, что success = true"):
            assert response.json()["success"] is True
