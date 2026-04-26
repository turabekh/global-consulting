from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from .models import Application, Document
from .serializers import (
    ApplicationCreateSerializer,
    ApplicationDetailSerializer,
    ApplicationListSerializer,
    DocumentSerializer,
)


class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    lookup_field = "reference"
    http_method_names = ("get", "post", "patch", "delete", "head", "options")

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).prefetch_related("documents")

    def get_serializer_class(self):
        if self.action == "list":
            return ApplicationListSerializer
        if self.action == "create":
            return ApplicationCreateSerializer
        return ApplicationDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(
            user=request.user,
            status=Application.Status.DRAFT,
            current_step=1,
        )
        out = ApplicationDetailSerializer(instance, context={"request": request})
        return Response(out.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.status != Application.Status.DRAFT:
            raise serializers_validation_error("Cannot edit a submitted application.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.status != Application.Status.DRAFT:
            raise serializers_validation_error("Cannot delete a submitted application.")
        instance.delete()

    @action(detail=True, methods=["post"])
    def submit(self, request, reference=None):
        application = self.get_object()
        if application.status != Application.Status.DRAFT:
            return Response(
                {"detail": "Application is not a draft."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        application.status = Application.Status.SUBMITTED
        application.submitted_at = timezone.now()
        application.save(update_fields=["status", "submitted_at", "updated_at"])
        serializer = ApplicationDetailSerializer(application, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="documents")
    def upload_document(self, request, reference=None):
        application = self.get_object()
        if application.status not in (
            Application.Status.DRAFT,
            Application.Status.SUBMITTED,
            Application.Status.NEEDS_INFO,
            Application.Status.IN_REVIEW,
        ):
            return Response(
                {"detail": "Cannot attach documents at this stage."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        upload = request.FILES.get("file")
        if not upload:
            return Response(
                {"file": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST
            )

        kind = request.data.get("kind", Document.Kind.OTHER)

        document = Document.objects.create(
            application=application,
            kind=kind,
            file=upload,
            original_filename=upload.name[:255],
            size_bytes=upload.size,
        )
        serializer = DocumentSerializer(document, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path=r"documents/(?P<doc_id>\d+)")
    def remove_document(self, request, reference=None, doc_id=None):
        application = self.get_object()
        if application.status != Application.Status.DRAFT:
            return Response(
                {"detail": "Documents can only be removed from drafts."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            document = application.documents.get(id=doc_id)
        except Document.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def serializers_validation_error(message: str):
    from rest_framework import serializers

    return serializers.ValidationError(message)
