import pandas as pd
import json
import random
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

user_database_path = os.path.join(current_directory, '../data/user_database.json')
investment_news_path = os.path.join(current_directory, '../data/investment_news.json')
relevant_data_path = os.path.join(current_directory, '../data/relevant_data.csv')

if os.path.exists(user_database_path) and os.path.exists(investment_news_path) and os.path.exists(relevant_data_path):

    with open(user_database_path, 'r') as dados:
        user_database = json.load(dados)

    with open(investment_news_path, 'r') as arquivo_json:
        investment_news = json.load(arquivo_json)

    df = pd.read_csv(relevant_data_path, sep=';')
    user_ids = df['user_id'].tolist()

    def generate_news(preferred_investment_type, investment_experience, investment_term):
        chave = f"{preferred_investment_type} {investment_experience} {investment_term}"
        investment_news_content = investment_news["investment_news"].get(chave, [])
        
        if investment_news_content:
            return random.choice(investment_news_content)["conteudo"]
        else:
            return None

    def get_user(user_id):
        if 'user_database' in globals():
            for usar_data in user_database:
                if usar_data.get('id') == user_id:
                    
                    news_id = len(usar_data.get('news', [])) + 1
                    preferred_investment_type = usar_data.get('tipo de investimento preferido')
                    investment_experience = usar_data.get('experiência em investimentos')
                    investment_term = usar_data.get('prazo de investimento')
                    
                    news_description = generate_news(preferred_investment_type, investment_experience, investment_term)
                    
                    if news_description is not None:
                        news = {'id': news_id, 'description': news_description}
                        
                        if 'news' not in usar_data:
                            usar_data['news'] = [news]
                        else:
                            usar_data['news'].append(news)
                    
                    return usar_data
        return None

    users = [user for id in user_ids if (user := get_user(id)) is not None]

    def update_user_json(user_database):
        with open('../data/user_database.json', 'w', encoding='utf-8') as dados:
            json.dump(user_database, dados, ensure_ascii=False, indent=2)

    for user in users:
        update_user_json(user_database)
        if 'nome' in user:
            print(f"User {user['nome']} updated in JSON!")
        else:
            print(f"User ID {user['id']} updated in JSON!")
else:
    print("One or more files was not found.")