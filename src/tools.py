from db import PLANTS_DB, PLANTING_CALENDAR, PESTS_DB
from schemas import PlantCareInput, PlantingCalendarInput, PestIdentifierInput, FertilizerCalculatorInput

from langchain_core.tools import tool
from datetime import datetime


@tool(args_schema=PlantCareInput)
def plant_care(plant_name: str) -> str:
    '''
    Надає повну інформацію про догляд за конкретною рослиною: полив, 
    освітлення, температура, ґрунт та типові проблеми.
    '''

    plant_lower = plant_name.lower().strip()
    plant_data = PLANTS_DB.get(plant_lower)

    if not plant_data:
        for key in PLANTS_DB:
            if plant_lower in key or key in plant_lower:
                plant_data = PLANTS_DB[key]
                plant_lower = key
                break
    if not plant_data:
        return f'На жаль, інформацію про "{plant_name}" не знайдено в базі. Спробуйте іншу назву.'
    
    result = [f'🌱 **ДОГЛЯД ЗА РОСЛИНОЮ: {plant_lower.upper()}**\n']
    result.append(f'**Тип:** {plant_data.get('тип', 'не вказано')}')
    result.append(f'💧 **Полив:** {plant_data['полив']}')
    result.append(f'☀️ **Освітлення:** {plant_data['освітлення']}')
    result.append(f'🌡️ **Температура:** {plant_data['температура']}')
    result.append(f'🪴 **Ґрунт:** {plant_data['ґрунт']}\n')

    if 'проблеми' in plant_data:
        result.append('⚠️ **ТИПОВІ ПРОБЛЕМИ:**')
        for problem, solution in plant_data['problems'].items() if 'problems' in plant_data else plant_data.get('проблеми', {}).items():
            result.append(f' • *{problem}*: {solution}')
        result.append('')

    if 'поради' in plant_data:
        result.append('💡 **ПОРАДИ:**')
        for tip in plant_data['поради']:
            result.append(f' • {tip}')

    return '\n'.join(result)


@tool(args_schema=PlantingCalendarInput)
def planting_calendar(month: int = 0) -> str:
    '''
    Показує календар посадки овочів та квітів. 
    Параметр month: номер місяця (1-12). Якщо 0 — використовується поточний місяць.
    '''

    if month == 0:
        month = datetime.now().month
    
    if month not in PLANTING_CALENDAR:
        return f'Календар для місяця №{month} ще не заповнений. Зазвичай активні роботи тривають з березня по червень.'

    month_names = {
        1: 'Січень', 2: 'Лютий', 3: 'Березень', 4: 'Квітень',
        5: 'Травень', 6: 'Червень', 7: 'Липень', 8: 'Серпень',
        9: 'Вересень', 10: 'Жовтень', 11: 'Листопад', 12: 'Грудень'
    }
    
    data = PLANTING_CALENDAR[month]
    result = [f'📅 **КАЛЕНДАР ПОСАДКИ: {month_names[month].upper()}**\n']
    
    if data.get('на розсаду'):
        result.append(f'🏠 **СІЯТИ НА РОЗСАДУ:** {', '.join(data['на розсаду'])}')
    
    if data.get('у ґрунт'):
        result.append(f'🌍 **СІЯТИ У ВІДКРИТИЙ ҐРУНТ:** {', '.join(data['у ґрунт'])}')
    
    if data.get('висаджувати розсаду'):
        result.append(f'🌱 **ВИСАДЖУВАТИ РОЗСАДУ:** {', '.join(data['висаджувати розсаду'])}')
    
    result.append(f'\n💡 **ПОРАДИ:** {data['поради']}')
    
    return '\n'.join(result)


@tool(args_schema=PestIdentifierInput)
def pest_identifier(symptoms: str) -> str:
    '''
    Визначає шкідника або хворобу за описом симптомів (наприклад: жовті плями, дрібні комахи).
    Надає рекомендації щодо лікування та профілактики.
    '''

    symptoms_lower = symptoms.lower()
    best_match = None
    max_score = 0

    for key, data in PESTS_DB.items():
        key_words = key.lower().split()
        score = sum(1 for kw in key_words if kw in symptoms_lower)
        if score > max_score:
            max_score = score
            best_match = data

    if not best_match or max_score == 0:
        return f'Не вдалося точно визначити проблему за описом: "{symptoms}". Спробуйте описати колір плям або вид комах детальніше.'

    result = [f'🔍 **ДІАГНОЗ: {best_match['діагноз']}**\n']
    result.append(f'🌿 **Уражені культури:** {', '.join(best_match['культури'])}')
    result.append(f'❓ **Причини:** {best_match['причини']}\n')
    
    result.append('💊 **ЛІКУВАННЯ:**')
    for step in best_match['лікування']:
        result.append(f' • {step}')
        
    result.append('\n🛡️ **ПРОФІЛАКТИКА:**')
    for tip in best_match['профілактика']:
        result.append(f' • {tip}')
        
    return '\n'.join(result)


@tool(args_schema=FertilizerCalculatorInput)
def fertilizer_calculator(area_m2: float, plant_type: str = 'загальний') -> str:
    '''
    Розраховує необхідну кількість комплексного добрива (в грамах) для ділянки заданої площі.
    Параметри: area_m2 (площа в кв. метрах), plant_type (тип рослин: овочі, квіти, газон).
    '''

    # Норми в грамах на 1 м2
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

tools_list = [plant_care, planting_calendar, pest_identifier, fertilizer_calculator]