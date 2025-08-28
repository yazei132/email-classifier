document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const textInput = document.getElementById('text-input');
    const fileInput = document.getElementById('file-input');
    const fileName = document.getElementById('file-name');
    const loadingElement = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const resultIcon = document.getElementById('result-icon');
    const resultTitle = document.getElementById('result-title');
    const resultCategory = document.getElementById('result-category');
    const resultExplanation = document.getElementById('result-explanation');
    const responseText = document.getElementById('response-text');
    
    // Mostrar nome do arquivo selecionado
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            fileName.textContent = this.files[0].name;
        } else {
            fileName.textContent = 'Nenhum arquivo selecionado';
        }
    });
    
    analyzeBtn.addEventListener('click', function() {
        const content = textInput.value.trim();
        
        if (!content) {
            alert('Por favor, digite o conteúdo para análise.');
            return;
        }
        
        // Mostrar loading
        loadingElement.style.display = 'block';
        resultContainer.style.display = 'none';
        
        // Simular análise (substitua com sua API real)
        simulateAnalysis(content);
    });
    
    // Função para upload de arquivo
    window.uploadFile = function() {
        const file = fileInput.files[0];
        
        if (!file) {
            alert('Por favor, selecione um arquivo PDF, TXT ou DOCX');
            return;
        }

        // Mostrar loading
        loadingElement.style.display = 'block';
        resultContainer.style.display = 'none';

        // Simular upload e análise (substitua com sua API real)
        setTimeout(() => {
            // Esconder loading
            loadingElement.style.display = 'none';
            
            // Simular resposta
            const simulatedResponse = {
                category: 'produtivo',
                response: 'O documento analisado apresenta conteúdo relevante para o ambiente profissional, com linguagem apropriada e objetivos claros.'
            };
            
            displayResults(simulatedResponse);
        }, 2000);
    };
    
    // Funções para exemplos
    window.loadExample = function(type) {
        const examples = {
            'reuniao': `Prezada equipe,

Gostaria de marcar uma reunião para discutirmos os próximos passos do projeto Alpha. 
Data sugerida: 25/10/2023 às 14h
Local: Sala de reuniões 3B

Pauta:
1. Revisão do cronograma
2. Alinhamento sobre os recursos necessários
3. Definição de metas para o próximo trimestre

Por favor, confirmem sua disponibilidade.

Atenciosamente,
João Silva
Gerente de Projetos`,
            'email': `Assunto: Atualização do Status do Projeto Beta

Prezados stakeholders,

Escrevo para informar que o projeto Beta está 85% completo e dentro do prazo estabelecido. 
Conseguimos resolver os problemas técnicos identificados na semana passada e estamos 
alinhados com as expectativas do cliente.

Próximos passos:
- Finalizar a implementação até sexta-feira
- Realizar testes de integração na próxima semana
- Preparar documentação técnica

Agradeço pelo empenho de todos.

Cordialmente,
Maria Santos
Líder de Projeto`,
            'plano': `Plano de Trabalho - Projeto Gama

Objetivo: Desenvolver novo módulo de relatórios para o sistema interno

Etapas:
1. Análise de requisitos (3 dias)
2. Prototipagem (5 dias)
3. Desenvolvimento (10 dias)
4. Testes (4 dias)
5. Implantação (2 dias)

Recursos necessários:
- 2 desenvolvedores backend
- 1 desenvolvedor frontend
- 1 tester

Entregas esperadas:
- Módulo de relatórios funcional
- Documentação técnica
- Manual do usuário`,
            'feedback': `Olá Carlos,

Gostaria de fornecer um feedback sobre sua apresentação de ontem.

Pontos positivos:
- Domínio do assunto
- Slides bem organizados
- Boa articulação das ideias

Sugestões de melhoria:
- Controlar melhor o tempo (a apresentação excedeu em 15 minutos)
- Incluir mais exemplos práticos
- Envolver mais a audiência com perguntas

No geral, foi uma excelente apresentação. Estou disponível para conversarmos mais sobre isso.

Atenciosamente,
Ana Costa
Coordenadora de Treinamentos`
        };
        
        textInput.value = examples[type] || 'Exemplo não encontrado';
        fileName.textContent = 'Nenhum arquivo selecionado';
        fileInput.value = '';
    };
    
    // Função para simular análise (substitua com chamada API real)
    function simulateAnalysis(content) {
        // Simular tempo de análise
        setTimeout(() => {
            // Esconder loading
            loadingElement.style.display = 'none';
            
            // Simular resposta baseada no conteúdo
            let simulatedResponse;
            
            if (content.length < 50) {
                simulatedResponse = {
                    category: 'improdutivo',
                    response: 'O texto é muito curto para conter informações relevantes para o ambiente profissional.'
                };
            } else if (content.includes('ganhe') || content.includes('oferta') || content.includes('grátis') || 
                      content.includes('limitada') || content.includes('clique aqui')) {
                simulatedResponse = {
                    category: 'improdutivo',
                    response: 'O texto parece ser promocional ou spam, não contendo conteúdo produtivo para o ambiente profissional.'
                };
            } else {
                simulatedResponse = {
                    category: 'produtivo',
                    response: 'O texto analisado apresenta conteúdo relevante para o ambiente de trabalho, com linguagem apropriada e objetivos claros.'
                };
            }
            
            displayResults(simulatedResponse);
        }, 2000);
    }
    
    // Função para exibir resultados
    function displayResults(data) {
        if (data.category === 'produtivo') {
            resultIcon.className = 'result-icon productive';
            resultIcon.innerHTML = '<i class="fas fa-check"></i>';
            resultTitle.textContent = 'Conteúdo Classificado como Produtivo';
            resultCategory.textContent = 'Produtivo';
            resultCategory.className = 'result-category productive';
            resultExplanation.textContent = 'Este conteúdo é relevante para o trabalho ou objetivos profissionais.';
        } else {
            resultIcon.className = 'result-icon unproductive';
            resultIcon.innerHTML = '<i class="fas fa-times"></i>';
            resultTitle.textContent = 'Conteúdo Classificado como Improdutivo';
            resultCategory.textContent = 'Improdutivo';
            resultCategory.className = 'result-category unproductive';
            resultExplanation.textContent = 'Este conteúdo não é relevante para o trabalho ou objetivos profissionais.';
        }
        
        responseText.textContent = data.response;
        resultContainer.style.display = 'block';
        
        // Scroll para o resultado
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    }
});