from django import forms
from .models import Artist
from .models import UserProfile
from django.core.exceptions import ValidationError


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False


class CreateService(forms.ModelForm):

    slots = forms.IntegerField(
        min_value=0,  # Prevent negative values
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
    )


    class Meta:
        model = Artist
        fields = ['tag', 'description', 'dos', 'donts', 'slots', 'image']

    def clean_slots(self):
        slots = self.cleaned_data.get('slots')
        if slots < 1:
            raise ValidationError("Slots cannot be negative or zero.")
        return slots

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
        instance.price = self.cleaned_data.get('price', {})
        if commit:
            instance.save()
        return instance