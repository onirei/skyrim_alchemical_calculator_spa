from django.shortcuts import render
from .models import CalculateForm


def get_name(request):
    if request.method == 'POST':
        form = CalculateForm(request.POST)
        if form.is_valid():
            #определяем набор элементов
            if form.cleaned_data["choice_field_last"] == '0':
                bd_data = 'Positive'
            # elif form.cleaned_data["choice_field_last"] == '1':
            else:
                bd_data = 'Negative'

            #определяем режим выборки
            if form.cleaned_data["choice_field"] == '0':
                data = form.finder(form.cleaned_data["attrib_1"], form.cleaned_data["attrib_2"], form.cleaned_data[
                    "attrib_3"], form.cleaned_data["attrib_4"])
            # elif form.cleaned_data["choice_field"] == '1':
            else:
                data = form.optimizer(form.cleaned_data["attrib_1"], form.cleaned_data["attrib_2"], form.cleaned_data[
                    "attrib_3"], form.cleaned_data["attrib_4"], bd_data)

            return render(request, 'skyrim_calk/index.html', {'form': form, 'data': data})
    else:
        form = CalculateForm()

    return render(request, 'skyrim_calk/index.html', {'form': form})


