from django.conf.urls import url, include
from rest_framework import routers
from ppsus_app import views


# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r'posto', views.PostoViewSet)
router.register(r'paciente', views.PacienteViewSet)
router.register(r'subjetiva', views.SubjetivaViewSet)
router.register(r'edmonton', views.EdmontonViewSet)
router.register(r'users', views.UserViewSet)
#router.register(r'avaliacoes', views.AvaliacaoView, base_name='avaliacoes/$')


# The API URLs are now determined automatically by the router.
urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^avaliacoes/(?P<id_paciente>[0-9]+)/$', views.AvaliacaoView.as_view()),
	url(r'^busca/(?P<n_sus>[0-9]+)/$', views.GetPacienteView.as_view()),
]