from rest_framework import serializers

from apps.core.markdown import render_markdown

from .models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    answer_html = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ("id", "category", "question", "answer", "answer_html", "order")

    def get_answer_html(self, obj: FAQ) -> str:
        return render_markdown(obj.answer)
