from django.contrib import admin
from django.urls import path
from GroupPortal.views import about, index, contacts, dashboard
from forum.views import error, success, create_comment, create_forum, create_poll, create_thread, view_comment_edit_history, view_thread_edit_history, update_category, update_comment, update_forum, update_poll, update_tag, update_thread, vote_comment, vote_poll, vote_thread, add_category, add_tag, confirm_action, confirm_delete, view_poll_results, recent_activity
from authentification.views import register_view, login_view, logout_view
from diary.views import diary_view, add_student, add_subject, add_grade

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('dashboard/', dashboard, name='dashboard'),
    path('error/', error, name='error'),
    path('success/', success, name='success'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    path('create-comment/', create_comment, name='create_comment'),
    path('create-forum/', create_forum, name='create_forum'),
    path('create-poll/', create_poll, name='create_poll'),
    path('create-thread/', create_thread, name='create_thread'),

    path('comment-edit-history/', view_comment_edit_history, name='comment_edit_history'),
    path('thread-edit-history/', view_thread_edit_history, name='thread_edit_history'),
    path('update-category/', update_category, name='update_category'),
    path('update-comment/', update_comment, name='update_comment'),
    path('update-forum/', update_forum, name='update_forum'),
    path('update-poll/', update_poll, name='update_poll'),
    path('update-tag/', update_tag, name='update_tag'),
    path('update-thread/', update_thread, name='update_thread'),

    path('vote-comment/', vote_comment, name='vote_comment'),
    path('vote-poll/', vote_poll, name='vote_poll'),
    path('vote-thread/', vote_thread, name='vote_thread'),

    path('add-category/', add_category, name='add_category'),
    path('add-tag/', add_tag, name='add_tag'),
    path('confirm-action/', confirm_action, name='confirm_action'),
    path('confirm-delete/', confirm_delete, name='confirm_delete'),
    path('poll-results/', view_poll_results, name='poll_results'),
    path('recent/', recent_activity, name='recent_activity'),

    # Diary URLs
    path('diary/', diary_view, name='diary'),
    path('add-student/', add_student, name='add-student'),
    path('add-subject/', add_subject, name='add-subject'),
    path('add-grade/', add_grade, name='add-grade'),
]
