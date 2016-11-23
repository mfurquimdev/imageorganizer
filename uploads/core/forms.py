from django import forms

from uploads.core.models import Document, Sprite

class SpriteForm(forms.ModelForm):
    class Meta:
        model = Sprite
        fields = ('image', )


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
