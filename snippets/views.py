from snippets.models import Snippet
from django.contrib.auth.models import User

from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly 

from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'retrieve' actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions.

    Additionally we also provide an extra 'highlight' action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    

