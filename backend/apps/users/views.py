from rest_framework import generics, parsers, permissions

from .serializers import UserSerializer


class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser)
    http_method_names = ("get", "patch", "head", "options")

    def get_object(self):
        return self.request.user
