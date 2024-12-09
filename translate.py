# %%

# %%
import openai
from docx import Document
import PyPDF2

openai.api_key = "YOUR_SECRECT_KEY"

input_pdf_path = "Introdução.pdf"  # Caminho do PDF de entrada
output_doc_path = "teste_artigo_traduzido.docx"  # Caminho do DOCX de saída

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
                "content": "You are a professional translator that translates Brazilian Portuguese scientific text into English scientific texT, preserving citations like '(1)' and the structure of paragraphs and line breaks."
            },
            {
                "role": "user",
                "content": f"Traduza o texto a seguir do português brasileiro para o inglês, mantendo as citações '(1)' inalteradas e a estrutura do texto:\n\n(Página {page_number+1})\n{extracted_text}"
            }
        ]

        # Chamada à API da OpenAI para tradução da página atual, usando o endpoint de chat
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Ajuste o modelo conforme suas disponibilidades (gpt-4, se tiver acesso)
            messages=messages,
            max_tokens=3000,
            temperature=0.0
        )

        translated_text = response.choices[0].message.content.strip()

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

print("Tradução completa! Documento salvo em:", output_doc_path)

