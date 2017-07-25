from django import forms

from music.models import WeatherTag

WEATHER_CHOICES = (
    ('sunny', '맑음'),
    ('cloudy', '흐림'),
    ('rainy', '비'),
    ('snowy', '눈'),
    ('foggy', '안개'),
)


class MusicChoiceWeatherTagForm(forms.ModelForm):
    weather_tag = forms.MultipleChoiceField(choices=WEATHER_CHOICES)

    class Meta:
        model = WeatherTag
        fields = [
            'sunny',
            'cloudy',
            'foggy',
            'rainy',
            'snowy',
        ]
