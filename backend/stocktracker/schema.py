import graphene
import graphql_jwt
import stocks.schema
import analysis.schema
import users.schema

class Query(stocks.schema.Query, analysis.schema.Query, users.schema.Query, graphene.ObjectType):
    pass

class Mutation(stocks.schema.Mutation, analysis.schema.Mutation, users.schema.Mutation, graphene.ObjectType):
    # JWT Authentication
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)