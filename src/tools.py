from schemas import FertilizerCalculatorInput
from schemas import SemanticSearchInput

import os
from langchain_core.tools import tool
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()
VECTOR_STORE_ID = os.getenv('VECTOR_STORE_ID')


@tool(args_schema=SemanticSearchInput)
def semantic_search(query: str) -> str:
    '''
    Шукає розширену інформацію про рослини, шкідників, хвороби та календар посадки в базі знань.
    Використовуйте цей інструмент, коли користувач ставить загальні питання про догляд, 
    опис симптомів хвороб або шукає поради щодо садівництва, яких немає в інших інструментах.
    '''
    
    results = client.vector_stores.search(
        vector_store_id=VECTOR_STORE_ID,
        query=query
    )

    if not results.data:
        return 'У базі знань не знайдено інформації за цим запитом.'
    
    content = results.data[0].content
    return f'Ось що знайдено в енциклопедії:\n{content}'


@tool(args_schema=FertilizerCalculatorInput)
def fertilizer_calculator(area_m2: float, plant_type: str = 'загальний') -> str:
    '''
    Розраховує необхідну кількість комплексного добрива (в грамах) для ділянки заданої площі.
    Параметри: area_m2 (площа в кв. метрах), plant_type (тип рослин: овочі, квіти, газон).
    '''

    rates = {
        'овочі': 40,
        'квіти': 30,
        'газон': 50,
        'загальний': 35
    }
    
    rate = rates.get(plant_type.lower(), rates['загальний'])
    total_amount = area_m2 * rate
    
    return (f'📊 **РОЗРАХУНОК ДОБРИВ:**\n'
            f'Для ділянки площею **{area_m2} м²** під **{plant_type}** '
            f'вам знадобиться приблизно **{total_amount} г** комплексного добрива.\n'
            f'*Рекомендація: рівномірно розподіліть добриво перед поливом або дощем.*')

tools_list = [semantic_search, fertilizer_calculator]