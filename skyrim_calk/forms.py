from django import forms
from .methods import selectors

class CalculateForm(forms.Form):

    CHOICES = selectors
    attrib_1 = forms.ChoiceField(label='', choices=CHOICES, required=True)
    attrib_2 = forms.ChoiceField(label='', choices=CHOICES, required=False)
    attrib_3 = forms.ChoiceField(label='', choices=CHOICES, required=False)
    attrib_4 = forms.ChoiceField(label='', choices=CHOICES, required=False)

    CHOICES = (('0', 'Поиск',), ('1', 'Оптимизация',))
    choice_field = forms.ChoiceField(label='Режим', widget=forms.RadioSelect, choices=CHOICES, initial='0')
    CHOICES2 = (('0', 'Положительные',), ('1', 'Отрицательные',))
    choice_field_last = forms.ChoiceField(label='Ключевой эффект', widget=forms.RadioSelect, choices=CHOICES2,
                                          initial='0')