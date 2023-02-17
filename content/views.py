from django.shortcuts import render, redirect
from .models import Title,Entry
from .forms import TitleForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """home page"""
    return render(request, 'content/index.html')

def sort_material(request):
    public_display_titles = []
    private_titles = Title.objects.filter(owner=request.user).order_by('date_added')
    public_titles = Title.objects.filter(public=True).order_by('date_added')
    for title in public_titles:
        if title not in private_titles:
            public_display_titles.append(title)

    return private_titles, public_display_titles

@login_required
def titles(request):
    private_titles, public_display_titles = sort_material(request)

    context = {'public_display_titles':public_display_titles,'private_titles':private_titles,}

    return render(request,'content/titles.html',context)

@login_required
def book(request,title_id):
    private_titles, public_display_titles = sort_material(request)

    title = Title.objects.get(id=title_id)
    username = title.owner

    if title in public_display_titles:
        read_only = True
        user_exp = '--(Read Only)'
    elif title in private_titles:
        read_only = False
        user_exp = '--(Yourself)'
    entries = title.entry_set.order_by('-date_added')
    context = {'title':title,'entries':entries,'user_exp':user_exp,'read_only':read_only}
    return render(request, 'content/book.html',context)

@login_required
def new_book(request):
    if request.method != 'POST':
        form = TitleForm()
    else:
        form = TitleForm(data=request.POST)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.owner = request.user
            new_book.save()
            return redirect('content:titles')
    context = {'form':form}
    return render(request,'content/new_book.html',context)

@login_required
def new_entry(request,title_id):
    title = Title.objects.get(id=title_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.owner = request.user
            new_entry.title = title
            new_entry.save()
            return redirect('content:book',title_id=title_id)

    context = {'title':title,'form':form}
    return render(request,'content/new_entry.html',context)

@login_required
def edit_title(request, title_id):
    title = Title.objects.get(id=title_id)
    if title.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = TitleForm(instance=title)
    else:
        form = TitleForm(instance=title,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('content:book',title_id=title.id)

    context = {'title':title, 'form':form}
    return render(request,'content/edit_title.html',context)

@login_required
def edit_entry(request,entry_id):
    entry = Entry.objects.get(id=entry_id)
    title = entry.title
    if title.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('content:book',title_id=title.id)
    context = {'entry':entry,'title':title,'form':form}
    return render(request,'content/edit_entry.html',context)

@login_required
def delete_title(request, title_id):
    title = Title.objects.get(id=title_id)
    if title.owner != request.user:
        raise Http404

    if request.method == 'POST':
        title.delete()
        return redirect('content:titles')

    context = {'title':title}
    return render(request,'content/delete_title.html',context)

@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    title = entry.title
    if title.owner != request.user:
        raise Http404

    if request.method == 'POST':
        entry.delete()
        return redirect('content:book',title_id=title.id)

    context = {'title':title,'entry':entry}
    return render(request,'content/delete_entry.html',context)

class Search(LoginRequiredMixin,ListView):
    model = Title
    template_name = 'content/search.html'
    context_object_name = 'search_result'

    def get_queryset(self):
        search_result = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            return search_result.filter(text__icontains=query)

        return search_result
