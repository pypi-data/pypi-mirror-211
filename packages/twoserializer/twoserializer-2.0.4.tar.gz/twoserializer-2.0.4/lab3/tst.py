from lab3.Json import Json

with open("op.json") as file:
    a = file
    b = Json.dump(a)
    print(b)
