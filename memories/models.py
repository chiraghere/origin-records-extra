from django.db import models
from api.models import Person

def path_file_name(instance, filename):
    return '/'.join(filter(None, ("memories", "images", instance.contributed_by ,filename)))

def path_file_name_two(instance, filename):
    return '/'.join(filter(None, ("memories", "documents", instance.contributed_by ,filename)))

def path_file_name_three(instance, filename):
    return '/'.join(filter(None, ("memories", "audios", instance.contributed_by ,filename)))

class Image(models.Model):
    image = models.ImageField(upload_to=path_file_name)
    persons = models.ManyToManyField(Person, related_name='taggedin_images')
    topic_tags = models.CharField(max_length=64, null=True)
    memory_date = models.DateField()
    memory_place = models.CharField(max_length=64, null=True)
    description = models.CharField(max_length=200, null=True)
    contributed_by = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='contributed_images')

class Document(models.Model):
    document = models.FileField(upload_to=path_file_name_two)
    persons = models.ManyToManyField(Person, related_name="taggedin_documents")
    topic_tags = models.CharField(max_length=64, null=True)
    memory_date = models.DateField()
    memory_place = models.CharField(max_length=64, null=True)
    description = models.CharField(max_length=200, null=True)
    contributed_by = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='contributed_documents')

class Audio(models.Model):
    audio = models.FileField(upload_to=path_file_name_three)
    persons = models.ManyToManyField(Person, related_name="taggedin_audios")
    topic_tags = models.CharField(max_length=64, null=True)
    memory_date = models.DateField()
    memory_place = models.CharField(max_length=64, null=True)
    description = models.CharField(max_length=200, null=True)
    contributed_by = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='contributed_audios')

class Story(models.Model):
    images = models.ManyToManyField(Image)
    title = models.CharField(max_length=144)
    story = models.CharField(max_length=400)