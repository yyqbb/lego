import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import boto3
from io import StringIO
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import plotly.express as px
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
import os
from dotenv import load_dotenv
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain.chains import LLMChain



documents = loader.load()
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
db = FAISS.from_documents(documents, embeddings)

everything_data = everything_data.rename(columns={"retale_price": "retail_price"})


# Random Forest
X = everything_data[['Theme', 'retail_price', 'Minifigs', 'Pieces']]
y = everything_data['percentage_increase_per_year_real']
X = pd.get_dummies(X, columns=['Theme'], drop_first=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
test_set_numbers = everything_data.loc[X_test.index, 'set_number'].tolist()

# Dash Dashboard
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("LEGO Set Growth Predictor"),
    dcc.Input(id='set-id-input', type='text', placeholder="Enter Set ID", debounce=True),
    html.Button(id='predict-button', n_clicks=0, children='Predict'),
    html.Div(id='prediction-output'),
    dcc.Textarea(id='customer-message-input', placeholder="Enter your message...", style={'width': '100%', 'height': '100px'}),
    html.Button(id='generate-button', n_clicks=0, children='Generate Response'),
    html.Div(id='response-output')
])

# Deal with user input:
@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [State('set-id-input', 'value')]
)
def predict_growth(n_clicks, set_id):
    if n_clicks > 0 and set_id:
        if set_id in test_set_numbers:
            set_data = everything_data[everything_data['set_number'] == set_id]

            if not set_data.empty:
                set_input = set_data[['Theme', 'retail_price', 'Minifigs', 'Pieces']]
                set_input = pd.get_dummies(set_input, columns=['Theme'], drop_first=True)
                set_input = set_input.reindex(columns=X.columns, fill_value=0)
                predicted_growth = rf_model.predict(set_input)
                
                return f"Predicted Yearly Growth: {predicted_growth[0]:.2f}%"
            
            else:
                return "Set ID not found in the dataset."
        else:
            return "Set ID is not valid for predictions."

    return ""


@app.callback(
    Output('response-output', 'children'),
    [Input('generate-button', 'n_clicks')],
    [State('user_input', 'value')]
)
def update_response(n_clicks, message):
    if n_clicks > 0 and message:
        knowledge_base = retrieve_info(message)
        response = chain.run(message=message, best_practice=knowledge_base)
        return response
    return ""

# Knowledge embedding
def retrieve_info(query):
    similar_results = db.similarity_search(query, k=3)
    page_contents_array = [doc.page_content for doc in similar_results]
    return page_contents_array

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini-2024-07-18", openai_api_key=OPENAI_API_KEY)

template = """
You are a world-class business analyst. 
I will user question, and you will give me the best answer that 
I should display in response
You will follow ALL of the rules below:

1/ Response should be concise, 100 words max, but the less the better.

Below is the user input
{message}

Here is the most relevant results
{results}

Please write the best response that should be displayed to the user
"""

prompt = PromptTemplate(
    input_variables=["message", "results"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
