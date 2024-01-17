from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
from django import forms
import random

from . import util

entries = util.list_entries()


class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-3' , 'placeholder' : "Title"} ))
    subject = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control my-3', 'placeholder' : "Subject"}))

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def create_page(request):
    return render(request, "encyclopedia/create-page.html" , {
        "form" : NewPageForm()
    })



def edit_page(request,title):
    subject = util.get_entry(title)
    form = NewPageForm(initial={'title' : title , 'subject' : subject})
    form.fields["title"].widget.attrs['readonly'] = True
    return render(request, "encyclopedia/edit-page.html" , {
        "form" : form
    })


def save_entry(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["subject"]
            util.save_entry(title, content)
            entries.append(title)
            return HttpResponseRedirect(reverse("article" , args=[title]))
        else:
            return render(request, "encyclopedia/edit-page.html" , {
                "form" : form
            })
        
def add_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            for i in entries:
                if title.lower() == i.lower():
                    return render(request, "encyclopedia/create-page.html" , {
                    "error" : "Title already exits",
                    "form" : form
                    })
            content = form.cleaned_data["subject"]
            util.save_entry(title, content)
            entries.append(title)
            return HttpResponseRedirect(reverse("article" , args=[title]))
                    
        else:
            return render(request, "encyclopedia/create-page.html" , {
                "form" : NewPageForm()
            })
        

def get_entry(request,name):
    article = None 
    for i in entries:
        if name.lower() == i.lower():
            article = markdown2.markdown(util.get_entry(i))
    if not article:
        return render(request , 'encyclopedia/not-found.html')    
    return render( request, "encyclopedia/article.html" , {
        "name" : name,
        "article": article
    })


def search_entry(request):
    results = []
    q = request.GET.get('q')
    for i in entries:
        if q.lower() in i.lower():
            results.append(i)
        if q.lower() == i.lower():
            return   HttpResponseRedirect(reverse("article" , args=[i]))
            
    if len(results) > 0 :        
        return render(request, "encyclopedia/search.html",{
            "header" : "Search Results: ",
            "results" : results
        })
    else: 
        return render(request , "encyclopedia/search.html" , {
            "header" : "No Results Found.",
            "message" : "Here are our all topics: "  ,
            "results": entries


        })

def get_random(request):
    random_name = random.choice(entries)
    return HttpResponseRedirect(reverse("article" , args=[random_name]))
