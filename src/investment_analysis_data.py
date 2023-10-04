import pandas as pd
import json
import random
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

user_data_path = os.path.join(current_directory, '../data/user_data.json')
investment_news_path = os.path.join(current_directory, '../data/investment_news.json')
relevant_data_path = os.path.join(current_directory, '../data/relevant_data.csv')

if os.path.exists(user_data_path) and os.path.exists(investment_news_path) and os.path.exists(relevant_data_path):

    with open(user_data_path, 'r') as dados:
        user_data = json.load(dados)

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
        if 'user_data' in globals():
            for dados_usuario in user_data:
                if dados_usuario.get('id') == user_id:
                    
                    news_id = len(dados_usuario.get('news', [])) + 1
                    preferred_investment_type = dados_usuario.get('tipo de investimento preferido')
                    investment_experience = dados_usuario.get('experiência em investimentos')
                    investment_term = dados_usuario.get('prazo de investimento')
                    
                    news_description = generate_news(preferred_investment_type, investment_experience, investment_term)
                    
                    if news_description is not None:
                        news = {'id': news_id, 'description': news_description}
                        
                        if 'news' not in dados_usuario:
                            dados_usuario['news'] = [news]
                        else:
                            dados_usuario['news'].append(news)
                    
                    return dados_usuario
        return None

    users = [user for id in user_ids if (user := get_user(id)) is not None]

    def update_user_json(user_data):
        with open('../data/user_data.json', 'w', encoding='utf-8') as dados:
            json.dump(user_data, dados, ensure_ascii=False, indent=2)

    for user in users:
        update_user_json(user_data)
        if 'nome' in user:
            print(f"User {user['nome']} updated in JSON!")
        else:
            print(f"User ID {user['id']} updated in JSON!")
else:
    print("Um ou mais arquivos não foram encontrados.")