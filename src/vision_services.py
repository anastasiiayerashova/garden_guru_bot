import logging
from dotenv import load_dotenv
import os
import aiohttp


logger = logging.getLogger(__name__)
load_dotenv()

PLANTNET_API_KEY = os.getenv('PLANTNET_API_KEY')
PLANT_URL = f'https://my-api.plantnet.org/v2/identify/all?api-key={PLANTNET_API_KEY}'



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
                    species = best_match['species']['scientificNameWithoutAuthor']
                    common_names = best_match['species'].get('commonNames', [''])
                    confidence = best_match['score']
                    
                    return (f'🌿 **ВИЗНАЧЕННЯ РОСЛИНИ:**\n'
                            f'На зображенні ймовірно **{common_names[0]}** '
                            f'(наукова назва: **{species}**), '
                            f'з точністю **{confidence*100:.2f}%.')
    
    except Exception as e:
        logger.error(f'Помилка при визначенні рослини: {e}', exc_info=True)
        return 'Вибачте, сталася помилка при визначенні рослини.'