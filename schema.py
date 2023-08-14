import graphene
from home.shcema import HomeQuery, HomeMutation
from accounts.schema import AccountsQuery, AccountsMutation

class Query(HomeQuery,AccountsQuery, graphene.ObjectType):
    pass


class Mutation(HomeMutation,AccountsMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)