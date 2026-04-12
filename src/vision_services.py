import logging
from dotenv import load_dotenv
import os
import aiohttp


logger = logging.getLogger(__name__)
load_dotenv()

PLANTNET_API_KEY = os.getenv('PLANTNET_API_KEY')
PLANT_URL = f'https://my-api.plantnet.org/v2/identify/all?api-key={PLANTNET_API_KEY}'
PLANT_URL_DISEASES = f'https://my-api.plantnet.org/v2/diseases/identify?api-key={PLANTNET_API_KEY}'



async def identify_plant(image_path: str) -> str:
    '''
    Визначає рослину за зображенням, використовуючи API PlantNet.
    Параметр: image_path (шлях до зображення рослини).
    '''

    try:
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()

            with open(image_path, 'rb') as f:
                data.add_field('images', f)

                async with session.post(PLANT_URL, data=data) as response:

                    if response.status != 200:
                        logger.error(f'Помилка при зверненні до PlantNet API: {response.status}')
                        return 'Вибачте, не вдалося визначити рослину. Спробуйте ще раз пізніше.'
                    
                    result = await response.json()

                    if not result.get('results'):
                        return 'Рослину не вдалося визначити. Спробуйте інше зображення.'
                    
                    best_match = result['results'][0]
                    species_data = best_match.get('species', {})
                    scientific_name = species_data.get('scientificNameWithoutAuthor', 'Unknown')
                    common_names = species_data.get('commonNames', [])
                    common_name = common_names[0] if common_names else 'назва невідома'
                    family = species_data.get('family', {}).get('scientificNameWithoutAuthor', 'Unknown family')
                    confidence = best_match.get('score', 0)
                    
                    return (f'🌿 **ВИЗНАЧЕННЯ РОСЛИНИ:**\n'
                            f'На зображенні ймовірно *{common_name}* '
                            f'👪 Родина: *{family}*\n'
                            f'🧬 Наукова назва: *{scientific_name}*\n'
                            f'📊 Точність визначення: *{confidence*100:.2f}%*.')
    
    except Exception as e:
        logger.error(f'Помилка при визначенні рослини: {e}', exc_info=True)
        return 'Вибачте, сталася помилка при визначенні рослини.'
    


async def identify_disease(image_path: str) -> str:
    '''
    Визначає хворобу рослини за зображенням, використовуючи API PlantNet.
    Параметр: image_path (шлях до зображення симптомів хвороби).
    '''

    try:
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()

            with open(image_path, 'rb') as f:
                data.add_field('images', f)

                async with session.post(PLANT_URL_DISEASES, data=data) as response:

                    if response.status != 200:
                        logger.error(f'Помилка при зверненні до PlantNet API для хвороб: {response.status}')
                        return 'Вибачте, не вдалося визначити хворобу. Спробуйте ще раз пізніше.'
                    
                    result = await response.json()

                    if not result.get('results'):
                        return 'Хворобу не вдалося визначити. Спробуйте інше зображення.'
                    
                    best_match = result['results'][0]
                    disease_name = best_match.get('name', 'невідома хвороба')
                    confidence = best_match.get('score', 0)
                    
                    return (f'⚠️ **ВИЗНАЧЕННЯ ХВОРОБИ:**\n'
                            f'На зображенні ймовірно *{disease_name}*, '
                            f'з точністю *{confidence*100:.2f}%*.')
    
    except Exception as e:
        logger.error(f'Помилка при визначенні хвороби: {e}', exc_info=True)
        return 'Вибачте, сталася помилка при визначенні хвороби.'