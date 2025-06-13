from django.shortcuts import render, get_object_or_404, redirect
from .models import Forum
from .forms import ForumForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.paginator import Paginator


# List all forums
from django.core.paginator import Paginator

def forum_list(request):
    # Default to 'date_creation' if 'sort' is empty
    sort_by = request.GET.get('sort', 'date_creation')  # Default sorting by date
    if not sort_by or sort_by not in ['date_creation', 'upvotes', 'title', 'desc']:  # Validate sort field
        sort_by = 'date_creation'  # Default to 'date_creation' if invalid or empty
    
    forums = Forum.objects.all().order_by(f"-{sort_by}")  # Add '-' for descending
    
    # Paginate the forums list, 2 forums per page
    paginator = Paginator(forums, 2)  # Show 2 forums per page
    page_number = request.GET.get('page')  # Get the current page number from the query string
    page_obj = paginator.get_page(page_number)  # Get the current page object
    
    return render(request, 'forum/forum_list.html', {'page_obj': page_obj, 'sort_by': sort_by})

# # View details of a specific forum
# def forum_detail(request, forum_id):
#     forum = get_object_or_404(Forum, id=forum_id)
#     return render(request, 'forum/forum_detail.html', {'forum': forum})

@login_required
def upvote_forum(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    forum.upvotes += 1  # Augmenter le nombre d'upvotes
    forum.save()
    return redirect('forum:forum_list')  # Rediriger vers la liste des forums
# Create a new forum
@login_required(login_url='login')
def forum_create(request):
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum:forum_list')
    else:
        form = ForumForm()
    return render(request, 'forum/forum_form.html', {'form': form})

# Update an existing forum
def forum_update(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    if request.method == 'POST':
        form = ForumForm(request.POST, instance=forum)  # Passer l'instance ici
        if form.is_valid():
            form.save()
            return redirect('forum:forum_list')
    else:
        form = ForumForm(instance=forum)  # Passer l'instance ici aussi
    return render(request, 'forum/forum_form.html', {'form': form})

# Delete a forum
def forum_delete(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    if request.method == 'POST':
        forum.delete()
        return redirect('forum:forum_list')  # Adjust the URL name as needed
    return render(request, 'forum/forum_confirm_delete.html', {'forum': forum})
def home(request):
    return render(request, 'home.html') 


from .models import Forum, Comment
from .forms import CommentForm



# Liste de mots inappropriés
INAPPROPRIATE_WORDS = ['mot1', 'mot2', 'mot3']  # Remplacez par les mots à filtrer

def contains_inappropriate_words(text):
    """Vérifie si le texte contient des mots inappropriés."""
    for word in INAPPROPRIATE_WORDS:
        if word.lower() in text.lower():
            return True
    return False
def forum_detail(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)

    # Récupérer tous les commentaires racine (sans parent_comment)
    comments = forum.comments.filter(parent_comment__isnull=True)

     # Gérer l'ajout d'un commentaire
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.forum = forum
            comment.user = request.user

            # Vérification des mots inappropriés
            if contains_inappropriate_words(comment.content):
                messages.error(request, "Votre commentaire contient des mots inappropriés.")
                return redirect('forum:forum_details1', forum_id=forum.id)

            # Vérifiez si c'est une réponse à un autre commentaire
            parent_comment_id = request.POST.get('parent_comment_id')
            if parent_comment_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_comment_id)
                    comment.parent_comment = parent_comment
                except Comment.DoesNotExist:
                    messages.error(request, "Le commentaire parent n'existe pas.")
                    return redirect('forum:forum_details1', forum_id=forum.id)
                        # Sauvegarder le commentaire
            comment.save()
            messages.success(request, "Votre commentaire a été ajouté avec succès.")


    else:
        comment_form = CommentForm()

    return render(request, 'forum/forum_details1.html', {
        'forum': forum,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Vérifier que l'utilisateur est l'auteur
    if comment.user != request.user:
        return redirect('forum:forum_details1', forum_id=comment.forum.id)

    if request.method == "POST":
        comment.delete()
        return redirect('forum:forum_details1', forum_id=comment.forum.id)

    return render(request, 'forum/onfirm_delete_comment.html', {'comment': comment})
from django.http import JsonResponse
from .models import Comment



from .forms import ResponseForm
@login_required






def reply_to_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.comment = parent_comment
            response.user = request.user
            response.save()
            messages.success(request, "Votre réponse a bien été ajoutée.")
            return redirect('forum:forum_details1', forum_id=parent_comment.forum.id)
        else:
            messages.error(request, "Il y a eu un problème avec votre réponse.")
    else:
        form = ResponseForm()

    return render(request, 'forum/reply_to_comment.html', {
        'form': form,
        'parent_comment': parent_comment
    })

from .models import Comment, Response
def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    if response.user == request.user:
        response.delete()  # Supprime la réponse
    return redirect('forum:forum_detail', forum_id=response.comment.forum.id)






