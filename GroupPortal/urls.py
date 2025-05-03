from django.contrib import admin
from django.urls import path
from GroupPortal.views import about, index, contacts, dashboard, create   
from forum.views import (
    error, success,
    create_comment, create_forum, create_poll, create_thread,
    view_comment_edit_history, view_thread_edit_history,
    update_category, update_comment, update_forum, update_poll, update_tag, update_thread,
    vote_comment, vote_poll, vote_thread,
    add_category, add_tag, confirm_action, confirm_delete, view_poll_results,
    recent_activity, thread_detail, delete_comment,
    forum_detail, forum_list
)
from authentification.views import register_view, login_view, logout_view
from diary.views import diary_view, add_student, add_subject, add_grade, edit_student, edit_subject, edit_grade

urlpatterns = [
    path('admin/', admin.site.urls),

    # General Views
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('dashboard/', dashboard, name='dashboard'),
    path('error/', error, name='error'),
    path('success/', success, name='success'),
    path('forums/', forum_list, name='forum_list'),  # Added forum list
    path('forum/<int:forum_id>/', forum_detail, name='forum_detail'),  # Added forum detail

    # Authentication Views
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    # Thread Views
    path('thread/<int:thread_id>/', thread_detail, name='thread_detail'),
    path('thread/<int:thread_id>/comment/', create_comment, name='create_comment'),
    path('thread/<int:thread_id>/comment/<int:parent_id>/', create_comment, name='reply_comment'),
    path('thread/<int:thread_id>/edit/', update_thread, name='update_thread'),
    path('thread/<int:thread_id>/history/', view_thread_edit_history, name='thread_edit_history'),
    path('thread/<int:thread_id>/vote/', vote_thread, name='vote_thread'),

    # Comment Views
    path('comment/<int:comment_id>/edit/', update_comment, name='update_comment'),
    path('comment/<int:comment_id>/history/', view_comment_edit_history, name='view_comment_edit_history'),
    path('comment/<int:comment_id>/vote/', vote_comment, name='vote_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),

    # Poll / Forum / Tag / Category Views
    path('create-forum/', create_forum, name='create_forum'),
    path('forum/<int:forum_id>/', forum_detail, name='forum_detail'),
    path('create-poll/', create_poll, name='create_poll'),
    path('create-thread/', create_thread, name='create_thread'),
    path('update-category/<int:category_id>/', update_category, name='update_category'),
    path('update-forum/<int:forum_id>/', update_forum, name='update_forum'),
    path('update-poll/<int:poll_id>/', update_poll, name='update_poll'),
    path('update-tag/<int:tag_id>/', update_tag, name='update_tag'),

    # Other Features
    path('add-category/', add_category, name='add_category'),
    path('add-tag/', add_tag, name='add_tag'),
    path('confirm-action/', confirm_action, name='confirm_action'),
    path('confirm-delete/', confirm_delete, name='confirm_delete'),
    path('poll-results/', view_poll_results, name='poll_results'),
    path('recent/', recent_activity, name='recent_activity'),

    # Diary URLs
    path('diary/', diary_view, name='diary'),
    path('add-student/', add_student, name='add-student'),
    path('edit-student/<int:student_id>/', edit_student, name='edit-student'),
    path('add-subject/', add_subject, name='add-subject'),
    path('edit-subject/<int:subject_id>/', edit_subject, name='edit-subject'),
    path('add-grade/', add_grade, name='add-grade'),
    path('edit-grade/<int:grade_id>/', edit_grade, name='edit-grade'),


    path('confirm-delete/<int:id>/', confirm_delete, name='confirm_delete'),
    path('poll-results/<int:poll_id>/', view_poll_results, name='poll_results'),
    path('recent/', recent_activity, name='recent_activity'),
    path('creaturepanel/', create, name='creaturepanel'),

