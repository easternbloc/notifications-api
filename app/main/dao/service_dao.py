from app.models import Service


def add_service(service):
    print("New service added")


def retrieve_all_services():
    services = list()

    services.append(Service(id=1,
                            user_id=1,
                            name="Service1",
                            created_at="01/01/2015",
                            active=True,
                            limit=100,
                            restricted=True))

    services.append(Service(id=2,
                            user_id=2,
                            name="Service2",
                            created_at="01/01/2015",
                            active=True,
                            limit=100,
                            restricted=True))

    services.append(Service(id=3,
                            user_id=3,
                            name="Service3",
                            created_at="01/01/2015",
                            active=True,
                            limit=100,
                            restricted=True))

    services.append(Service(id=4,
                            user_id=4,
                            name="Service4",
                            created_at="01/01/2015",
                            active=True,
                            limit=100,
                            restricted=True))

    services.append(Service(id=5,
                            user_id=5,
                            name="Service5",
                            created_at="01/01/2015",
                            active=True,
                            limit=100,
                            restricted=True))

    return services
