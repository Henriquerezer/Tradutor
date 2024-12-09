# %%
import openai
from docx import Document
import PyPDF2
from collections import defaultdict

openai.api_key = "YOUR_SECRECT_KEY"

input_pdf_path = "Introdução.pdf"  # Caminho do PDF de entrada
output_doc_path = "teste_artigo_traduzido.docx"  # Caminho do DOCX de saída

cost_per_1k_input_tokens = 0.000150  # Substitua pelo valor da documentação
cost_per_1k_output_tokens = 0.000600  # Substitua pelo valor da documentação
total_cost = 0
total_prompt_tokens = 0
total_completion_tokens = 0
total_cost_input = 0
total_cost_output = 0


# Cria o documento de saída em branco
output_doc = Document()

# Abre o PDF
with open(input_pdf_path, "rb") as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)
    
    for page_number in range(num_pages):
        # Extrai o texto da página atual
        page = reader.pages[page_number]
        extracted_text = page.extract_text()

        # Cria a mensagem para o modelo de chat
        # Instruções: traduzir do português para inglês, manter estilo formal e formatação, citações "(1)"
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a professional translator specialized in scientific texts. Your task is to translate Brazilian Portuguese scientific text into English scientific text, "
                    "strictly preserving the original context, including grammar, punctuation, and formatting. Ensure that citations such as '(1)', paragraph structures, and line breaks remain unchanged."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Translate the following text from Brazilian Portuguese to English. Do not correct any grammar, punctuation, or structure. Maintain the scientific tone and format of the original text:\n\n"
                    f"(Page {page_number+1})\n{extracted_text}"
                )
            }
        ]

        # Chamada à API da OpenAI para tradução da página atual, usando o endpoint de chat
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Ajuste o modelo conforme suas disponibilidades
            messages=messages,
            max_tokens=3000,
            temperature=0.0
        )

        translated_text = response.choices[0].message.content.strip()

        # Verifica se 'usage' está presente na resposta
        if 'usage' in response:
            prompt_tokens = response['usage']['prompt_tokens']
            completion_tokens = response['usage']['completion_tokens']

            cost_input = (prompt_tokens / 1000) * cost_per_1k_input_tokens
            cost_output = (completion_tokens / 1000) * cost_per_1k_output_tokens
            cost_total = cost_input + cost_output

            # Atualiza os acumuladores
            total_prompt_tokens += prompt_tokens
            total_completion_tokens += completion_tokens
            total_cost_input += cost_input
            total_cost_output += cost_output
            total_cost += cost_total
        else:
            print(f"Erro ao processar a página {page_number + 1}: 'usage' não retornado pela API.")


        # Imprime a tradução da página no console
        print(f"--- Tradução da página {page_number+1} ---")
        print(translated_text)
        print("-----------------------------------------")

        # Adiciona a tradução da página ao documento Word de saída
        # Mantemos as quebras de linha
        for paragraph in translated_text.split("\n"):
            output_doc.add_paragraph(paragraph)
        
        # Opcionalmente, adicionar uma quebra de página após cada página traduzida
        # output_doc.add_page_break()

# Salva o documento traduzido final
output_doc.save(output_doc_path)

print(f"Tokens de entrada (input): {total_prompt_tokens}")
print(f"Tokens de saída (output): {total_completion_tokens}")
print(f"Custo total de entrada: ${total_cost_input:.4f}")
print(f"Custo total de saída: ${total_cost_output:.4f}")
print(f"Custo total da API: ${total_cost:.4f}")



print("Tradução completa! Documento salvo em:", output_doc_path)


# %%
