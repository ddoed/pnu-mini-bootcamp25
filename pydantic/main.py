from pydantic import BaseModel

class User(BaseModel):
	id: int
	name: str
	email: str
	is_active: bool = True

user = User(id="1f1", name="Linux", email="linux@linux.com")
print(user)