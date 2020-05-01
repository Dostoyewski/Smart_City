from django import forms

GENDER = (
    (0, "MALE"),
    (1, "FEMALE")
)


class ParserForm(forms.Form):
    """
    Form for updating profile data
    """
    name = forms.CharField(max_length=50, label='Имя')
    vorname = forms.CharField(max_length=50, label='Фамилия')
    fathername = forms.CharField(max_length=50, label='Отчество')
    gender = forms.ChoiceField(choices=GENDER, label='Пол')
    age = forms.IntegerField(label='Возраст')
    urlVK = forms.CharField(max_length=50, label='ссылка VK')

