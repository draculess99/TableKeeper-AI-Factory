import pytest
import json
import os
from datetime import datetime, timedelta
from app import app, init_db, get_db, check_conflict, times_overlap

@pytest.fixture
def client():
    app.config['TESTING'] = True
    init_db()

    with app.test_client() as client:
        yield client

    if os.path.exists('tablekeeper.db'):
        os.remove('tablekeeper.db')

@pytest.fixture
def sample_times():
    start = datetime.utcnow().replace(hour=18, minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=2)
    return start.isoformat(), end.isoformat()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'TableKeeper' in response.data
    assert b'Create Reservation' in response.data

def test_get_restaurants(client):
    response = client.get('/api/restaurants')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) >= 2
    names = [r['name'] for r in data]
    assert 'The Golden Fork' in names
    assert 'Sunset Bistro' in names

def test_get_tables(client):
    response = client.get('/api/tables/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3
    assert data[0]['table_number'] == 1
    assert data[0]['capacity'] == 2
    assert data[1]['table_number'] == 2
    assert data[1]['capacity'] == 4

def test_get_reservations(client):
    response = client.get('/api/reservations')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) >= 1
    assert 'customer_name' in data[0]
    assert 'start_time' in data[0]

def test_create_reservation_success(client, sample_times):
    start, end = sample_times
    response = client.post('/api/reservations',
        data=json.dumps({
            'table_id': 2,
            'customer_name': 'Bob Smith',
            'party_size': 3,
            'start_time': start,
            'end_time': end
        }),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['message'] == 'Reservation created successfully'

def test_create_reservation_overlapping_conflict(client, sample_times):
    """Test that overlapping reservations are rejected (double-booking prevention)"""
    start, end = sample_times

    response1 = client.post('/api/reservations',
        data=json.dumps({
            'table_id': 3,
            'customer_name': 'Charlie Brown',
            'party_size': 4,
            'start_time': start,
            'end_time': end
        }),
        content_type='application/json'
    )
    assert response1.status_code == 201

    overlap_start = (datetime.fromisoformat(start) + timedelta(minutes=30)).isoformat()
    overlap_end = (datetime.fromisoformat(end) + timedelta(minutes=30)).isoformat()

    response2 = client.post('/api/reservations',
        data=json.dumps({
            'table_id': 3,
            'customer_name': 'Diana Prince',
            'party_size': 2,
            'start_time': overlap_start,
            'end_time': overlap_end
        }),
        content_type='application/json'
    )
    assert response2.status_code == 409
    data = json.loads(response2.data)
    assert 'already booked' in data['error'].lower()

def test_party_size_exceeds_capacity(client, sample_times):
    start, end = sample_times
    response = client.post('/api/reservations',
        data=json.dumps({
            'table_id': 1,
            'customer_name': 'Eve Wilson',
            'party_size': 5,
            'start_time': start,
            'end_time': end
        }),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'capacity' in data['error'].lower()

def test_invalid_party_size(client, sample_times):
    start, end = sample_times
    response = client.post('/api/reservations',
        data=json.dumps({
            'table_id': 2,
            'customer_name': 'Frank Castle',
            'party_size': 0,
            'start_time': start,
            'end_time': end
        }),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'party size' in data['error'].lower()

def test_start_time_after_end_time(client):
    end = datetime.utcnow().replace(hour=18, minute=0, second=0, microsecond=0)
    start = end + timedelta(hours=2)

    response = client.post('/api/reservations',
        data=json.dumps({
            'table_id': 2,
            'customer_name': 'Grace Hopper',
            'party_size': 2,
            'start_time': start.isoformat(),
            'end_time': end.isoformat()
        }),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'start time must be before end time' in data['error'].lower()

def test_reservation_exceeds_max_duration(client):
    start = datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=5)

    response = client.post('/api/reservations',
        data=json.dumps({
            'table_id': 2,
            'customer_name': 'Henry Ford',
            'party_size': 2,
            'start_time': start.isoformat(),
            'end_time': end.isoformat()
        }),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'exceed' in data['error'].lower()

def test_delete_reservation(client, sample_times):
    start, end = sample_times

    create_response = client.post('/api/reservations',
        data=json.dumps({
            'table_id': 2,
            'customer_name': 'Isabel Myers',
            'party_size': 2,
            'start_time': start,
            'end_time': end
        }),
        content_type='application/json'
    )
    reservation_id = json.loads(create_response.data)['id']

    delete_response = client.delete(f'/api/reservations/{reservation_id}')
    assert delete_response.status_code == 200

    reservations_response = client.get(f'/api/reservations')
    reservations = json.loads(reservations_response.data)
    assert all(r['id'] != reservation_id for r in reservations if r['customer_name'] == 'Isabel Myers')

def test_times_overlap_utility():
    """Test the times_overlap helper function"""
    s1 = datetime(2026, 10, 1, 18, 0).isoformat()
    e1 = datetime(2026, 10, 1, 20, 0).isoformat()
    s2 = datetime(2026, 10, 1, 19, 0).isoformat()
    e2 = datetime(2026, 10, 1, 21, 0).isoformat()

    assert times_overlap(s1, e1, s2, e2) == True
    assert times_overlap(s1, e1, datetime(2026, 10, 1, 21, 0).isoformat(), datetime(2026, 10, 1, 22, 0).isoformat()) == False
    assert times_overlap(s1, e1, datetime(2026, 10, 1, 17, 0).isoformat(), datetime(2026, 10, 1, 18, 0).isoformat()) == False

def test_check_conflict_utility():
    """Test the check_conflict helper function"""
    init_db()

    now = datetime.utcnow()
    start = now.replace(minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=2)

    assert check_conflict(1, start.isoformat(), end.isoformat()) == True
    assert check_conflict(3, start.isoformat(), end.isoformat()) == False

    if os.path.exists('tablekeeper.db'):
        os.remove('tablekeeper.db')

def test_missing_customer_name(client, sample_times):
    start, end = sample_times
    response = client.post('/api/reservations',
        data=json.dumps({
            'table_id': 2,
            'customer_name': '   ',
            'party_size': 2,
            'start_time': start,
            'end_time': end
        }),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'name' in data['error'].lower()

def test_table_not_found(client, sample_times):
    start, end = sample_times
    response = client.post('/api/reservations',
        data=json.dumps({
            'table_id': 999,
            'customer_name': 'Jack Ryan',
            'party_size': 2,
            'start_time': start,
            'end_time': end
        }),
        content_type='application/json'
    )
    assert response.status_code == 404

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
