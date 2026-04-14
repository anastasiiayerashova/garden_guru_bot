import logging
from init import agent


logger = logging.getLogger(__name__)



async def get_agent_response(user_text: str, chat_id: int, session_id: int = 0) -> str:
    config = {'configurable': {'thread_id': f"{str(chat_id)}_{session_id}"}}

    try:
        result_state = await agent.ainvoke({'messages': [('user', user_text)]}, config=config)
        return result_state['messages'][-1].content

    except Exception as e:
        logger.error(f'LangGraph Error: {e}', exc_info=True)
        return 'Вибачте, сталася внутрішня помилка. Спробуйте пізніше.'