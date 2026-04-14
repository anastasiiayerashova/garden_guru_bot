import logging
import time
from init import agent


logger = logging.getLogger(__name__)



async def get_agent_response(user_text: str, chat_id: int, session_id: int = 0) -> str:
    thread_id = f'{str(chat_id)}_{session_id}'
    config = {'configurable': {'thread_id': thread_id}}
    
    logger.info(f'💬 Отримано запит від користувача: "{user_text}" (Chat ID: {chat_id}, Thread ID: {thread_id})')

    start_time = time.perf_counter()
    
    try:
        result_state = await agent.ainvoke({'messages': [('user', user_text)]}, config=config)
        response_content = result_state['messages'][-1].content

        end_time = time.perf_counter()
        duration = end_time - start_time

        logger.info(f'✅ [Agent Response] Успішно за {duration:.2f}с')
        return response_content

    except Exception as e:
        logger.error(f'LangGraph Error: {e}', exc_info=True)
        return 'Вибачте, сталася внутрішня помилка. Спробуйте пізніше.'