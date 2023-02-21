from django.shortcuts import render, redirect
from .models import Title,Entry
from .forms import TitleForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


# <---- Below help manage database ---->
def sort_material(request):
    public_display_titles = []
    user_titles = Title.objects.filter(owner=request.user).order_by('date_added')
    user_private_titles = Title.objects.filter(owner=request.user, public=False)
    public_titles = Title.objects.filter(public=True).order_by('date_added')
    for title in public_titles:
        if title not in user_titles:
            public_display_titles.append(title)

    return user_titles, public_display_titles, user_private_titles

def title_expression(title,public_display_titles,user_titles, user_private_titles):
    if title in public_display_titles:
        read_only = True
        user_exp = '--(Read Only)--'
        return read_only,user_exp
    elif title in user_titles:
        if title not in user_private_titles:
            read_only = False
            user_exp = '--(Yourself【public】)--'
            return read_only, user_exp
        else:
            read_only = False
            user_exp = '--(Yourself【private】)--'
            return read_only, user_exp
    elif title not in private_titles or public_display_titles:
        raise Http404
# <---- Above help manage database ---->


def index(request):
    """home page"""
    return render(request, 'content/index.html')

@login_required
def titles(request):
    user_titles, public_display_titles, user_private_titles = sort_material(request)


    context = {'public_display_titles':public_display_titles,'user_titles':user_titles,}
    return render(request,'content/titles.html',context)

@login_required
def book(request,title_id):
    user_titles, public_display_titles, user_private_titles = sort_material(request)

    title = Title.objects.get(id=title_id)

    read_only, user_exp = title_expression(title,public_display_titles,user_titles,user_private_titles)

    is_favorite = False
    if title.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    entries = title.entry_set.order_by('-date_added')
    context = {'title':title,'entries':entries,'user_exp':user_exp,'read_only':read_only,'is_favorite':is_favorite,
               'title.id':title.id}
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

@login_required
def add_or_remove_favorite(request, title_id):

    title = Title.objects.get(id=title_id)

    if title.favorite.filter(id=request.user.id).exists():
        title.favorite.remove(request.user)

    else:
        title.favorite.add(request.user)
    return redirect('content:book', title_id=title.id)

@login_required
def my_favorite(request):
    user = request.user
    my_favorite = user.favorite.all()

    context = {'my_favorite':my_favorite}
    return render(request, 'content/my_favorite.html', context)

class Search(LoginRequiredMixin,ListView):
    model = Title
    template_name = 'content/search.html'
    context_object_name = 'search_result_title'

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        query = self.request.GET.get('search')

        if query:
            search_result_title = qs.filter(text__icontains=query).filter(Q(owner=user)|Q(public=True)).distinct()
            return search_result_title
        else:
            return None



