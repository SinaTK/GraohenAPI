import graphene



class Query(graphene.ObjectType):
    hello = graphene.String(default_value = 'Hi beauty!')


schema = graphene.Schema(query=Query)