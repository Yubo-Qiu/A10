from django.urls import path
from .views import VoterListView, VoterDetailView
from .views import GraphsView

urlpatterns = [
    path("", VoterListView.as_view(), name="voters"),
    path("graphs/", GraphsView.as_view(), name="graphs"),
    path("voter/<int:pk>/", VoterDetailView.as_view(), name="voter_detail"),
]
