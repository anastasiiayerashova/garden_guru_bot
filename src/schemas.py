from pydantic import BaseModel, Field


class SemanticSearchInput(BaseModel):
    query: str = Field(description='Пошуковий запит для енциклопедії садівництва (наприклад, "як лікувати плями на листі")')


class PlantCareInput(BaseModel):
    plant_name: str = Field(description='Назва рослини (наприклад, "Томат", "Фіалка")')


class PlantingCalendarInput(BaseModel):
    month: int = Field(
        default=0, 
        ge=0, le=12, 
        description='Номер місяця від 1 до 12. 0 означає поточний місяць.'
    )


class PestIdentifierInput(BaseModel):
    symptoms: str = Field(description='Опис симптомів (наприклад, "жовті плями", "білий наліт")')


class FertilizerCalculatorInput(BaseModel):
    area_m2: float = Field(gt=0, description='Площа ділянки в квадратних метрах')
    plant_type: str = Field(default='загальний', description='Тип культури: овочі, квіти, газон або загальний')