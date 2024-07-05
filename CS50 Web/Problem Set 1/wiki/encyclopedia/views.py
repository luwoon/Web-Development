from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
import markdown2
import random

from . import util


class SearchForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Search Encyclopedia"}))


class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    md = forms.CharField(label="Content", widget=forms.Textarea)


class EditForm(forms.Form):
    md = forms.CharField(label="Content", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def entry(request, title):
    if title in util.list_entries():
        entry_content = util.get_entry(title)
        content = markdown2.markdown(entry_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content,
            "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Sorry, the page you are looking for does not exist.",
            "form": SearchForm()
        })
    

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title):
                return redirect(reverse("entry", args=[title]))
            else:
                entries = [entry for entry in util.list_entries() if title.lower() in entry.lower()]
                return render(request, "encyclopedia/search_results.html", {
                    "title": title,
                    "entries": entries,
                    "form": SearchForm()
                })
    return redirect(reverse("index"))


def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_content = form.cleaned_data["md"]
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "message": "Page already exists.",
                    "form": SearchForm()
                })
            else:
                util.save_entry(title, entry_content)
                return redirect(reverse("entry", args=[title]))
    return render(request, "encyclopedia/create.html", {
            "create_form": CreateForm(),
            "form": SearchForm()
        })


def edit(request, title):
    if request.method == "GET":
        entry_content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
          "title": title,
          "edit_form": EditForm(initial={"md":entry_content}),
          "form": SearchForm()
        })
    elif request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            entry_content = form.cleaned_data["md"]
            util.save_entry(title, entry_content)
            return redirect(reverse("entry", args=[title]))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": entry_content,
        "form": SearchForm()
    })


def random_page(request):
    list = util.list_entries()
    random_entry = random.choice(list)
    return redirect(reverse("entry", args=[random_entry]))