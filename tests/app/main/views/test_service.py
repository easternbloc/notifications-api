from flask import json


# from app.models import Service


def test_get_services_view(notify_api):
    # expected = Service(id=1,
    #                    user_id=1,
    #                    name="Service1",
    #                    created_at="01/01/2015",
    #                    active=True,
    #                    limit=100,
    #                    restricted=True)

    resp = notify_api.test_client().get(
        '/services',
        headers={'Authorization': 'NOTIFY USER1234'})

    data = json.loads(resp.get_data())

    assert resp.status_code == 200
    assert len(data['service']) == 5
    assert data['service'][0]['id'] == 1
    assert data['service'][0]['name'] == 'Service1'
