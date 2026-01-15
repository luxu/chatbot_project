import tempfile

from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render

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
    template_name = 'core/index.html'
    file_pdf: InMemoryUploadedFile = request.FILES['file_pdf']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tf:
        for chunk in file_pdf.chunks():
            tf.write(chunk)
        temp_path = tf.name
    process_pdf_to_chunks(temp_path)
    return render(request, template_name)

def answer(request):
    template_name = 'core/index.html'
    question = request.POST.get('question')
    vector_store = load_existing_vector_store()
    result = ''
    if vector_store:
        retriever = vector_store.as_retriever()
        response = chatbot_ia(retriever, question)
        for resp in response['context']:
            result += resp.page_content
    context = {
        'responses': result,
        'question': question
    }

    return render(request, template_name, context)
