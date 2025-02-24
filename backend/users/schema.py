import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth.models import User
from .models import Profile

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        exclude = ('user',)


class RegisterUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, username, email, password):
        if User.objects.filter(username=username).exists():
            raise GraphQLError("Username already exists")

        if User.objects.filter(email=email).exists():
            raise GraphQLError("Email already exists")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return RegisterUserMutation(user=user)


class UpdateProfileMutation(graphene.Mutation):
    class Arguments:
        bio = graphene.String()
        # Avatar would be handled separately via a REST endpoint

    profile = graphene.Field(ProfileType)

    @classmethod
    def mutate(cls, root, info, bio=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to update your profile")

        user = info.context.user

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)

        if bio is not None:
            profile.bio = bio

        profile.save()
        return UpdateProfileMutation(profile=profile)


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.ID())
    users = graphene.List(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not logged in")
        return user

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)

    def resolve_users(self, info):
        return User.objects.all()


class Mutation(graphene.ObjectType):
    register_user = RegisterUserMutation.Field()
    update_profile = UpdateProfileMutation.Field()