from django.shortcuts import render
from django.shortcuts import redirect
from random import choice
from django import forms
from django.core.exceptions import ValidationError

from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

class NewEditForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label=False, widget=forms.Textarea())
    new = forms.BooleanField(label="new", widget=forms.HiddenInput, required=False, initial="True")
    
    # Data Validation, to check that when a user tries to create a new page if it exisits it throws an error
    # If a user is editing an exisiting page however we permit the title 
    def clean_title(self):
        title = self.cleaned_data['title']
        if (title in util.list_entries()) and self.data['new']=="True":
            raise ValidationError("Page Already Exists")
        return title 
    


def index(request):
    entriesList = util.list_entries()
    title = "All Pages"
    # Check to see wether we are at the index page based on submitting a search
    search = request.GET.get('q', None)
    if search is not None:

        # If the searched term is a page we return the page
        if search in entriesList:        
            return HttpResponseRedirect(reverse("project_1_wiki/wikientry", args=(search,)))

        # Else we see if it exists as a substring of pages and returns a list of pages
        filteredEntries = [] 
        for entry in entriesList:
            if search.lower() in entry.lower():
                filteredEntries.append(entry)

        # We update the page title and entries list acoriding to the search result
        title = search
        entriesList = filteredEntries

    # Renders a list of entries, either all if not a result of a search call else renders results
    return render(request, "project_1_wiki/index.html", {
        "title": title,
        "entries": entriesList
    })



def random(request):
    # When random is called we redirect to a random wiki entry page
    return HttpResponseRedirect(reverse("project_1_wiki/wikientry", args=(choice(util.list_entries()),)))



def wikientry(request, entry):

    exists = False
    html = str

    # Check to ensure that the page the user is trying to acess is an existing wiki entry
    if util.get_entry(entry) is not None: 
        exists=True
        html = util.markdown2html(entry)

    # Renders the wiki entry otherwise an error messsage for page not found
    return render(request, "project_1_wiki/entry.html", {
        "entry": entry,
        "html": html,
        "exists": exists
    })



def edit(request):
    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewEditForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            util.save_entry(title, content)

            # On Sucess we redirect to the edited page
            return HttpResponseRedirect(reverse("project_1_wiki/wikientry", args=(title,)))

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "project_1_wiki/edit.html", {
                "form": form
            })

    # Check if this page was called from an exisiting page
    entry = request.GET.get('entry', None)
    if entry is not None: 

        # Create a form using existing data from the page the edit request came from
        form = NewEditForm(initial={
            "content": util.get_entry(entry),
            "new": 'False',
            "title": entry
        })

        # Stop the user from being able to edit the page title
        form.fields['title'].widget.attrs['readonly'] = True
    # Else we create a new form for a new page
    else: form = NewEditForm()

    # Renders the form for the user to edit/create a page
    return render(request, "project_1_wiki/edit.html", {
        "form": form
    })