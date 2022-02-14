from django import forms


class PrivateMessageForm(forms.Form):
    subscriber_number = forms.IntegerField(label='Абонентский номер')
    message = forms.CharField(
        label='Сообщение', max_length=900, widget=forms.Textarea)
