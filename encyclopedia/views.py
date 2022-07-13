from django.shortcuts import render
from . import util
from markdown2 import markdown
from django.http import Http404, HttpResponseRedirect
from random import choice
from django import forms
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# returns entry based on title entered by user
def view_entry(request, entry):
    if util.get_entry(entry):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown(util.get_entry(entry)),
            "title": entry
            })
    else:
        raise Http404()

def search_results(request):
    term = request.GET.get('term')
    if util.search(term):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown(util.get_entry(term)),
            "title": term
            })
    else:
        util.possible_matches(term)
        return render(request, "encyclopedia/results.html", {
            "matches": util.possible_matches(term),
            })

def random_entry(request):
    entry = choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown(util.get_entry(entry)),
        "title": entry
        })

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title")
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":5}), label="Entry Content")

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            if util.get_entry(title) == None:
                util.save_entry(title, body)
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.error(request,'Error: Entry already exist. Please choose a new title or edit the existing entry.')
                return render(request, 'encyclopedia/new.html', context={'form': form})

        else:
            return render(request, "encyclopedia/index.html"), {
                "form": form
            }

    return render(request, "encyclopedia/new.html", {
        "form":NewEntryForm(),
    })

def edit_entry(request):

    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            util.save_entry(title, body)
            return redirect('entry', title)

    if request.method == "GET":
        title = request.GET.get("title")
        form = NewEntryForm(initial={"title": title, "body":util.get_entry(title)})

        return render(request, "encyclopedia/edit.html", {
            "form": form
            })
