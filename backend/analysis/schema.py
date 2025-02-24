import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import (
    StockImage, StockNote, StockEvaluation,
    SectorImage, SectorNote, SectorEvaluation
)
from stocks.models import Stock, Sector
from graphene_file_upload.scalars import Upload


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


# Stock Note Mutations
class CreateStockNoteMutation(graphene.Mutation):
    class Arguments:
        stock_id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String(required=True)

    note = graphene.Field(StockNoteType)

    @classmethod
    def mutate(cls, root, info, stock_id, content, title=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            stock = Stock.objects.get(pk=stock_id)
        except Stock.DoesNotExist:
            raise GraphQLError(f"Stock with ID {stock_id} does not exist")

        note = StockNote(
            stock=stock,
            user=info.context.user,
            title=title,
            content=content
        )
        note.save()

        return CreateStockNoteMutation(note=note)


class UpdateStockNoteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()

    note = graphene.Field(StockNoteType)

    @classmethod
    def mutate(cls, root, info, id, title=None, content=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            note = StockNote.objects.get(pk=id)
        except StockNote.DoesNotExist:
            raise GraphQLError(f"Note with ID {id} does not exist")

        # Check if the note belongs to the current user
        if note.user != info.context.user:
            raise GraphQLError("You can only update your own notes")

        if title is not None:
            note.title = title
        if content is not None:
            note.content = content

        note.save()
        return UpdateStockNoteMutation(note=note)


class DeleteStockNoteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            note = StockNote.objects.get(pk=id)

            # Check if the note belongs to the current user
            if note.user != info.context.user:
                raise GraphQLError("You can only delete your own notes")

            note.delete()
            return DeleteStockNoteMutation(success=True)
        except StockNote.DoesNotExist:
            raise GraphQLError(f"Note with ID {id} does not exist")


# Stock Evaluation Mutations
class CreateStockEvaluationMutation(graphene.Mutation):
    class Arguments:
        stock_id = graphene.ID(required=True)
        rating = graphene.Int(required=True)
        notes = graphene.String()

    evaluation = graphene.Field(StockEvaluationType)

    @classmethod
    def mutate(cls, root, info, stock_id, rating, notes=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        if rating < 1 or rating > 5:
            raise GraphQLError("Rating must be between 1 and 5")

        try:
            stock = Stock.objects.get(pk=stock_id)
        except Stock.DoesNotExist:
            raise GraphQLError(f"Stock with ID {stock_id} does not exist")

        # Check if user already has an evaluation of this type for this stock
        existing = StockEvaluation.objects.filter(
            stock=stock,
            user=info.context.user
        ).first()

        if existing:
            # Update existing evaluation
            existing.rating = rating
            existing.notes = notes
            existing.save()
            return CreateStockEvaluationMutation(evaluation=existing)

        # Create new evaluation
        evaluation = StockEvaluation(
            stock=stock,
            user=info.context.user,
            rating=rating,
            notes=notes
        )
        evaluation.save()

        return CreateStockEvaluationMutation(evaluation=evaluation)


class UpdateStockEvaluationMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        rating = graphene.Int()
        notes = graphene.String()

    evaluation = graphene.Field(StockEvaluationType)

    @classmethod
    def mutate(cls, root, info, id, rating=None, notes=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            evaluation = StockEvaluation.objects.get(pk=id)
        except StockEvaluation.DoesNotExist:
            raise GraphQLError(f"Evaluation with ID {id} does not exist")

        # Check if the evaluation belongs to the current user
        if evaluation.user != info.context.user:
            raise GraphQLError("You can only update your own evaluations")

        if rating is not None:
            if rating < 1 or rating > 5:
                raise GraphQLError("Rating must be between 1 and 5")
            evaluation.rating = rating

        if notes is not None:
            evaluation.notes = notes

        evaluation.save()
        return UpdateStockEvaluationMutation(evaluation=evaluation)


class DeleteStockEvaluationMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            evaluation = StockEvaluation.objects.get(pk=id)

            # Check if the evaluation belongs to the current user
            if evaluation.user != info.context.user:
                raise GraphQLError("You can only delete your own evaluations")

            evaluation.delete()
            return DeleteStockEvaluationMutation(success=True)
        except StockEvaluation.DoesNotExist:
            raise GraphQLError(f"Evaluation with ID {id} does not exist")


# Similar mutations for Sector Notes and Evaluations
class CreateSectorNoteMutation(graphene.Mutation):
    class Arguments:
        sector_id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String(required=True)

    note = graphene.Field(SectorNoteType)

    @classmethod
    def mutate(cls, root, info, sector_id, content, title=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            sector = Sector.objects.get(pk=sector_id)
        except Sector.DoesNotExist:
            raise GraphQLError(f"Sector with ID {sector_id} does not exist")

        note = SectorNote(
            sector=sector,
            user=info.context.user,
            title=title,
            content=content
        )
        note.save()

        return CreateSectorNoteMutation(note=note)


class UpdateSectorNoteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()

    note = graphene.Field(SectorNoteType)

    @classmethod
    def mutate(cls, root, info, id, title=None, content=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            note = SectorNote.objects.get(pk=id)
        except SectorNote.DoesNotExist:
            raise GraphQLError(f"Note with ID {id} does not exist")

        # Check if the note belongs to the current user
        if note.user != info.context.user:
            raise GraphQLError("You can only update your own notes")

        if title is not None:
            note.title = title
        if content is not None:
            note.content = content

        note.save()
        return UpdateSectorNoteMutation(note=note)


class DeleteSectorNoteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        try:
            note = SectorNote.objects.get(pk=id)

            # Check if the note belongs to the current user
            if note.user != info.context.user:
                raise GraphQLError("You can only delete your own notes")

            note.delete()
            return DeleteSectorNoteMutation(success=True)
        except SectorNote.DoesNotExist:
            raise GraphQLError(f"Note with ID {id} does not exist")


class CreateSectorEvaluationMutation(graphene.Mutation):
    class Arguments:
        sector_id = graphene.ID(required=True)
        rating = graphene.Int(required=True)
        evaluation_type = graphene.String(required=True)
        notes = graphene.String()

    evaluation = graphene.Field(SectorEvaluationType)

    @classmethod
    def mutate(cls, root, info, sector_id, rating, notes=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action")

        if rating < 1 or rating > 5:
            raise GraphQLError("Rating must be between 1 and 5")

        try:
            sector = Sector.objects.get(pk=sector_id)
        except Sector.DoesNotExist:
            raise GraphQLError(f"Sector with ID {sector_id} does not exist")

        # Check if user already has an evaluation of this type for this sector
        existing = SectorEvaluation.objects.filter(
            sector=sector,
            user=info.context.user
        ).first()

        if existing:
            # Update existing evaluation
            existing.rating = rating
            existing.notes = notes
            existing.save()
            return CreateSectorEvaluationMutation(evaluation=existing)

        # Create new evaluation
        evaluation = SectorEvaluation(
            sector=sector,
            user=info.context.user,
            rating=rating,
            notes=notes
        )
        evaluation.save()

        return CreateSectorEvaluationMutation(evaluation=evaluation)

class UploadStockImageMutation(graphene.Mutation):
    class Arguments:
        stock_id = graphene.ID(required=True)
        image = Upload(required=True)
        title = graphene.String()
        description = graphene.String()
        timeframe = graphene.String()
        analysis_type = graphene.String()

    success = graphene.Boolean()
    stock_image = graphene.Field(StockImageType)

    @classmethod
    def mutate(cls, root, info, stock_id, image, title=None, description=None,
               timeframe=None, analysis_type=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to upload images")

        try:
            stock = Stock.objects.get(pk=stock_id)
        except Stock.DoesNotExist:
            raise GraphQLError(f"Stock with ID {stock_id} does not exist")

        stock_image = StockImage(
            stock=stock,
            user=info.context.user,
            title=title,
            description=description,
            timeframe=timeframe,
            analysis_type=analysis_type,
            image=image
        )
        stock_image.save()

        return UploadStockImageMutation(success=True, stock_image=stock_image)

class UploadSectorImageMutation(graphene.Mutation):
    class Arguments:
        sector_id = graphene.ID(required=True)
        image = Upload(required=True)
        title = graphene.String()
        description = graphene.String()
        analysis_type = graphene.String()

    success = graphene.Boolean()
    sector_image = graphene.Field(SectorImageType)

    @classmethod
    def mutate(cls, root, info, sector_id, image, title=None, description=None, analysis_type=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to upload images")

        try:
            sector = Sector.objects.get(pk=sector_id)
        except Sector.DoesNotExist:
            raise GraphQLError(f"Sector with ID {sector_id} does not exist")

        sector_image = SectorImage(
            sector=sector,
            user=info.context.user,
            title=title,
            description=description,
            analysis_type=analysis_type,
            image=image
        )
        sector_image.save()

        return UploadSectorImageMutation(success=True, sector_image=sector_image)


class Query(graphene.ObjectType):
    # Stock images with filtering
    stock_images = graphene.List(
        StockImageType,
        stock_id=graphene.ID(),
        user_id=graphene.ID()
    )

    # Stock notes with filtering
    stock_notes = graphene.List(
        StockNoteType,
        stock_id=graphene.ID(),
        user_id=graphene.ID()
    )

    # Stock evaluations with filtering
    stock_evaluations = graphene.List(
        StockEvaluationType,
        stock_id=graphene.ID(),
        user_id=graphene.ID()
    )

    # Sector images with filtering
    sector_images = graphene.List(
        SectorImageType,
        sector_id=graphene.ID(),
        user_id=graphene.ID()
    )

    # Sector notes with filtering
    sector_notes = graphene.List(
        SectorNoteType,
        sector_id=graphene.ID(),
        user_id=graphene.ID()
    )

    # Sector evaluations with filtering
    sector_evaluations = graphene.List(
        SectorEvaluationType,
        sector_id=graphene.ID(),
        user_id=graphene.ID()
    )

    # Resolver methods
    def resolve_stock_images(self, info, stock_id=None, user_id=None):
        query = StockImage.objects.all()

        if stock_id:
            query = query.filter(stock_id=stock_id)

        if user_id:
            query = query.filter(user_id=user_id)

        return query

    def resolve_stock_notes(self, info, stock_id=None, user_id=None):
        query = StockNote.objects.all()

        if stock_id:
            query = query.filter(stock_id=stock_id)

        if user_id:
            query = query.filter(user_id=user_id)

        return query

    def resolve_stock_evaluations(self, info, stock_id=None, user_id=None):
        query = StockEvaluation.objects.all()

        if stock_id:
            query = query.filter(stock_id=stock_id)

        if user_id:
            query = query.filter(user_id=user_id)

        return query

    def resolve_sector_images(self, info, sector_id=None, user_id=None):
        query = SectorImage.objects.all()

        if sector_id:
            query = query.filter(sector_id=sector_id)

        if user_id:
            query = query.filter(user_id=user_id)

        return query

    def resolve_sector_notes(self, info, sector_id=None, user_id=None):
        query = SectorNote.objects.all()

        if sector_id:
            query = query.filter(sector_id=sector_id)

        if user_id:
            query = query.filter(user_id=user_id)

        return query

    def resolve_sector_evaluations(self, info, sector_id=None, user_id=None):
        query = SectorEvaluation.objects.all()

        if sector_id:
            query = query.filter(sector_id=sector_id)

        if user_id:
            query = query.filter(user_id=user_id)

        return query


class Mutation(graphene.ObjectType):
    create_stock_note = CreateStockNoteMutation.Field()
    update_stock_note = UpdateStockNoteMutation.Field()
    delete_stock_note = DeleteStockNoteMutation.Field()

    create_stock_evaluation = CreateStockEvaluationMutation.Field()
    update_stock_evaluation = UpdateStockEvaluationMutation.Field()
    delete_stock_evaluation = DeleteStockEvaluationMutation.Field()

    create_sector_note = CreateSectorNoteMutation.Field()
    update_sector_note = UpdateSectorNoteMutation.Field()
    delete_sector_note = DeleteSectorNoteMutation.Field()

    create_sector_evaluation = CreateSectorEvaluationMutation.Field()

    upload_stock_image = UploadStockImageMutation.Field()
    upload_sector_image = UploadSectorImageMutation.Field()
