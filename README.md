### **Projeto: Desenvolvimento de Chatbot Básico em Python com Django**

### Descrição do Projeto
- Desenvolvimento de um chatbot básico utilizando Python e Django, com lógica simples de perguntas e respostas pré-definidas.
O projeto tem como objetivo demonstrar organização de código, domínio de lógica de programação e uso do framework Django, sem integrações complexas.


- O chatbot poderá ser acessado por meio de uma interface web simples ou por uma view básica no Django, conforme necessidade do cliente.

### Objetivo
Criar um chatbot que:

- **Receba mensagens do usuário**

- **Identifique palavras-chave**

- **Retorne respostas pré-definidas**

- **Possua estrutura simples e de fácil manutenção**

### Tecnologias Utilizadas
- Python/Django
- Estruturas de dados (dict, list)
- Templates HTML básicos do Django (quando aplicável)

### Funcionalidades
- Campo para envio de mensagens
- Respostas automáticas baseadas em palavras-chave
- Resposta padrão para mensagens não reconhecidas
- Opção de reiniciar a conversa

Código organizado seguindo o padrão do Django

### Escopo do Projeto:
- [x] Criação do projeto e app Django
- [x] Implementação da lógica do chatbot
- [x] Views simples para processamento das mensagens
- [x] Templates básicos, se necessário
- [x] Código comentado e organizado
- [x] Autenticação de usuários

### Fora do Escopo
- [x] Integração com IA ou APIs externas
- [x] Banco de dados avançado
- [] Processamento de linguagem natural

### Prazo
- 7 dias corridos, incluindo desenvolvimento e ajustes finais.(09 a 16/01)

### Entregáveis
- Código-fonte completo

### Instruções para execução do projeto
- Clone o projeto em sua máquina
````bash
 git clone https://github.com/lucas-almeida-silva/chatbot-django.git
````
Instale o gerenciador de pacotes: ``uv``
````bash
https://docs.astral.sh/uv/#highlights
````
Entre na pasta do projeto
````code
cd chatbot_project
````

Crie o ambiente virtual 
````bash
 uv venv
````

Ative o ambiente virtual
````bash
WINDOWS: .venv\Scripts\activate
LINUX/MAC: source .venv\Bin\activate
````
Instalar as dependências
````bash
 uv sync
````
Renomeie o env-sample
````bash
 mv env-sample .env
````
Rode as migrações
````bash
 task migrate
````
Criar um superuser
````bash
 task createsuperuser
````
Rodar a aplicação
````bash
 task runserver
````

### OBS: Para funcionamento correto da IA do OpenAI, vc deve criar uma conta no site da OpenAI e obter sua chave de API. Após, colocar a chave no arquivo ***.env**, sem isso vai dar erro.

### Estrutura preparada para futuras evoluções