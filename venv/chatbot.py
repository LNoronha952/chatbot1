import customtkinter as ctk
import pandas as pd
import requests
from io import StringIO  # Importar StringIO da biblioteca io

# Função para carregar dados da planilha do Google
def carregar_dados():
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQsN8z3MryaLYLjbeMZaOv_tjWtXp6dKag422YxoAxFSYUgc6ws3UPJJl_cFCQwKHiVyT7_ioKD0Aao/pub?output=csv'  # Substitua pelo link da sua planilha em formato CSV
    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = pd.read_csv(StringIO(response.text))  # Usar StringIO para ler os dados como CSV
        return dados
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

# Função de resposta do chatbot
def chatbot_response():
    user_input = user_entry.get().lower()
    if user_input:
        chat_box.insert(ctk.END, "Você: " + user_input + "\n")
        
        # Procurar dados na planilha
        if dados is not None:
            resposta = ""
            
            # Exemplo: Responder com informações sobre uma tarefa específica
            if "tarefa" in user_input:
                # Extrai o nome da tarefa mencionado pelo usuário
                partes = user_input.split()
                tarefa_nome = " ".join(partes[partes.index("tarefa")+1:]) if "tarefa" in partes else ""
                
                # Procura a tarefa na planilha
                for _, linha in dados.iterrows():
                    if tarefa_nome.lower() in str(linha["Tarefa"]).lower():
                        prioridade = linha["Prioridade de"]
                        status = linha["Status"]
                        data_inicio = linha["Data de início"]
                        data_termino = linha["Data de término"]
                        resposta = (
                            f"Tarefa: {linha['Tarefa']}\n"
                            f"Prioridade: {prioridade}\n"
                            f"Status: {status}\n"
                            f"Data de Início: {data_inicio}\n"
                            f"Data de Término: {data_termino}\n"
                        )
                        break
                if not resposta:
                    resposta = "Desculpe, não encontrei informações sobre essa tarefa.\n"
            else:
                resposta = "Por favor, pergunte sobre uma tarefa específica. Exemplo: 'Status da tarefa Tarefa1'.\n"
        
        else:
            resposta = "Erro ao acessar os dados. Por favor, tente novamente mais tarde.\n"
        
        chat_box.insert(ctk.END, "Chatbot: " + resposta)
        user_entry.delete(0, ctk.END)

# Carregar os dados da planilha
dados = carregar_dados()

# Configuração da interface com customtkinter
ctk.set_appearance_mode("dark")  # Modo escuro
ctk.set_default_color_theme("blue")  # Tema da cor

root = ctk.CTk()
root.title("Chatbot com Dados da Planilha")
root.geometry("500x600")

# Caixa de exibição do chat
chat_box = ctk.CTkTextbox(root, width=480, height=450)
chat_box.grid(row=0, column=0, padx=10, pady=10)

# Entrada do usuário
user_entry = ctk.CTkEntry(root, width=380, placeholder_text="Digite sua pergunta sobre a tarefa...")
user_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Botão para enviar a mensagem
send_button = ctk.CTkButton(root, text="Enviar", command=chatbot_response)
send_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

# Iniciar a interface
root.mainloop()
