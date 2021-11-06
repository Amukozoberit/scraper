from django import forms

Radius_CHOICES= [
    ('orange', 'Oranges'),
    ('cantaloupe', 'Cantaloupes'),
    ('mango', 'Mangoes'),
    ('honeydew', 'Honeydews'),
    ]

class UserForm(forms.Form):
    search=forms.CharField(max_length=10)
    radius= forms.CharField(label='Choose radius', widget=forms.Select(choices=Radius_CHOICES))

