from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    tag1 = models.CharField(max_length=20)
    tag2 = models.CharField(max_length=20)
    tag3 = models.CharField(max_length=20)

class Word(models.Model):
    word_number = models.IntegerField(primary_key=True)
    japanese = models.CharField(max_length=20)
    korean = models.CharField(max_length=20)
    korean_definition = models.CharField(max_length=255)
    tag = models.CharField(max_length=20)

class UserWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    is_favorite = models.BooleanField()
    is_memorized = models.BooleanField()