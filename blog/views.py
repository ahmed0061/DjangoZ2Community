from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User



# not used anymore
def home(request):		
	context={
		'Post':Post.objects.all()
	}
	return render(request, 'blog/home.html', context)

class PostListView(ListView):
	model = Post
	# <app>/<model>_<viewtype>.html
	template_name = 'blog/home.html'
	context_object_name = 'Post'
	ordering = ['-author']
	paginate_by = 5

class UserPostListView(ListView):
	model = Post
	# <app>/<model>_<viewtype>.html
	template_name = 'blog/user_posts.html'
	context_object_name = 'Post'
	
	paginate_by = 5
	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('date_posted')



class PostDetailView(DetailView):
	model = Post
	# <app>/<model>_<viewtype>.html
	template_name = 'blog/post_detail.html'
	context_object_name = 'pt'

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content', 'author']
	template_name = 'blog/post_form.html'

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
	model = Post
	fields = ['title', 'content', 'author']
	template_name = 'blog/post_form.html'
	# restriction : only author can update his posts
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	fields = ['title', 'content', 'author']
	template_name = 'blog/post_confirm_delete.html'
	success_url = '/'
	# restriction : only author can update his posts
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

def about(request):

	return render(request, 'blog/about.html')