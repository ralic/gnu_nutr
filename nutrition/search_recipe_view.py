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

class RecipeSearchForm(forms.Form):
    text = forms.CharField(max_length=60)
    category = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(RecipeSearchForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [(c.id, c.name) for c in get_recipe_categories()]


@login_required
def search_recipe(request):
    data = request.GET.copy()
    if data.has_key('text'):
        first_show = False
    else:
        first_show = True
    form = RecipeSearchForm(request.GET)
    if form.is_valid():
        text = form.cleaned_data['text']
        category = int(form.cleaned_data['category'])
        recipes = get_recipes_matching(text, category)
    else:
        recipes = []
        text = ''

    return render_to_response( 'recipe_search.html', {
            "form": form,
            "first_show": first_show,
            "text": text,
            "recipes": recipes
            })

def search_edit_recipe(request):
    data = request.GET.copy()
    if data.has_key('text'):
        first_show = False
    else:
        first_show = True
    form = RecipeSearchForm(request.GET)
    if form.is_valid():
        text = form.cleaned_data['text']
        category = int(form.cleaned_data['category'])
        recipes = get_recipes_matching_owned_by_user(request.user, text, category)
    else:
        recipes = []
        text = ''

    return render_to_response( 'search_edit_recipe.html', {
            "form": form,
            "first_show": first_show,
            "text": text,
            "recipes": recipes
            })