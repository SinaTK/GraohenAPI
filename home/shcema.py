import graphene
from graphene_django import DjangoObjectType
from home.models import Person, Car
from django.shortcuts import get_object_or_404


class PersonType(DjangoObjectType):
    class Meta:
        model = Person


class CarType(DjangoObjectType):
    class Meta:
        model = Car

class  HomeQuery(graphene.ObjectType):
    persons = graphene.List(PersonType)
    cars = graphene.List(CarType)
    person = graphene.Field(PersonType, id=graphene.Int())
    car = graphene.Field(CarType, model=graphene.String())


    def resolve_persons(root, info, **kwargs):
        return Person.objects.all()
    
    def resolve_cars(root, info, **kwargs):
        return Car.objects.all()
    
    def resolve_person(root, info, **kwargs):
        id = kwargs.get('id')
        return get_object_or_404(Person, id=id)
            
    def resolve_car(root, info, **kwargs):
        model = kwargs.get('model')
        return get_object_or_404(Car, model=model)