from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import CommentForm
from product.models import Estate, Favorite, Category
from .models import Comment




def estate_detail_view(request, pk):
    estate = get_object_or_404(Estate, pk=pk)
    comments = estate.comments.order_by('-created_at')
    recommendations = Estate.objects.filter(
        category=estate.category
    ).exclude(pk=estate.pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.estate = estate
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен')
            return redirect('estate_detail', pk=estate.pk)
    else:
        form = CommentForm()

    return render(request, 'main/estate_detail.html', {
        'estate': estate,
        'comments': comments,
        'form': form,
        'recommendations': recommendations
    })

def index_view(request):
    estates = Estate.objects.filter(is_active=True)
    liked_estates = []  # -> [1, 2, 3, 4, 5]
    if request.user.is_authenticated:
        liked_estates = Favorite.objects.filter(user=request.user).values_list('estate_id', flat=True)
    parent_categories = Category.objects.filter(parent_category=None)
    return render(
        request=request,
        template_name='main/index.html',
        context={
            "parent_categories": parent_categories,
            "estates": estates,
            "liked_estates": liked_estates
        }
    )


@login_required
def create_comment_view(request, estate_id):
    estate = get_object_or_404(Estate, id=estate_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(
                estate=estate,
                author=request.user,
                content=comment_text
            )
    return redirect('estate_detail', pk=estate.id)

@login_required
def estate_like_view(request, estate_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Войдите в систему')
        return redirect('index')

    estate = get_object_or_404(Estate, id=estate_id)

    like_exist = Favorite.objects.filter(user=request.user, estate=estate).first()

    if not like_exist:
        like = Favorite(
            user=request.user,
            estate=estate
        )
        like.save()
    else:
        like_exist.delete()

    return redirect('index')


def estate_list_view(request):
    estates = EstateFilter(request.GET, queryset=Estate.objects.filter(is_active=True))

    paginator = Paginator(estates.qs, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request=request,
        template_name='main/estate_list.html',
        context={
            'estates': estates,
            'page_obj': page_obj
        }
    )