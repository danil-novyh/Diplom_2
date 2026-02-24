import allure
from typing import List


class OrderHelpers:
    """Вспомогательные методы для работы с заказами."""
    
    @staticmethod
    @allure.step("Подготовка валидных ингредиентов для заказа")
    def prepare_valid_ingredients(ingredient_ids: List[str], count: int = 3) -> List[str]:
        """
        Возвращает список валидных ID ингредиентов.
        Args:
            ingredient_ids: Полный список ID из API
            count: Количество ингредиентов для заказа (по умолчанию 3)
        Returns:
            List[str]: Список ID ингредиентов
        """
        return ingredient_ids[:count]
    
    @staticmethod
    @allure.step("Подготовка невалидных ингредиентов для заказа")
    def prepare_invalid_ingredients() -> List[str]:
        """
        Возвращает список невалидных ID ингредиентов.
        Returns:
            List[str]: Список заведомо невалидных ID
        """
        return ["invalid_hash_123", "wrong_id_456"]
    
    @staticmethod
    @allure.step("Подготовка пустого списка ингредиентов")
    def prepare_empty_ingredients() -> List[str]:
        """
        Возвращает пустой список ингредиентов.
        Returns:
            List[str]: Пустой список
        """
        return []
    
    @staticmethod
    @allure.step("Подготовка списка с дублирующимися ингредиентами")
    def prepare_duplicate_ingredients(ingredient_ids: List[str], count: int = 3) -> List[str]:
        """
        Возвращает список с повторяющимися ID ингредиентов.
        Args:
            ingredient_ids: Полный список ID из API
            count: Количество повторений
        Returns:
            List[str]: Список с дубликатами
        """
        if not ingredient_ids:
            return []
        return [ingredient_ids[0]] * count
    
    @staticmethod
    @allure.step("Подготовка списка с одним ингредиентом")
    def prepare_single_ingredient(ingredient_ids: List[str]) -> List[str]:
        """
        Возвращает список с одним ингредиентом.
        Args:
            ingredient_ids: Полный список ID из API
        Returns:
            List[str]: Список с одним ID
        """
        if not ingredient_ids:
            return []
        return [ingredient_ids[0]]
    
    @staticmethod
    @allure.step("Подготовка списка с выбранными ингредиентами")
    def prepare_selected_ingredients(ingredient_ids: List[str], indices: List[int]) -> List[str]:
        """
        Возвращает список ингредиентов по указанным индексам.
        Args:
            ingredient_ids: Полный список ID из API
            indices: Список индексов для выбора
        Returns:
            List[str]: Список выбранных ID
        """
        return [ingredient_ids[i] for i in indices if i < len(ingredient_ids)]