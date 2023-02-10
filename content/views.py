from django.shortcuts import render, redirect
from .models import Title,Entry
from .forms import TitleForm,EntryForm

def index(request):
    """home page"""
    return render(request, 'content/index.html')

def titles(request):
    titles =Title.objects.order_by('date_added')
    context = {'titles':titles}
    return render(request,'content/titles.html',context)

def book(request,title_id):
    title = Title.objects.get(id=title_id)
    entries = title.entry_set.order_by('-date_added')
    context = {'title':title,'entries':entries}
    return render(request, 'content/book.html',context)

def new_book(request):
    if request.method != 'POST':
        form = TitleForm()
    else:
        form = TitleForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('content:titles')
    context = {'form':form}
    return render(request,'content/new_book.html',context)

def new_entry(request,title_id):
    title = Title.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.title = title
            new_entry.save()
            return redirect('content:book',title_id=title_id)

    context = {'title':title,'form':form}
    return render(request,'content/new_entry.html',context)

def edit_title(request, title_id):
    title = Title.objects.get(id=title_id)

    if request.method != "POST":
        form = TitleForm(instance=title)
    else:
        form = TitleForm(instance=title,data=request.POST)
        if form.is_valid():
            form.dave()
            return redirect('content:book',title_id=title.id)

    context = {'title':title, 'form':form}
    return render(request,'content/edit_title.html',context)

def edit_entry(request,entry_id):
    entry = Entry.objects.get(id=entry_id)
    title = entry.title

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('content:book',title_id=title.id)
    context = {'entry':entry,'title':title,'form':form}
    return render(request,'content.edit_entry.html',context)