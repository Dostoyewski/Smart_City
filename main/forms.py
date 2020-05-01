from django import forms

GENDER = (
    (0, "MALE"),
    (1, "FEMALE")
)


class ChangeForm(forms.Form):
    """
    Form for updating profile data
    """
    name = forms.CharField(max_length=50, label='Имя')
    vorname = forms.CharField(max_length=50, label='Фамилия')
    fathername = forms.CharField(max_length=50, label='Отчество')
    gender = forms.ChoiceField(choices=GENDER, label='Пол')
    age = forms.DateField(label='Возраст')
    position = forms.CharField(max_length=50, label='Должность')
    exp = forms.IntegerField(label='Стаж')
    message = forms.CharField(label='Сообщение')
