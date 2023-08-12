import graphene
from home.shcema import HomeQuery


class Query(HomeQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)