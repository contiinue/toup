from rest_framework import serializers


class VacancyWorkerSerializer(serializers.Serializer):
    do_choice = (("start", "Start Worker"), ("stop", "Stop Worker"))
    do = serializers.ChoiceField(choices=do_choice)
    interval = serializers.IntegerField(required=False)
