from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from forum.models import Category, Tag, Forum, Thread, ThreadSubscription, SavedThread, ThreadEditHistory, ThreadVote, Comment, CommentEditHistory, CommentVote, Poll, PollOption, PollVote
from forum.forms import CategoryForm, TagForm, ForumForm, ThreadForm, CommentForm, PollForm
from django.db.models import Q
from django.utils.timezone import now, timedelta

#Додати логіку профіля користувача та досягнень

def error(request):
    return render(request, 'error.html', {'message': 'An error occurred.'})

def success(request):
    return render(request, 'success.html', {'message': 'Operation successful.'})

def confirm_action(request):
    return render(request, 'confirm_action.html', {'message': 'Are you sure you want to proceed with this action?'})

def confirm_delete(request):
    return render(request, 'confirm_delete.html', {'message': 'Are you sure you want to delete this item?'})

def recent_activity(request):
    last_week = now() - timedelta(days=7)
    threads = Thread.objects.filter(created_at__gte=last_week).order_by('-created_at')
    comments = Comment.objects.filter(created_at__gte=last_week).order_by('-created_at')
    polls = Poll.objects.filter(created_at__gte=last_week).order_by('-created_at')

    category_id = request.GET.get('category')
    forum_id = request.GET.get('forum')
    tag_id = request.GET.get('tag')

    if category_id:
        threads = threads.filter(category_id=category_id)
        polls = polls.filter(thread__category_id=category_id)
    if forum_id:
        threads = threads.filter(category__forum_id=forum_id)
        polls = polls.filter(thread__category__forum_id=forum_id)
    if tag_id:
        threads = threads.filter(tags__id=tag_id)
        polls = polls.filter(thread__tags__id=tag_id)

    context = {
        'threads': threads,
        'comments': comments,
        'polls': polls,
        'categories': Category.objects.all(),
        'forums': Forum.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'recent_activity.html', context)
    

# ----- Category Views -----
@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "success.html", {"message": "Category created successfully!"})
    else:
        form = CategoryForm()
    return render(request, "add_category.html", {"form": form})

@login_required
def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return render(request, "success.html", {"message": "Category updated successfully!"})
    else:
        form = CategoryForm(instance=category)
    return render(request, "update_category.html", {"form": form, "category": category})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        category.delete()
        return render(request, "success.html", {"message": "Category deleted successfully!"})
    return render(request, "confirm_delete.html", {"object": category, "type": "category"})

