from pydantic import BaseModel


class RoleSchema(BaseModel):
    id: int
    name: str
    

class RequestRoleSchema(BaseModel):
    name: str
