import requests

host = "http://localhost"
port = "5000"
url = host + ":" + port

add_url = url + "/data/wishlist/add"
get_url = url + "/data/wishlist/get"
update_url = url + "/data/wishlist/update"
delete_url = url + "/data/wishlist/delete"

added_wishlist_entry = ""

def test_add_to_wishlist():
     global added_wishlist_entry

     payload = {"book_id":1, "list_id":1}
     response = requests.post(add_url, json=payload)
     returned_obj = response.json()
     added_wishlist_entry = str(returned_obj["data"]["id"])

     assert response.status_code == 200

def test_get_all_wishlists():
     response = requests.get(get_url)
     assert response.status_code == 200

def test_get_single_wishlist():
     url = get_url + "/" + added_wishlist_entry
     response = requests.get(url=url)
     assert response.status_code == 200

def test_update_wishlist_entry():
     global added_wishlist_entry
     payload = {"book_id":5}
     url = update_url + "/" + added_wishlist_entry
     response = requests.put(url=url, json=payload)
     assert response.status_code == 200

def test_delete_wishlist_entry():
     global added_wishlist_entry 
     url = delete_url + "/" + added_wishlist_entry
     response = requests.delete(url=url)
     assert response.status_code == 200
