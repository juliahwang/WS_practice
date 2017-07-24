from django import forms

WEATHER_CHOICES = (
        ('sunny', '맑음'),
        ('cloudy', '흐림'),
        ('rainy', '비'),
        ('snowy', '눈'),
        ('foggy', '안개'),
    )


class MusicChoiceWeatherTagForm(forms.ModelForm):
    weathertag = forms.MultipleChoiceField(choices=WEATHER_CHOICES)
