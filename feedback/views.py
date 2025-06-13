from django.shortcuts import render, get_object_or_404, redirect
from .models import Feedback
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Pour afficher des messages de succès/erreur
from django.views import View
from django.core.paginator import Paginator

# Vue pour afficher tous les feedbacks de l'utilisateur connecté
@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.filter(user=request.user)
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})

# Liste de mots inappropriés
BAD_WORDS = ['badword1', 'badword2', 'offensiveword']

# Vue de création d'un feedback
@login_required(login_url='login')

def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        comment = request.POST.get('comment', '').strip()
        rating = request.POST.get('rating', None)

        # Vérification des mots inappropriés dans le commentaire
        if any(bad_word in comment.lower() for bad_word in BAD_WORDS):
            messages.error(request, 'Votre commentaire contient des mots inappropriés.')
            return render(request, 'feedback/feedback_form.html', {'form': form})

        # Validation du commentaire (non vide)
        if not comment:
            messages.error(request, 'Le commentaire ne peut pas être vide.')
            return render(request, 'feedback/feedback_form.html', {'form': form})

        # Validation de la note
        if rating is not None:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError("La note doit être comprise entre 1 et 5.")
            except ValueError as e:
                messages.error(request, f"Erreur dans la note : {str(e)}")
                return render(request, 'feedback/feedback_form.html', {'form': form})

        if form.is_valid():
            # Créer un objet Feedback sans l'enregistrer immédiatement
            feedback = form.save(commit=False)
            feedback.user = request.user  # Associer l'utilisateur connecté
            feedback.comment = comment  # Ajouter le commentaire
            feedback.rating = rating    # Ajouter la note
            feedback.sentiment = feedback.analyze_sentiment()  # Analyse de sentiment
            feedback.save()  # Sauvegarder dans la base de données

            messages.success(request, 'Votre feedback a été créé avec succès!')
            return redirect('all_feedbacks')  # Rediriger vers la page de feedbacks
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_form.html', {'form': form})



# Vue d'édition d'un feedback
@login_required(login_url='login')
def feedback_edit(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    


    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            # Appliquer l'analyse de sentiment après modification du commentaire
            feedback.sentiment = feedback.analyze_sentiment()  # Analyser à nouveau le sentiment

            form.save()  # Sauvegarder le feedback modifié

            messages.success(request, 'Votre feedback a été mis à jour avec succès!')
            return redirect('all_feedbacks')
    else:
        form = FeedbackForm(instance=feedback)
    
    return render(request, 'feedback/feedback_form.html', {'form': form})

# Vue de suppression d'un feedback
@login_required(login_url='login')
def feedback_delete(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    
    # Vérifier que l'utilisateur est le propriétaire du feedback
    if request.user != feedback.user:
        messages.error(request, "Vous ne pouvez pas supprimer ce feedback.")
        return redirect('all_feedbacks')

    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Votre feedback a été supprimé avec succès!')
        return redirect('all_feedbacks')
    
    return render(request, 'feedback/feedback_confirm_delete.html', {'feedback': feedback})

# Vue pour supprimer plusieurs feedbacks
class FeedbackDeleteMultipleView(View):
    def post(self, request, *args, **kwargs):
        feedback_ids = request.POST.getlist('feedback_ids')
        feedbacks = Feedback.objects.filter(id__in=feedback_ids)

        # Vérifier que l'utilisateur est le propriétaire de tous les feedbacks
        if feedbacks.filter(user=request.user).count() != len(feedbacks):
            messages.error(request, "Vous ne pouvez pas supprimer certains de ces feedbacks.")
            return redirect('all_feedbacks')

        feedbacks.delete()
        messages.success(request, 'Les feedbacks sélectionnés ont été supprimés avec succès!')
        return redirect('all_feedbacks')

# Vue de la page d'accueil
def home(request):
    return render(request, 'feedback/home.html')

# Vue pour afficher tous les feedbacks
def all_feedbacks(request):

    feedbacks = Feedback.objects.all()

   # Récupérer le paramètre de tri depuis l'URL
    sentiment_filter = request.GET.get('sentiment', None)

    # Filtrer les feedbacks par sentiment si le paramètre est passé
    if sentiment_filter:
        feedbacks = Feedback.objects.filter(sentiment=sentiment_filter).order_by('-created_at')
    else:
        feedbacks = Feedback.objects.all().order_by('-created_at')  # Afficher tous les feedbacks s'il n'y a pas de filtre

    # Pagination
    paginator = Paginator(feedbacks, 3)  # 3 feedbacks par page
    page_number = request.GET.get('page')  # Récupérer le numéro de la page
    page_obj = paginator.get_page(page_number)  # Obtenir les feedbacks pour la page actuelle

    return render(request, 'feedback/all_feedbacks.html', {'page_obj': page_obj, 'sentiment_filter': sentiment_filter})

# Vue pour la page index
def index(request):
    return render(request, 'feedback/index.html')

# Vue pour afficher une page de remerciement après soumission de feedback
def feedback_thanks(request):
    return render(request, 'feedback/feedback_thanks.html')

from django.db.models import Count

@login_required
def feedback_statistics(request):
    # Calculer le nombre de feedbacks pour chaque type de sentiment
    sentiment_stats = Feedback.objects.values('sentiment').annotate(total=Count('id'))

    # Préparer les données pour l'affichage (triées par type de sentiment)
    stats = {
        'positif': 0,
        'négatif': 0,
        'neutre': 0,
    }
    for item in sentiment_stats:
        stats[item['sentiment']] = item['total']

    return render(request, 'feedback/feedback_statistics.html', {'stats': stats})
