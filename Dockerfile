# Usa imagem oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pela API
EXPOSE 10000

# Comando para rodar o servidor FastAPI
CMD ["uvicorn", "ApiConsultaLivro:app", "--host", "0.0.0.0", "--port", "10000"]