# ----- Tag Views -----
@login_required
def add_tag(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            tag = Tag(name=name)
            tag.save()
            return render(request, "success.html", {"message": "Tag created successfully!"})
        return render(request, "error.html", {"message": "Tag name is required."})
    return render(request, "add_tag.html")

@login_required
def update_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            tag.name = name
            tag.save()
            return render(request, "success.html", {"message": "Tag updated successfully!"})
        return render(request, "error.html", {"message": "Tag name is required."})
    return render(request, "update_tag.html", {"tag": tag})

@login_required
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == "POST":
        tag.delete()
        return render(request, "success.html", {"message": "Tag deleted successfully!"})
    return render(request, "confirm_delete.html", {"object": tag, "type": "tag"})


# ----- Forum Views -----
@login_required
def create_forum(request):
    if request.method == "POST":
        forum_name = request.POST.get("name")
        forum_description = request.POST.get("description")
        
        if forum_name:
            forum = Forum(name=forum_name, description=forum_description)
            forum.save()
            return render(request, "success.html", {"message": "Forum created successfully!"})
        else:
            return render(request, "error.html", {"message": "Forum name is required."})
    
    return render(request, "create_forum.html")

@login_required
def update_forum(request, forum_id):
    try:
        forum = Forum.objects.get(id=forum_id)
    except Forum.DoesNotExist:
        return render(request, "error.html", {"message": "Forum not found."})

    if request.method == "POST":
        forum_name = request.POST.get("name")
        forum_description = request.POST.get("description")

        if forum_name:
            forum.name = forum_name
            forum.description = forum_description
            forum.save()
            return render(request, "success.html", {"message": "Forum updated successfully!"})
        else:
            return render(request, "error.html", {"message": "Forum name is required."})

    return render(request, "update_forum.html", {"forum": forum})

@login_required
def delete_forum(request, forum_id):
    try:
        forum = Forum.objects.get(id=forum_id)
    except Forum.DoesNotExist:
        return render(request, "error.html", {"message": "Forum not found."})

    if request.method == "POST":
        forum.delete()
        return render(request, "success.html", {"message": "Forum deleted successfully!"})

    return render(request, "confirm_delete.html", {"forum": forum})


# ----- Thread Views -----
@login_required
def create_thread(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        tag_ids = request.POST.getlist("tags")
        status = request.POST.get("status", "open")
        attachment = request.FILES.get("attachment")

        if title and description:
            thread = Thread(
                title=title,
                description=description,
                author=request.user,
                category_id=category_id or None,
                status=status,
                attachment=attachment
            )
            thread.save()
            if tag_ids:
                thread.tags.set(tag_ids)
            return render(request, "success.html", {"message": "Thread created successfully!"})
        return render(request, "error.html", {"message": "Title and description are required."})
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, "create_thread.html", {"categories": categories, "tags": tags})

@login_required
def update_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, author=request.user)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        tag_ids = request.POST.getlist("tags")
        status = request.POST.get("status")
        attachment = request.FILES.get("attachment")

        if title and description:
            ThreadEditHistory.objects.create(
                user=request.user,
                thread=thread,
                old_content=thread.description,
                new_content=description
            )
            thread.title = title
            thread.description = description
            thread.category_id = category_id or None
            thread.status = status or thread.status
            if attachment:
                thread.attachment = attachment
            thread.save()
            if tag_ids:
                thread.tags.set(tag_ids)
            else:
                thread.tags.clear()
            return render(request, "success.html", {"message": "Thread updated successfully!"})
        return render(request, "error.html", {"message": "Title and description are required."})
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, "update_thread.html", {"thread": thread, "categories": categories, "tags": tags})

@login_required
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, author=request.user)
    if request.method == "POST":
        thread.is_deleted = True
        thread.save()
        return render(request, "success.html", {"message": "Thread deleted successfully!"})
    return render(request, "confirm_delete.html", {"object": thread, "type": "thread"})

@login_required
def subscribe_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == "POST":
        ThreadSubscription.objects.get_or_create(user=request.user, thread=thread)
        return render(request, "success.html", {"message": "Subscribed to thread!"})
    return render(request, "confirm_action.html", {"object": thread, "action": "subscribe"})

@login_required
def unsubscribe_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == "POST":
        ThreadSubscription.objects.filter(user=request.user, thread=thread).delete()
        return render(request, "success.html", {"message": "Unsubscribed from thread!"})
    return render(request, "confirm_action.html", {"object": thread, "action": "unsubscribe"})

@login_required
def save_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == "POST":
        SavedThread.objects.get_or_create(user=request.user, thread=thread)
        return render(request, "success.html", {"message": "Thread saved!"})
    return render(request, "confirm_action.html", {"object": thread, "action": "save"})

@login_required
def unsave_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == "POST":
        SavedThread.objects.filter(user=request.user, thread=thread).delete()
        return render(request, "success.html", {"message": "Thread unsaved!"})
    return render(request, "confirm_action.html", {"object": thread, "action": "unsave"})

@login_required
def vote_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == "POST":
        vote_type = request.POST.get("vote_type")
        if vote_type in ["up", "down"]:
            ThreadVote.objects.update_or_create(
                user=request.user,
                thread=thread,
                defaults={"vote_type": vote_type}
            )
            return render(request, "success.html", {"message": f"Thread {vote_type}voted!"})
        return render(request, "error.html", {"message": "Invalid vote type."})
    return render(request, "vote_thread.html", {"thread": thread})

