from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_product():
    return {"message": "პროდუქტების მიღება წარმატებით შესრულდა"}


@app.post("/products")
def create_product():
    return {"message": "პროდუქტი შეიქმნა წარმატებით"}


@app.put("/products")
def update_product():
    return {"message": "პროდუქტი სრულად განახლდა წარმატებით"}


@app.patch("/products")
def partial_update_product():
    return {"message": "პროდუქტი ნაწილობრივ განახლდა წარმატებით"}


@app.delete("/products")
def delete_product():
    return {"message": "პროდუქტი წაიშალა წარმატებით"}