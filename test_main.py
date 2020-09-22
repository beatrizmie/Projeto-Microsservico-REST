from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#MAIN
def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


#CREATE NEW TASK
def test_create_task():
    response = client.post(
        "/tasks/d5c1c91b-3cf3-4694-861c-1f7935f12aa2",
        json={"name": "test", "description": "Testing"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "name": "test",
        "description": "Testing",
        "is_done": False
    }


#READ ALL TASKS
def test_list_all_tasks():
    response = client.get('/tasks/')
    assert response.status_code == 200


#READ ALL DONE OR NOT DONE TASKS
def test_list_all_done_tasks():
    response = client.get(
        '/tasks/list/true'
    )
    assert response.status_code == 200

def test_list_all_not_done_tasks():
    response = client.get(
        '/tasks/list/false'
    )
    assert response.status_code == 200
    

#UPDATE TASK NAME
def test_update_task_name():
    response = client.put(
        '/tasks/d5c1c91b-3cf3-4694-861c-1f7935f12ab2/name?task_name=heyy',
        )
    assert response.status_code == 200
    assert response.json() == {
        "name": "heyy",
        "description": "hello everyone",
        "is_done": False
    }

def test_update_task_name_using_non_existent_task_id():
    response = client.put(
        '/tasks/d5c1c91b-3cf3-4694-861c-1f7935f12aa2/name?task_name=heyy',
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}

def test_update_task_name_using_wrong_type_of_parameter():
    response = client.put(
        '/tasks/string/name?task_name=heyy',
    )
    assert response.status_code == 422
    assert response.json() ==  {
        'detail': [{
            'loc': ['path', 'task_id'], 
            'msg': 'value is not a valid uuid', 
            'type': 'type_error.uuid'
            }
        ]
    }


#UPDATE TASK DESCRIPTION
def test_update_task_description():
    response = client.put(
        '/tasks/d5c1c91b-3cf3-4694-861c-1f7935f12ab3/description?task_description=heyy everybody',
        )
    assert response.status_code == 200
    assert response.json() == {
        "name": "bia",
        "description": "heyy everybody",
        "is_done": False
    }

def test_update_task_description_using_non_existent_task_id():
    response = client.put(
        '/tasks/d5c1c91b-3cf3-4694-861c-1f7935f12aa2/description?task_description=heyy everybody',
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}

def test_update_task_description_using_wrong_type_of_parameter():
    response = client.put(
        '/tasks/string/description?task_description=heyy everybody',
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['path', 'task_id'], 
            'msg': 'value is not a valid uuid', 
            'type': 'type_error.uuid'
            }
        ]
    }


#UPDATE TASK IS DONE
def test_update_task_is_done():
    response = client.put(
        '/tasks/d5c1c91b-3cf3-4694-861c-1f7935f12ab4/is_done'
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "samu",
        "description": "heyy samu",
        "is_done": True
    }

def test_update_task_is_not_done():
    response = client.put(
        '/tasks/d5c1c91b-3cf3-4694-861c-1f7935f12ab5/is_done'
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "samu",
        "description": "heyy samu",
        "is_done": False
    }

def test_update_task_is_done_using_non_existing_task_id():
    response = client.put(
        '/tasks/d5c1c91b-3cf3-4694-861c-1f7935f12aa2/is_done'
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}

def test_update_task_is_done_using_wrong_type_of_parameter():
    response = client.put(
        '/tasks/true/is_done'
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['path', 'task_id'],
            'msg': 'value is not a valid uuid',
            'type': 'type_error.uuid'
            }
        ]
    }


#DELETE TASK
def test_delete_task():
    response = client.delete(
        '/tasks/d5c1c91b-3cf3-4694-861c-1f7935f12ab5'
    )
    assert response.status_code == 200

def test_delete_task_using_non_existing_id():
    response = client.delete(
        '/tasks/d5c1c91b-3cf3-4694-861c-1f7935f12aa5'
    )
    assert response.status_code == 404

def test_delete_task_using_wrong_type_of_parameter():
    response = client.delete(
        '/tasks/string'
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['path', 'task_id'],
            'msg': 'value is not a valid uuid',
            'type': 'type_error.uuid'
            }
        ]
    }