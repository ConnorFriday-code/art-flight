from django import forms
from .models import Artist

class CreateService(forms.ModelForm):
    price_keys = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter price keys (one per line)'}),
        required=False
    )
    price_values = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter corresponding prices (one per line)'}),
        required=False
    )

    tag = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'tag-input',
                'placeholder': 'Type a tag',
                'autocomplete': 'off'
            }
        ),
        label="Tag"
    )

    class Meta:
        model = Artist
        fields = ['tag','description','dos','donts', 'slots', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.price:
            keys, values = zip(*self.instance.price.items())
            self.fields['price_keys'].initial = "\n".join(keys)
            self.fields['price_values'].initial = "\n".join(map(str, values))

    def clean(self):
        cleaned_data = super().clean()
        price_keys = cleaned_data.get('price_keys', '').splitlines()
        price_values = cleaned_data.get('price_values', '').splitlines()

        if len(price_keys) != len(price_values):
            raise forms.ValidationError("The number of keys and values must match.")

        try:
            cleaned_data['price'] = dict(zip(price_keys, map(float, price_values)))
        except ValueError:
            raise forms.ValidationError("All price values must be valid numbers.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Assign the cleaned `price` to the model instance
        instance.price = self.cleaned_data.get('price', {})
        if commit:
            instance.save()
        return instance