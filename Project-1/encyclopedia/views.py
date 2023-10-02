from django.shortcuts import render
from markdown2 import Markdown

import random

from . import util


def convert_md_to_html(title):
    content = util.get_entry(title)
    md = Markdown()
    if content is None:
        return None
    else:
        return md.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    html_cont = convert_md_to_html(title)
    if html_cont is None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_cont
        })


def search(request):
    if request.method == "POST":
        entry_req = request.POST['q']
        html_cont = convert_md_to_html(entry_req)
        if html_cont is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_req,
                "content": html_cont
            })
        else:
            all_entries = util.list_entries()
            recommend = []
            for entryy in all_entries:
                if entry_req.lower() in entryy.lower():
                    recommend.append(entryy)
            return render(request, "encyclopedia/search.html", {
                "recommend": recommend
            })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        title_exist = util.get_entry(title)
        if title_exist is not None:
            return render(request, 'encyclopedia/error.html', {
                "message": "Entry Page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })


def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def save_page(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def random_page(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = convert_md_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content": html_content
    })
