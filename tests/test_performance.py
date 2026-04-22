import time

def test_load_time(client):
    start = time.time()
    client.get('/students')
    end = time.time()

    assert (end - start) < 4