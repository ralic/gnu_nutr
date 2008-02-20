# web_nutrition: a web based nutrition and diet analysis program.
# Copyright (C) 2008 Edgar Denny

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django import newforms as forms

from models import *

from constants import tracked_nutrient


def get_nutrient_choices():
    choices = [(-1, '')]
    for nutr_id, unit_of_measure, nutr_desc in tracked_nutrient.general:
        choices.append((nutr_id, nutr_desc))
    for nutr_id, unit_of_measure, nutr_desc in tracked_nutrient.vitamins:
        choices.append((nutr_id, nutr_desc))
    for nutr_id, unit_of_measure, nutr_desc in tracked_nutrient.minerals:
        choices.append((nutr_id, nutr_desc))
    for nutr_id, unit_of_measure, nutr_desc in tracked_nutrient.amino_acids:
        choices.append((nutr_id, nutr_desc))
    for nutr_id, unit_of_measure, nutr_desc in tracked_nutrient.fats:
        choices.append((nutr_id, nutr_desc))
    return choices

def get_factor_choices():
    return [(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1'), (0, ''), (-1, '-1'), (-2, '-2'), (-3, '-3'), (-4, '-4'), (-5, '-5')]


class NutrientSearchForm(forms.Form):
    food_group = forms.ChoiceField()
    nutrient_1 = forms.ChoiceField()
    factor_1 = forms.ChoiceField()
    nutrient_2 = forms.ChoiceField()
    factor_2 = forms.ChoiceField()
    nutrient_3 = forms.ChoiceField()
    factor_3 = forms.ChoiceField()
    nutrient_4 = forms.ChoiceField()
    factor_4 = forms.ChoiceField()
    nutrient_5 = forms.ChoiceField()
    factor_5 = forms.ChoiceField()
    nutrient_6 = forms.ChoiceField()
    factor_6 = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(NutrientSearchForm, self).__init__(*args, **kwargs)
        self.fields['food_group'].choices = \
            [(c.group_id, c.name) for c in get_food_groups()]
        nutr_choices = get_nutrient_choices()
        factor_choices = get_factor_choices()
        self.fields['nutrient_1'].choices = \
            [(c[0], c[1]) for c in nutr_choices]
        self.fields['nutrient_2'].choices = \
            [(c[0], c[1]) for c in nutr_choices]
        self.fields['nutrient_3'].choices = \
            [(c[0], c[1]) for c in nutr_choices]
        self.fields['nutrient_4'].choices = \
            [(c[0], c[1]) for c in nutr_choices]
        self.fields['nutrient_5'].choices = \
            [(c[0], c[1]) for c in nutr_choices]
        self.fields['nutrient_6'].choices = \
            [(c[0], c[1]) for c in nutr_choices]
        self.fields['factor_1'].choices = \
            [(c[0], c[1]) for c in factor_choices]
        self.fields['factor_2'].choices = \
            [(c[0], c[1]) for c in factor_choices]
        self.fields['factor_3'].choices = \
            [(c[0], c[1]) for c in factor_choices]
        self.fields['factor_4'].choices = \
            [(c[0], c[1]) for c in factor_choices]
        self.fields['factor_5'].choices = \
            [(c[0], c[1]) for c in factor_choices]
        self.fields['factor_6'].choices = \
            [(c[0], c[1]) for c in factor_choices]

class FormErrors:
    def __init__(self):
        self.factor_1 = False
        self.nutrient_1 = False
        self.factor_2 = False
        self.nutrient_2 = False
        self.factor_3 = False
        self.nutrient_3 = False
        self.factor_4 = False
        self.nutrient_4 = False
        self.factor_5 = False
        self.nutrient_5 = False
        self.factor_6 = False
        self.nutrient_6 = False

def validate(data):
    errors = FormErrors()
    has_errors = False
    if data['nutrient_1'] != '-1' and data['factor_1'] == '0':
        errors.factor_1 = True
        has_errors = True
    if data['nutrient_1'] == '-1' and data['factor_1'] != '0':
        errors.nutrient_1 = True
        has_errors = True
    if data['nutrient_2'] != '-1' and data['factor_2'] == '0':
        errors.factor_2 = True
        has_errors = True
    if data['nutrient_2'] == '-1' and data['factor_2'] != '0':
        errors.nutrient_2 = True
        has_errors = True
    if data['nutrient_3'] != '-1' and data['factor_3'] == '0':
        errors.factor_3 = True
        has_errors = True
    if data['nutrient_3'] == '-1' and data['factor_3'] != '0':
        errors.nutrient_3 = True
        has_errors = True
    if data['nutrient_4'] != '-1' and data['factor_4'] == '0':
        errors.factor_4 = True
        has_errors = True
    if data['nutrient_4'] == '-1' and data['factor_4'] != '0':
        errors.nutrient_4 = True
        has_errors = True
    if data['nutrient_5'] != '-1' and data['factor_5'] == '0':
        errors.factor_5 = True
        has_errors = True
    if data['nutrient_5'] == '-1' and data['factor_5'] != '0':
        errors.nutrient_5 = True
        has_errors = True
    if data['nutrient_6'] != '-1' and data['factor_6'] == '0':
        errors.factor_6 = True
        has_errors = True
    if data['nutrient_6'] == '-1' and data['factor_6'] != '0':
        errors.nutrient_6 = True
        has_errors = True
    return has_errors, errors

def save_nutrient_search_data_to_session(session, data):
    session['nutrient_search'] = {}
    for key, val in data.items():
        session['nutrient_search'][key] = val

@login_required
def nutrient_search(request):
    if request.GET:
        data = request.GET.copy()
        form = NutrientSearchForm(data)
        if data.has_key('search'):
            has_errors, errors = validate(data)
            if not has_errors:
                save_nutrient_search_data_to_session(request.session, data)
                return HttpResponseRedirect( '/nutrient_search_result/')

    else:
        form = NutrientSearchForm({'factor_1':0, 'factor_2':0, 'factor_3':0, 'factor_4':0,
                                   'factor_5':0, 'factor_6':0})
        errors = FormErrors()
    return render_to_response( 'nutrient_search.html',{
            'form': form,
            'errors':errors})