from django import forms

class InputForm(forms.Form):
    q = forms.CharField(required=True, max_length=256, widget=forms.TextInput(attrs={'rows':'1','size':'40', 'placeholder':'検索したい商品名や型番を入力してください。', 'style':'font-size:30px; border:12px #00b388 solid;'}))

class InputForm2(forms.Form):
    q = forms.CharField(required=True, max_length=256, widget=forms.TextInput(attrs={'style':'border:5px #00b388 solid;'}))

