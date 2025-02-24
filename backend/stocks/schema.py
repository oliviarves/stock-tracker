import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Stock, Sector, Tag, StockList


# Types
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


# Stock Mutations
class CreateStockMutation(graphene.Mutation):
    class Arguments:
        symbol = graphene.String(required=True)
        name = graphene.String(required=True)
        sector_id = graphene.ID()

    stock = graphene.Field(StockType)

    @classmethod
    def mutate(cls, root, info, symbol, name, sector_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        sector = None
        if sector_id:
            try:
                sector = Sector.objects.get(pk=sector_id)
            except Sector.DoesNotExist:
                raise GraphQLError(f"Sector with ID {sector_id} does not exist")

        stock = Stock(symbol=symbol, name=name, sector=sector)
        stock.save()

        return CreateStockMutation(stock=stock)


class UpdateStockMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        symbol = graphene.String()
        name = graphene.String()
        sector_id = graphene.ID()

    stock = graphene.Field(StockType)

    @classmethod
    def mutate(cls, root, info, id, symbol=None, name=None, sector_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            stock = Stock.objects.get(pk=id)
        except Stock.DoesNotExist:
            raise GraphQLError(f"Stock with ID {id} does not exist")

        if symbol:
            stock.symbol = symbol
        if name:
            stock.name = name

        if sector_id:
            try:
                stock.sector = Sector.objects.get(pk=sector_id)
            except Sector.DoesNotExist:
                raise GraphQLError(f"Sector with ID {sector_id} does not exist")

        stock.save()
        return UpdateStockMutation(stock=stock)


class DeleteStockMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            stock = Stock.objects.get(pk=id)
            stock.delete()
            return DeleteStockMutation(success=True)
        except Stock.DoesNotExist:
            raise GraphQLError(f"Stock with ID {id} does not exist")


# Sector Mutations
class CreateSectorMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    sector = graphene.Field(SectorType)

    @classmethod
    def mutate(cls, root, info, name, description=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        sector = Sector(name=name, description=description)
        sector.save()

        return CreateSectorMutation(sector=sector)


class UpdateSectorMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()

    sector = graphene.Field(SectorType)

    @classmethod
    def mutate(cls, root, info, id, name=None, description=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            sector = Sector.objects.get(pk=id)
        except Sector.DoesNotExist:
            raise GraphQLError(f"Sector with ID {id} does not exist")

        if name:
            sector.name = name
        if description is not None:
            sector.description = description

        sector.save()
        return UpdateSectorMutation(sector=sector)


class DeleteSectorMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            sector = Sector.objects.get(pk=id)
            sector.delete()
            return DeleteSectorMutation(success=True)
        except Sector.DoesNotExist:
            raise GraphQLError(f"Sector with ID {id} does not exist")


# Tag Mutations
class CreateTagMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        stock_ids = graphene.List(graphene.ID)

    tag = graphene.Field(TagType)

    @classmethod
    def mutate(cls, root, info, name, stock_ids=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        tag = Tag.objects.create(name=name)

        if stock_ids:
            stocks = []
            for stock_id in stock_ids:
                try:
                    stock = Stock.objects.get(pk=stock_id)
                    stocks.append(stock)
                except Stock.DoesNotExist:
                    raise GraphQLError(f"Stock with ID {stock_id} does not exist")

            tag.stocks.set(stocks)

        return CreateTagMutation(tag=tag)


class UpdateTagMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        stock_ids = graphene.List(graphene.ID)

    tag = graphene.Field(TagType)

    @classmethod
    def mutate(cls, root, info, id, name=None, stock_ids=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            tag = Tag.objects.get(pk=id)
        except Tag.DoesNotExist:
            raise GraphQLError(f"Tag with ID {id} does not exist")

        if name:
            tag.name = name
            tag.save()

        if stock_ids is not None:
            stocks = []
            for stock_id in stock_ids:
                try:
                    stock = Stock.objects.get(pk=stock_id)
                    stocks.append(stock)
                except Stock.DoesNotExist:
                    raise GraphQLError(f"Stock with ID {stock_id} does not exist")

            tag.stocks.set(stocks)

        return UpdateTagMutation(tag=tag)


class DeleteTagMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            tag = Tag.objects.get(pk=id)
            tag.delete()
            return DeleteTagMutation(success=True)
        except Tag.DoesNotExist:
            raise GraphQLError(f"Tag with ID {id} does not exist")


# StockList Mutations
class CreateStockListMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        stock_ids = graphene.List(graphene.ID)

    stock_list = graphene.Field(StockListType)

    @classmethod
    def mutate(cls, root, info, name, stock_ids=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        stock_list = StockList.objects.create(name=name, user=info.context.user)

        if stock_ids:
            stocks = []
            for stock_id in stock_ids:
                try:
                    stock = Stock.objects.get(pk=stock_id)
                    stocks.append(stock)
                except Stock.DoesNotExist:
                    raise GraphQLError(f"Stock with ID {stock_id} does not exist")

            stock_list.stocks.set(stocks)

        return CreateStockListMutation(stock_list=stock_list)


class UpdateStockListMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        stock_ids = graphene.List(graphene.ID)

    stock_list = graphene.Field(StockListType)

    @classmethod
    def mutate(cls, root, info, id, name=None, stock_ids=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            stock_list = StockList.objects.get(pk=id, user=info.context.user)
        except StockList.DoesNotExist:
            raise GraphQLError(f"Stock list with ID {id} does not exist or does not belong to you")

        if name:
            stock_list.name = name
            stock_list.save()

        if stock_ids is not None:
            stocks = []
            for stock_id in stock_ids:
                try:
                    stock = Stock.objects.get(pk=stock_id)
                    stocks.append(stock)
                except Stock.DoesNotExist:
                    raise GraphQLError(f"Stock with ID {stock_id} does not exist")

            stock_list.stocks.set(stocks)

        return UpdateStockListMutation(stock_list=stock_list)


class DeleteStockListMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            stock_list = StockList.objects.get(pk=id, user=info.context.user)
            stock_list.delete()
            return DeleteStockListMutation(success=True)
        except StockList.DoesNotExist:
            raise GraphQLError(f"Stock list with ID {id} does not exist or does not belong to you")


class Query(graphene.ObjectType):
    all_stocks = graphene.List(StockType)
    stock = graphene.Field(StockType, id=graphene.ID(), symbol=graphene.String())

    all_sectors = graphene.List(SectorType)
    sector = graphene.Field(SectorType, id=graphene.ID())

    all_tags = graphene.List(TagType)
    tag = graphene.Field(TagType, id=graphene.ID())

    my_stock_lists = graphene.List(StockListType)
    stock_list = graphene.Field(StockListType, id=graphene.ID())

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

    def resolve_my_stock_lists(self, info):
        if not info.context.user.is_authenticated:
            return StockList.objects.none()
        return StockList.objects.filter(user=info.context.user)

    def resolve_stock_list(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to view stock lists")
        return StockList.objects.get(pk=id, user=info.context.user)


class Mutation(graphene.ObjectType):
    create_stock = CreateStockMutation.Field()
    update_stock = UpdateStockMutation.Field()
    delete_stock = DeleteStockMutation.Field()

    create_sector = CreateSectorMutation.Field()
    update_sector = UpdateSectorMutation.Field()
    delete_sector = DeleteSectorMutation.Field()

    create_tag = CreateTagMutation.Field()
    update_tag = UpdateTagMutation.Field()
    delete_tag = DeleteTagMutation.Field()

    create_stock_list = CreateStockListMutation.Field()
    update_stock_list = UpdateStockListMutation.Field()
    delete_stock_list = DeleteStockListMutation.Field()