from rest_framework import serializers
from .models import Image, Document, Audio, Story

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'persons', 'topic_tags', 'memory_date', 'memory_place', 'description']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'document', 'persons', 'topic_tags', 'memory_date', 'memory_place', 'description']

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'audio', 'persons', 'topic_tags', 'memory_date', 'memory_place', 'description']

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'images', 'title', 'story']