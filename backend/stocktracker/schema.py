import graphene
from graphene_django import DjangoObjectType
from stocks.models import Stock, Sector, Tag, StockList
from analysis.models import (
    StockImage, StockNote, StockEvaluation,
    SectorImage, SectorNote, SectorEvaluation
)
from django.contrib.auth.models import User
from users.models import Profile


# Define types
class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class SectorType(DjangoObjectType):
    class Meta:
        model = Sector


class StockType(DjangoObjectType):
    class Meta:
        model = Stock


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class StockListType(DjangoObjectType):
    class Meta:
        model = StockList


class StockImageType(DjangoObjectType):
    class Meta:
        model = StockImage


class StockNoteType(DjangoObjectType):
    class Meta:
        model = StockNote


class StockEvaluationType(DjangoObjectType):
    class Meta:
        model = StockEvaluation


class SectorImageType(DjangoObjectType):
    class Meta:
        model = SectorImage


class SectorNoteType(DjangoObjectType):
    class Meta:
        model = SectorNote


class SectorEvaluationType(DjangoObjectType):
    class Meta:
        model = SectorEvaluation


# Define Query
class Query(graphene.ObjectType):
    all_stocks = graphene.List(StockType)
    stock = graphene.Field(StockType, id=graphene.ID(), symbol=graphene.String())

    all_sectors = graphene.List(SectorType)
    sector = graphene.Field(SectorType, id=graphene.ID())

    all_tags = graphene.List(TagType)
    tag = graphene.Field(TagType, id=graphene.ID())

    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.ID())

    # TODO: Add more query fields for other models

    def resolve_all_stocks(self, info):
        return Stock.objects.all()

    def resolve_stock(self, info, id=None, symbol=None):
        if id:
            return Stock.objects.get(pk=id)
        if symbol:
            return Stock.objects.get(symbol=symbol)
        return None

    def resolve_all_sectors(self, info):
        return Sector.objects.all()

    def resolve_sector(self, info, id):
        return Sector.objects.get(pk=id)

    def resolve_all_tags(self, info):
        return Tag.objects.all()

    def resolve_tag(self, info, id):
        return Tag.objects.get(pk=id)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            return None
        return user

    def resolve_user(self, info, id):
        if not info.context.user.is_authenticated:
            return None
        return User.objects.get(pk=id)


# Define Schema
schema = graphene.Schema(query=Query)