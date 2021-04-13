from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response


from api.models import IPLocalization, Currency
from api.serializers import CurrencySerializer, IPLocalizationSerializer, RawIPLocalizationSerializer, SearchDBSerializer

# Create your views here.


class CurrencyViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CurrencySerializer


CurrencyDetailedView = CurrencyViewSet.as_view(actions={'get': 'retrieve', 'delete': 'destroy'})
CurrencyListView = CurrencyViewSet.as_view(actions={'get': 'list', 'post': 'create'})


class IPLocalizationViewSet(ModelViewSet):
    queryset = IPLocalization.objects.all()
    permission_classes = [IsAuthenticated, ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer_action_classes = {
            'create': RawIPLocalizationSerializer
        }

    def get_serializer_class(self, *args, **kwargs):
        if self.action in self.serializer_action_classes:
            return self.serializer_action_classes[self.action]
        return IPLocalizationSerializer

    @action(detail=False, methods=['get'])
    def find(self, request):
        serializer = SearchDBSerializer(data=request.GET)
        args = ()
        if serializer.is_valid(raise_exception=True):
            if 'ip' in serializer.data:
                args = (Q(ip__contains=serializer.validated_data['ip']),)
            elif 'url' in serializer.data:
                args = (Q(url__contains=serializer.validated_data['url']),)
            try:  # there must be a better way to do this
                record = self.queryset.filter(*args).select_related('currency')
            except IPLocalization.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            record, many = (record.first(), False) if len(record) < 2 else (record, True)  # same here, this is a behavior I never encountered before

            serializer = self.get_serializer(record, many=many)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        entries = [IPLocalization(**data) for data in serializer.validated_data]
        IPLocalization.objects.bulk_create(entries)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


IPLocalizationListView = IPLocalizationViewSet.as_view(actions={'post': 'create', 'get': 'list'})
IPFindInDBView = IPLocalizationViewSet.as_view(actions={'get': 'find'})
IPLocalizationDetailedView = IPLocalizationViewSet.as_view(actions={'delete': 'destroy', 'get': 'retrieve'})
