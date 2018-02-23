from django.conf.urls import url, include
from rest_framework import routers
from ppsus_app import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token


# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r'posto', views.PostoViewSet)
router.register(r'paciente', views.PacienteViewSet)
router.register(r'subjetiva', views.SubjetivaViewSet)
router.register(r'edmonton', views.EdmontonViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'upload', views.DocumentViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^avaliacoes/(?P<id_paciente>[0-9]+)/$', views.AvaliacaoView.as_view()),
	url(r'^busca/(?P<n_sus>[0-9]+)/$', views.GetPacienteView.as_view()),
	url(r'^uploads/[0-9]+/[0-9]+/[0-9]+/$', views.DocumentViewSet),
	

	url(r'^api-token-auth/', obtain_jwt_token),
	url(r'^api-token-refresh/', refresh_jwt_token),

]