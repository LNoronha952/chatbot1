import customtkinter as ctk
import spacy
import pandas as pd
import requests
import random
from difflib import SequenceMatcher
from io import StringIO

# Carregar o modelo de linguagem do spaCy para português
nlp = spacy.load('pt_core_news_sm')

class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Artemis")
        master.geometry("600x500")

        # Configuração da janela
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        master.grid_rowconfigure(2, weight=0)

        ctk.set_appearance_mode("dark")  # "light" ou "dark"
        ctk.set_default_color_theme("dark-blue")

        # Área de texto
        self.text_area = ctk.CTkTextbox(master, width=500, height=300, wrap="word")
        self.text_area.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_area.insert(ctk.END, "Olá! Eu sou a Artemis, sua assistente virtual. Como posso te ajudar hoje?\n")
        self.text_area.configure(state="disabled")

        # Campo de entrada
        self.entry = ctk.CTkEntry(master, width=400, placeholder_text="Digite sua pergunta aqui...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)

        # Botão de envio
        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="blue", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)

        # Carregar dados da planilha
        self.table_data = self.carregar_dados()

    def carregar_dados(self):
        url = 'LINK_DA_PLANILHA_EM_CSV'  # Substitua pelo link da planilha compartilhada (CSV)
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = pd.read_csv(StringIO(response.text))
            return data
        except Exception as e:
            print(f"Erro ao carregar os dados: {e}")
            return None

    def process_input(self, event=None):
        user_input = self.entry.get()
        if not user_input:
            return

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "Você: " + user_input + "\n")

        response = self.get_bot_response(user_input)
        self.text_area.insert(ctk.END, "Artemis: " + response + "\n")

        self.text_area.configure(state="disabled")

        self.entry.delete(0, ctk.END)

    def get_bot_response(self, user_input):
        # Processar o input com spaCy
        doc = nlp(user_input.lower())
        # Extrair tokens lematizados sem pontuações e palavras de parada
        tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]

        if self.table_data is not None:
            # Tentar encontrar uma correspondência com as colunas
            for column in self.table_data.columns:
                # Lematizar o nome da coluna
                column_lemma = nlp(column.lower())[0].lemma_
                # Verificar se a coluna está nos tokens
                if column_lemma in tokens:
                    column_data = self.table_data[column].dropna().astype(str).tolist()
                    response = f"Os dados da coluna '{column}' são: {', '.join(column_data)}."
                    return response
                else:
                    # Verificar similaridade entre tokens e nome da coluna
                    for token in tokens:
                        similarity = self.similarity(token, column_lemma)
                        if similarity > 0.8:
                            column_data = self.table_data[column].dropna().astype(str).tolist()
                            response = f"Os dados da coluna '{column}' são: {', '.join(column_data)}."
                            return response

        # Randomizar respostas para entradas genéricas
        respostas_genericas = [
            "Desculpe, não entendi. Poderia reformular a pergunta?",
            "Poderia explicar melhor? Estou aqui para ajudar!",
            "Hmm, não tenho certeza se entendi. Pode tentar novamente?",
            "Ainda estou aprendendo, pode tentar perguntar de outra forma?"
        ]

        # Respostas simples baseadas em palavras-chave
        if any(greeting in tokens for greeting in ["olá", "oi"]):
            return random.choice(["Olá! Em que posso ajudar?", "Oi! Como posso te ajudar hoje?", "Olá! Estou aqui para ajudar."])
        elif any(farewell in tokens for farewell in ["tchau", "adeus", "até logo"]):
            return random.choice(["Até mais!", "Tchau! Estou sempre aqui se precisar.", "Adeus! Volte sempre que precisar de ajuda."])
        elif "ajuda" in tokens or "socorro" in tokens:
            return "Claro! Estou aqui para ajudar. O que você precisa?"
        else:
            return random.choice(respostas_genericas)

    def similarity(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

if __name__ == "__main__":
    root = ctk.CTk()
    chatbot = Chatbot(root)
    root.mainloop()
