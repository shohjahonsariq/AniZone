from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import Q

from .models import Anime, Episode, Comment, AnimeView, Category
from .forms import CommentForm

# Google orqali avtomatik login view
class GoogleAutoLoginView(View):
    def get(self, request):
        next_url = request.GET.get('next', '/')
        return redirect(f'/accounts/google/login/?next={next_url}')

# Profil sahifasi
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    animes = Anime.objects.all()

    if query:
        animes = animes.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if category_id:
        animes = animes.filter(categories__id=category_id)

    categories = Category.objects.all()

    return render(request, 'home.html', {
        'animes': animes,
        'query': query,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })

# Anime tafsiloti sahifasi — endi LIKE va IZOH bilan
@login_required
def anime_detail(request, pk):
    anime = get_object_or_404(Anime, pk=pk)

     # 👁 Faqat birinchi marta ko‘rsa, yozamiz
         # 👁 Faqat birinchi marta ko‘rsa, yozamiz
    seen_key = f'viewed_anime_{anime.pk}'
    if not request.session.get(seen_key, False):
        anime.views += 1
        anime.save(update_fields=['views'])
        request.session[seen_key] = True

    episodes = anime.episodes.all().order_by('episode_number')
    comments = anime.comments.all().order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.anime = anime
            comment.user = request.user
            comment.save()
            return redirect('anime_detail', pk=pk)

    context = {
        'anime': anime,
        'episodes': episodes,
        'form': form,
        'comments': comments,
        'has_liked': request.user in anime.likes.all()
    }
    return render(request, 'anime_detail.html', context)

# Epizod detail sahifasi
@login_required
def episode_detail(request, pk):
    episode = get_object_or_404(Episode, pk=pk)
    return render(request, 'episode_detail.html', {'episode': episode})

# ❤️ Like tugmasi
@login_required
def like_anime(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    if request.user in anime.likes.all():
        anime.likes.remove(request.user)
    else:
        anime.likes.add(request.user)
    return redirect('anime_detail', pk=pk)
