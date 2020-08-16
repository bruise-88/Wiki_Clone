from django.shortcuts import render
import markdown2
from django import forms

from . import util

import random

cur_title = ""

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def showpage(request, title):
    md = markdown2.Markdown()
    htmlstr = util.get_entry(title)
    if (htmlstr == None):
        return render(request, "encyclopedia/Showpage.html", {
            "title": "Not Found",
            "info": "<p>The item is not available on wiki, sorry try another word</p>",
            "dis": "none"
        })
    html = md.convert(htmlstr)
    global cur_title
    cur_title = title

    return render(request, "encyclopedia/Showpage.html", {
        "title": title,
        "info": html
    })


def search(request):
    if request.method == "GET":
        query = request.GET.get('q')
        entries = util.list_entries()
        matchlist = []
        for entry in entries:
            if query.casefold() == entry.casefold():
                return showpage(request, query)
            elif entry.casefold().count(query.casefold()):
                matchlist.append(entry)
        if not matchlist:
            return showpage(request, "#")
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": matchlist
            })


class Newpageform(forms.Form):
    title = forms.CharField()
    mdtxt = forms.CharField(widget=forms.Textarea)


def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    else:
        form = Newpageform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            mdtxt = form.cleaned_data["mdtxt"]
            if title in util.list_entries():
                return render(request, "encyclopedia/Showpage.html", {
                    "title": "Alread Exists",
                    "info": "<p>The item submitted already exits in this encyclopedia</p>",
                    "dis": "none"
                })
            else:
                with open(f'entries\\{title}.md', mode='w') as f1:
                    f1.write(mdtxt)
                return showpage(request, title)
        else:
            return render(request, "encyclopedia/Showpage.html", {
                "title": "Invalid Submission",
                "info": "<p>You left some field empty, try again!</p>",
                "dis": "none"
            })


class Editpageform(forms.Form):
    title = forms.CharField(widget=forms.Textarea)
    mdtxt = forms.CharField(widget=forms.Textarea)


def editpage(request):
    print(cur_title)
    if request.method == "GET":
        with open(f'entries\\{cur_title}.md', mode='r') as f1:
            mdtxt = f1.read()
        return render(request, "encyclopedia/editpage.html",
                      {
                          "title" : cur_title,
                          "mdtxt": mdtxt
                      })
    else:
        form = Editpageform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            mdtxt = form.cleaned_data["mdtxt"]
            with open(f'entries\\{title}.md', mode='w') as f1:
                print(f1.write(mdtxt))
            return showpage(request, title)
        else:
            return render(request, "encyclopedia/Showpage.html", {
                "title": "Invalid Submission",
                "info": "<p>You left some field empty, try again!</p>",
                "dis": "none"
            })


def randompage(request):
    option = random.choice(util.list_entries())
    return showpage(request, option)
