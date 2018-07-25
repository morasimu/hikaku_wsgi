from django.shortcuts import render
from django.template.context_processors import request
from hikaku.extract_api import Yahoo_api, Rakuten_api, Amazon_html
from hikaku.forms import InputForm, InputForm2

# Create your views here.
def index(request):
    form = InputForm()
    return render(request, 'search_ver1.html', {'form':form})

def go_test(request):
    form = InputForm()
    return render(request, 'search_ver1.html', {'form':form})

def result(request):
    form = InputForm(request.POST)
    re_form = InputForm2()
    if not form.is_valid():
        return render(request, 'search_ver1.html', {'form': form})
    data_y = Yahoo_api(form.cleaned_data['q']).res
    data_r = Rakuten_api(form.cleaned_data['q']).res
    data_a = Amazon_html(form.cleaned_data['q']).res
    data_y.update(data_r)
    data_y.update(data_a)
    data_y.update({'form':re_form, 'keyw':form.cleaned_data['q']})
    return render(request, 'result.html', data_y)
