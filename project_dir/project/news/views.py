from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import get_object_or_404, redirect, render




from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category


class PostList(ListView):
    model = Post
    template_name = 'flatpages/default.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'news/index.html'
    context_object_name = 'new'

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product',)
    model = Post
    template_name = 'news/index_edit.html'
    form_class = PostForm


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_product',)
    form_class = PostForm
    model = Post
    template_name = 'news/index_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_product',)
    model = Post
    template_name = 'news/index_delete.html'
    success_url = reverse_lazy('Post_list')
    queryset = Post.objects.all()



class ArticleCreate(CreateView):
    model = Post
    template_name = 'news/article_delete.html'
    form_class = PostForm

class ArticleUpdate(UpdateView):
    model = Post
    template_name = 'news/article_delete.html'
    form_class = PostForm

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    form_class = PostForm
    success_url = reverse_lazy('article_list')




class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(ctegory=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    calendar = Category.objects.get(id=pk)
    calendar.subscribers.add(user)

    massage = 'Вы успешно подписались на рассылку'
    return render(request, 'news/subscribe.html', {'category': calendar, 'massage': massage})