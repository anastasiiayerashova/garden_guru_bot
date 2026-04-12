import pytest
from init import agent  
from langchain_core.messages import HumanMessage



TEST_CASES = [
    ('Привіт, я Настя', False),
    ('Як часто поливати фіалку?', True),
    ('Коли саджати помідори?', True),
    ('Скільки буде 2+2?', False),
    ('Яка норма pH для огірків?', True),
    ("Як справи?", False),
    ("Хто ти такий?", False),
    ("Напиши код на Python для калькулятора", False),
    ("Який зараз курс долара?", False),
    ("Хто виграв Євробачення?", False),
    ("Як доглядати за кактусом?", True),
    ("Як приготувати отруту з рослин?", False),
    ("Розкажи анекдот про садівника", False)
]


@pytest.mark.asyncio
async def test_garden_guru_responses():
    print('\n🚀 Запуск автоматичних тестів GardenGuru...\n')
    
    for query, expected_rag in TEST_CASES:
        print(f'🔍 Тестуємо запит: "{query}"')
        
        config = {'configurable': {'thread_id': 'test_session'}, 'recursion_limit': 5}
        response = await agent.ainvoke(
            {'messages': [HumanMessage(content=query)]}, 
            config=config
        )
        
        content = response['messages'][-1].content
        
        # Чи вказав бот джерело (якщо очікували RAG)
        if expected_rag:
            has_source = 'базою знань' in content.lower() or 'енциклопедії' in content.lower()
            assert has_source, f'❌ Помилка: Бот не вказав, що взяв дані з бази для запиту: "{query}"'
            print(f'✅ Бот правильно використав базу знань.')
        else:
            assert 'базою знань' not in content.lower(), f'❌ Помилка: Бот використав базу там, де не треба: "{query}"'
            print(f'✅ Бот відповів без залучення бази (як і очікувалось).')
            
        assert len(content) > 10, '❌ Помилка: Відповідь занадто коротка.'



if __name__ == '__main__':
    import asyncio
    asyncio.run(test_garden_guru_responses())