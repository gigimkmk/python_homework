

import requests

def get_user(user_id):
    url = "https://jsonplaceholder.typicode.com/users"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    users = response.json()

    for user in users:
        if user["id"] == user_id:
            return {
                "name": user["name"],
                "email": user["email"],
                "city": user["address"]["city"],
                "company": user["company"]["name"]
            }

    return None


print(get_user(3))
print(get_user(20))