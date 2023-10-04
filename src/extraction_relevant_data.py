import pandas as pd
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

json_file_path = os.path.join(current_directory, '../data/user_database.json')

if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = pd.read_json(json_file, encoding='utf-8')

    key_mapping = {
        "id": "user_id",
        "nome": "name",
        "idade": "age",
        "sexo": "gender",
        "renda mensal": "monthly_income",
        "objetivo financeiro": "financial_goal",
        "tolerância ao risco": "risk_tolerance",
        "prazo de investimento": "investment_term",
        "valor para investimento": "investment_amount",
        "tipo de investimento preferido": "preferred_investment_type",
        "experiência em investimentos": "investment_experience"
    }

    data.rename(columns=key_mapping, inplace=True)

    csv_file_path = os.path.join(current_directory, '../data/relevant_data.csv')

    data.to_csv(csv_file_path, index=False, sep=';', encoding='utf-8-sig')
else:
    print(f"The file '{json_file_path}' was not found.")