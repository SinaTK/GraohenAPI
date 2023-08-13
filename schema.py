import graphene
from home.shcema import HomeQuery, HomeMutation


class Query(HomeQuery, graphene.ObjectType):
    pass


class Mutation(HomeMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)