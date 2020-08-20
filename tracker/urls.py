from django.urls import path
from tracker import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("forgot/", views.forgot_password, name="forgot_password"),
    path('reset/<uidb64>/<token>', views.reset_password, name='reset_password'),
    path("my_account/", views.my_account, name="my_account"),
    path("my_account/change_email/", views.change_email, name="change_email"),
    path("my_account/change_password/", views.change_password, name="change_password"),
    path("my_account/delete/", views.delete_account, name="delete_account"),
    path("new_game/", views.new_game, name="new_game"),
    path("history/", views.history, name="history"),
    path("history/delete_game", views.delete_game, name="delete_game"),
    path("game/<int:game_id>/<int:timestamp>/", views.game, name="game"),
    path("game/<int:game_id>/<int:timestamp>/edit", views.game_edit, name="game_edit"),
    path("game/<int:game_id>/<int:timestamp>/add_player", views.add_player, name="add_player"),
    path("game/<int:game_id>/<int:timestamp>/delete_player", views.delete_player, name="delete_player"),
    path("game/<int:game_id>/<int:timestamp>/get_scores", views.get_scores, name="get_scores"),
    path("game/<int:game_id>/<int:timestamp>/save_scores", views.save_scores, name="save_scores"),
]