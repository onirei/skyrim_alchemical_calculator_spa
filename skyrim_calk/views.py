from django.shortcuts import render
from .forms import CalculateForm
from .methods import finder, optimizer

def get_name(request):
    if request.method == 'POST':
        form = CalculateForm(request.POST)
        if form.is_valid():
            #определяем набор элементов
            if form.cleaned_data["choice_field_last"] == '0':
                bd_data = 'Positive'
            else:
                bd_data = 'Negative'

            #определяем режим выборки
            if form.cleaned_data["choice_field"] == '0':
                data = finder(form.cleaned_data["attrib_1"], form.cleaned_data["attrib_2"], form.cleaned_data[
                    "attrib_3"], form.cleaned_data["attrib_4"])
            else:
                data = optimizer(form.cleaned_data["attrib_1"], form.cleaned_data["attrib_2"], form.cleaned_data[
                    "attrib_3"], form.cleaned_data["attrib_4"], bd_data)

            return render(request, 'skyrim_calk/index.html', {'form': form, 'data': data})
    else:
        form = CalculateForm()

    return render(request, 'skyrim_calk/index.html', {'form': form})


