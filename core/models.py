from django.db import models

class Bot(models.Model):
    answer = models.CharField(max_length=255)
    response = models.CharField(max_length=255)

    def __str__(self):
        return f'Pergunta: {self.answer} Resposta: {self.response}'
