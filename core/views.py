import tempfile

from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render

from decouple import config

from core.models import Bot
from ia.model_ia import process_pdf_to_chunks, load_existing_vector_store, chatbot_ia


@login_required
def index(request):
    template_name = 'core/index.html'
    if request.method == 'POST':
        question = request.POST.get('question')
        context = {
            'answer': question
        }
        return render(request, template_name, context)
    return render(request, template_name)


def upload_pdf(request):
    try:
        openai_api_key = config("OPENAI_API_KEY")
        print(f"Tudo certo, chave da API OpenAI encontrada")
    except Exception as e:
        print(f"Erro ao ler OPENAI_API_KEY usando decouple: {e}")
        raise ValueError("Chave da API OpenAI não encontrada via decouple")
    template_name = 'core/index.html'
    file_pdf: InMemoryUploadedFile = request.FILES['file_pdf']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tf:
        for chunk in file_pdf.chunks():
            tf.write(chunk)
        temp_path = tf.name
    process_pdf_to_chunks(temp_path,openai_api_key)
    return render(request, template_name)


def answer(request):
    template_name = 'core/index.html'
    question = request.POST.get('question')
    openai_api_key = config("OPENAI_API_KEY")
    # NÃO foi criado a API e vai usar o padrão do chat
    if len(openai_api_key) == 0:
        bot = Bot.objects.filter(answer__icontains=question)
        response = [resp.response for resp in bot]
        # Se a pergunta(answer) não tiver na Base de Dados, retorna a resposta padrão
        if not response:
            response = 'Pergunta não consta nas palavras chave.'
        else:
            # Se a pergunta(answer) tiver na Base de Dados, retorna a resposta
            response = response[0]
    else:
        vector_store = load_existing_vector_store(openai_api_key)
        response = ''
        if vector_store:
            retriever = vector_store.as_retriever()
            response = chatbot_ia(retriever, question, openai_api_key)
            for resp in response['context']:
                response += resp.page_content
    context = {
        'responses': response,
        'question': question
    }

    return render(request, template_name, context)