def view_thread_edit_history(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    history = ThreadEditHistory.objects.filter(thread=thread).order_by('-edited_at')
    return render(request, "thread_edit_history.html", {"thread": thread, "history": history})


# ----- Comment Views -----
@login_required
def create_comment(request):
    if request.method == "POST":
        thread_id = request.POST.get("thread_id")
        poll_id = request.POST.get("poll_id")
        parent_id = request.POST.get("parent_id")
        content = request.POST.get("content")
        attachment = request.FILES.get("attachment")

        thread = get_object_or_404(Thread, id=thread_id) if thread_id else None
        poll = get_object_or_404(Poll, id=poll_id) if poll_id else None
        parent = get_object_or_404(Comment, id=parent_id) if parent_id else None

        if content and (thread or poll):
            comment = Comment(
                thread=thread,
                poll=poll,
                author=request.user,
                parent=parent,
                content=content,
                attachment=attachment
            )
            comment.save()
            return render(request, "success.html", {"message": "Comment created successfully!"})
        return render(request, "error.html", {"message": "Content is required."})
    threads = Thread.objects.all()
    polls = Poll.objects.all()
    return render(request, "create_comment.html", {"threads": threads, "polls": polls})

@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == "POST":
        content = request.POST.get("content")
        attachment = request.FILES.get("attachment")

        if content:
            CommentEditHistory.objects.create(
                user=request.user,
                comment=comment,
                old_content=comment.content,
                new_content=content
            )
            comment.content = content
            if attachment:
                comment.attachment = attachment
            comment.save()
            return render(request, "success.html", {"message": "Comment updated successfully!"})
        return render(request, "error.html", {"message": "Content is required."})
    return render(request, "update_comment.html", {"comment": comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == "POST":
        comment.is_deleted = True
        comment.save()
        return render(request, "success.html", {"message": "Comment deleted successfully!"})
    return render(request, "confirm_delete.html", {"object": comment, "type": "comment"})

@login_required
def vote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        vote_type = request.POST.get("vote_type")
        if vote_type in ["up", "down"]:
            CommentVote.objects.update_or_create(
                user=request.user,
                comment=comment,
                defaults={"vote_type": vote_type}
            )
            return render(request, "success.html", {"message": f"Comment {vote_type}voted!"})
        return render(request, "error.html", {"message": "Invalid vote type."})
    return render(request, "vote_comment.html", {"comment": comment})

def view_comment_edit_history(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    history = CommentEditHistory.objects.filter(comment=comment).order_by('-edited_at')
    return render(request, "comment_edit_history.html", {"comment": comment, "history": history})


# ----- Poll Views -----
@login_required
def create_poll(request):
    if request.method == "POST":
        thread_id = request.POST.get("thread_id")
        question = request-linking-to-another-sectionrequest.POST.get("question")
        options = request.POST.getlist("options")

        thread = get_object_or_404(Thread, id=thread_id)
        if question and len(options) >= 2:
            poll = Poll(thread=thread, question=question)
            poll.save()
            for option_text in options:
                if option_text.strip():
                    PollOption.objects.create(poll=poll, text=option_text)
            return render(request, "success.html", {"message": "Poll created successfully!"})
        return render(request, "error.html", {"message": "Question and at least two options are required."})
    threads = Thread.objects.all()
    return render(request, "create_poll.html", {"threads": threads})

@login_required
def update_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, thread__author=request.user)
    if request.method == "POST":
        question = request.POST.get("question")
        options = request.POST.getlist("options")

        if question and len(options) >= 2:
            poll.question = question
            poll.save()
            poll.options.all().delete()
            for option_text in options:
                if option_text.strip():
                    PollOption.objects.create(poll=poll, text=option_text)
            return render(request, "success.html", {"message": "Poll updated successfully!"})
        return render(request, "error.html", {"message": "Question and at least two options are required."})
    return render(request, "update_poll.html", {"poll": poll})

@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, thread__author=request.user)
    if request.method == "POST":
        poll.delete()
        return render(request, "success.html", {"message": "Poll deleted successfully!"})
    return render(request, "confirm_delete.html", {"object": poll, "type": "poll"})

@login_required
def vote_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == "POST":
        option_id = request.POST.get("option_id")
        option = get_object_or_404(PollOption, id=option_id, poll=poll)
        PollVote.objects.update_or_create(
            user=request.user,
            option=option
        )
        return render(request, "success.html", {"message": "Poll vote recorded!"})
    return render(request, "vote_poll.html", {"poll": poll})

def view_poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    options = poll.options.all()
    total_votes = PollVote.objects.filter(option__poll=poll).count()
    results = [
        {"option": option, "votes": PollVote.objects.filter(option=option).count()}
        for option in options
    ]
    return render(request, "poll_results.html", {"poll": poll, "results": results, "total_votes": total_votes})

