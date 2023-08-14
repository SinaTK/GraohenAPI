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
    

class PersonInput(graphene.InputObjectType):
    name = graphene.String()
    age = graphene.Int()


class CarInput(graphene.InputObjectType):
    persons_id = graphene.List(graphene.ID)
    model = graphene.String()
    year = graphene.Int()


class CreatePerson(graphene.Mutation):
    class Arguments:
        input = PersonInput(required=True)

    person = graphene.Field(PersonType)
    ok = graphene.Boolean(default_value=False)

    def mutate(root, info, input=None):
        person = Person.objects.create(name=input.name, age=input.age)
        ok = True
        return CreatePerson(person=person, ok=ok)
    

class UpdatePerson(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PersonInput()
    
    person = graphene.Field(PersonType)
    ok = graphene.Boolean(default_value=False)

    def mutate(root, info, id, input):
        person_instance = get_object_or_404(Person, id=id)
        if input.name is not None:
            person_instance.name = input.name
        if input.age is not None:
            person_instance.age = input.age
        person_instance.save()
        ok = True
        return UpdatePerson(person=person_instance, ok=ok)


class DeletePerson(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    person = graphene.Field(PersonType)
    ok = graphene.Boolean(default_value=False)

    def mutate(root, info, id):
        peron_instance = get_object_or_404(Person, id=id)
        peron_instance.delete()
        ok = True
        return DeletePerson(person=peron_instance, ok=ok)


class CreateCar(graphene.Mutation):
    class Arguments:
        input = CarInput()

    car = graphene.Field(CarType)
    ok = graphene.Boolean(default_value = False)
    
    def mutate(root, info, input=None):
        persons_list = []
        for person_id in input.persons_id:
            person_instance = get_object_or_404(Person, id=person_id)
            persons_list.append(person_instance)
        
        car_instance = Car.objects.create(model=input.model, year=input.year)
        car_instance.owner.set(persons_list)
        ok = True
        return CreateCar(car=car_instance, ok=ok)


class HomeMutation(graphene.ObjectType):
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()
    delete_person = DeletePerson.Field()
    create_car = CreateCar.Field()