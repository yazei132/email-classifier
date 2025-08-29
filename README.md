📧 Email Classifier - Sistema de Classificação de Emails
Um sistema inteligente que classifica emails em "produtivos" ou "improdutivos" utilizando Google Gemini AI e gera respostas automáticas personalizadas.

✨ Funcionalidades
🤖 Classificação Inteligente: Usa Google Gemini AI para análise contextual de emails.

📝 Respostas Automáticas: Gera respostas personalizadas baseadas na categoria do email

🌐 Interface Web: Interface amigável com Flask e HTML/CSS/JS

🔧 Fallback Inteligente: Sistema tradicional baseado em palavras-chave caso a API falhe

🎯 Pré-processamento Avançado: Limpeza e normalização de texto com NLTK

🛠️ Tecnologias Utilizadas
Backend: Python, Flask, Flask-CORS

IA: Google Gemini AI API

NLP: NLTK (Natural Language Toolkit)

Frontend: HTML5, CSS3, JavaScript

Processamento de Texto: Regex, Unidecode

📋 Pré-requisitos
Python 3.8+

Conta no Google AI Studio (para chave API do Gemini)

pip (gerenciador de pacotes Python)

🚀 Instalação e Configuração
1. Clone o repositório
bash
git clone <url-do-repositorio>
cd email-classifier
2. Crie um ambiente virtual (recomendado)
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
3. Instale as dependências
bash
pip install -r requirements.txt
4. Configure a API Key do Gemini
Edite o arquivo app.py e substitua a chave API:

python
GENINI_API_KEY = "sua_chave_api_aqui"
Ou configure como variável de ambiente:

bash
export GEMINI_API_KEY="AIzaSyCc73A4noSXLwjtn-9Cyfoq_o_lqUZAuyU"
5. Execute a aplicação
bash
python app.py
6. Acesse a aplicação
Abra seu navegador e vá para: http://localhost:5000

🎮 Como Usar
Acesse a página inicial no navegador

Cole o conteúdo do email na área de texto

Clique em "Analisar Email"

Veja o resultado:

Classificação (Produtivo/Improdutivo)

Resposta automática sugerida

📊 Exemplos de Classificação
✅ Emails Produtivos
Assuntos de trabalho/projetos

Reuniões profissionais

Prazos e entregas

Dúvidas técnicas

Resolução de problemas

❌ Emails Improdutivos
Spam e promoções

Loterias e esquemas

Marketing não solicitado

Golpes e phishing

Conteúdo não profissional

Arquivo deployado https://email-classifier-17xp.onrender.com/
