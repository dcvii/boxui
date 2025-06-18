from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import json

from .models import Comment, CommentInteraction


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def karma_interaction(request):
    """API endpoint to handle karma interactions (upvotes/downvotes)"""
    try:
        data = json.loads(request.body)
        comment_id = data.get('comment_id')
        reaction = data.get('reaction')  # 1 for upvote, -1 for downvote
        
        # Validate input
        if not comment_id or reaction not in [1, -1]:
            return JsonResponse({'error': 'Invalid input'}, status=400)
        
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user
        
        # Get or create interaction
        interaction, created = CommentInteraction.objects.get_or_create(
            comment=comment,
            user=user,
            defaults={'reaction': reaction}
        )
        
        # If interaction already exists, update or delete it
        if not created:
            if interaction.reaction == reaction:
                # Same reaction - remove it (toggle off)
                interaction.delete()
                user_reaction = None
            else:
                # Different reaction - update it
                interaction.reaction = reaction
                interaction.save()
                user_reaction = reaction
        else:
            user_reaction = reaction
        
        # Return updated karma score and user's current reaction
        return JsonResponse({
            'success': True,
            'karma_score': comment.karma_score,
            'user_reaction': user_reaction
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_comment_karma(request, comment_id):
    """API endpoint to get current karma score for a comment"""
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        user_reaction = None
        
        if request.user.is_authenticated:
            try:
                interaction = CommentInteraction.objects.get(
                    comment=comment,
                    user=request.user
                )
                user_reaction = interaction.reaction
            except CommentInteraction.DoesNotExist:
                pass
        
        return JsonResponse({
            'karma_score': comment.karma_score,
            'user_reaction': user_reaction
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

