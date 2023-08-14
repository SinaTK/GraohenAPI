from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from graphene_django import DjangoObjectType
import graphene
import graphql_jwt

class UserType(DjangoObjectType):
    class Meta:
        model = User


class AccountsQuery(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_user(root, info, id):
        user = info.context.user
        if user.is_authenticated:
            return get_object_or_404(User, id=id)
        raise Exception('You must log in first')
    

class UserInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean(default_value=False)
    user = graphene.Field(UserType)

    def mutate(root, info, input=None):
        user_instance = User.objects.create_user(input.username, input.email, input.password)
        ok = True
        return CreateUser(user=user_instance, ok=ok)
    

class AccountsMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()