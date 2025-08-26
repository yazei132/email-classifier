from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import requests
import os
import google.generativeai as genai
import unicodedata

# ===== CONFIGURAÇÃO INICIAL =====
app = Flask(__name__)
CORS(app)

# ===== CONFIGURAÇÃO GEMINI AI =====
# ===== CHAVE DA API =====
GENINI_API_KEY = "AIzaSyCc73A4noSXLwjtn-9Cyfoq_o_lqUZAuyU"
genai.configure(api_key=GENINI_API_KEY)

# ===== DOWNLOAD RECURSOS NLTK =====
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# ===== INICIALIZAR NLTK =====
stemmer = PorterStemmer()
stop_words = set(stopwords.words('portuguese'))

# ===== FUNÇÕES AUXILIARES =====
def remove_accents(text):
    """Remove acentos do texto"""
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                  if unicodedata.category(c) != 'Mn')

def preprocess_text(text):
    """
    Pré-processamento de texto: remove caracteres especiais, converte para minúsculas,
    remove stopwords e aplica stemming.
    """
    # Converter para minúsculas
    text = text.lower()
    
    # Remover acentos
    text = remove_accents(text)
    
    # Remover caracteres especiais e números (mantém letras e espaços)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenização
    try:
        tokens = word_tokenize(text, language='portuguese')
    except:
        # Fallback para tokenização simples se houver erro
        tokens = text.split()
    
    # Remover stopwords e aplicar stemming
    filtered_tokens = []
    for word in tokens:
        if word not in stop_words and len(word) > 2:
            try:
                stemmed_word = stemmer.stem(word)
                filtered_tokens.append(stemmed_word)
            except:
                filtered_tokens.append(word)
    
    return " ".join(filtered_tokens)

# ===== CLASSIFICAÇÃO COM GEMINI AI =====
def classify_email_gemini(text):
    """
    Classifica e-mail usando Google Gemini de forma INTELIGENTE
    """
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Classifique este e-mail como APENAS "produtivo" ou "improdutivo".
    
    REGRAS:
    - PRODUTIVO: trabalho, projetos, reuniões, prazos, desenvolvimento profissional, 
                questões técnicas, ajuda profissional, resolução de problemas
    - IMPRODUTIVO: spam, promoções, loterias, esquemas, conteúdo não profissional,
                  golpes, phishing, marketing não solicitado
    
    IMPORTANTE: 
    - "urgente" pode ser produtivo se for sobre trabalho!
    - "ajuda" pode ser produtivo se for técnica/profissional!
    - "resolver" é geralmente produtivo!
    
    Responda APENAS com uma palavra: "produtivo" ou "improdutivo"
    
    E-MAIL: {text}
    """
    
    try:
        response = model.generate_content(prompt)
        classification = response.text.strip().lower()
        
        if "produtivo" in classification:
            return "produtivo"
        elif "improdutivo" in classification:
            return "improdutivo"
        else:
            # Fallback para método tradicional se a IA não responder corretamente
            return classify_email_fallback(text)
            
    except Exception as e:
        print(f"Erro Gemini: {e}")
        return classify_email_fallback(text)

# ===== FALLBACK TRADICIONAL =====
def classify_email_fallback(text):
    """
    Fallback: classificação baseada em palavras-chave se a API falhar
    """
    processed_text = preprocess_text(text)
    processed_no_accents = remove_accents(processed_text.lower())
    
    productive_keywords = [
        'reuniao', 'projeto', 'trabalho', 'relatorio', 'prazo', 'entrega', 
        'cliente', 'negocio', 'contrato', 'proposta', 'orcamento', 'desenvolvimento',
        'apresentacao', 'metas', 'objetivos', 'resultados', 'relatorios',
        'ajuda', 'suporte', 'resolver', 'solucionar', 'duvida', 'pendencia',
        'problema', 'tecnico', 'sistema', 'codigo', 'programacao', 'implementacao',
        'urgente', 'importante', 'prioridade'
    ]
    
    unproductive_keywords = [
        'promocao', 'desconto', 'ofertas', 'spam', 'loteria', 'premio',
        'ganhador', 'heranca', 'gratis', 'limitado', 'oportunidade', 
        'fortuna', 'dinheiro', 'riqueza', 'investimento', 'ganhe', 'prize',
        'winner', 'million', 'bilion', 'fortune'
    ]
    
    productive_count = sum(1 for word in productive_keywords if word in processed_no_accents)
    unproductive_count = sum(1 for word in unproductive_keywords if word in processed_no_accents)
    
    if productive_count > unproductive_count:
        return "produtivo"
    else:
        return "improdutivo"

# ===== GERAÇÃO DE RESPOSTA =====
def generate_response(category, original_text):
    """
    Gera uma resposta automática baseada na categoria do e-mail.
    """
    if category == "produtivo":
        responses = [
            "Obrigado pelo seu e-mail. Analisarei o conteúdo com atenção e retornarei em breve.",
            "Agradeço pelo contato. Estou revisando as informações e em breve darei um retorno.",
            "Recebi seu e-mail e vou analisar o conteúdo. Retornarei o mais breve possível.",
            "Obrigado pela mensagem. Estou verificando as informações e em breve entrarei em contato."
        ]
        return responses[len(original_text) % len(responses)]
    else:
        responses = [
            "Obrigado pelo contato. No momento, estou focado em prioridades profissionais específicas.",
            "Agradeço sua mensagem, mas não estou considerando este tipo de oportunidade no momento.",
            "Obrigado pelo e-mail. No momento, não estou envolvido com este tipo de proposta.",
            "Agradeço o contato, mas este não é um assunto que eu possa priorizar no momento."
        ]
        return responses[len(original_text) % len(responses)]

# ===== ROTAS FLASK =====
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_email():
    try:
        data = request.get_json()
        email_content = data.get('email_content', '')
        
        if not email_content:
            return jsonify({'error': 'Nenhum conteúdo de e-mail fornecido'}), 400
        
        # Classificar o e-mail com Gemini AI
        category = classify_email_gemini(email_content)
        
        # Gerar resposta automática
        response = generate_response(category, email_content)
        
        return jsonify({
            'category': category,
            'response': response
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao processar o e-mail: {str(e)}'}), 500

# ===== EXECUÇÃO DO SERVIDOR FLASK =====
if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📧 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)