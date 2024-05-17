from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from api_v1.dependencies import role_service
from api_v1.jwt_auth.validations import get_current_admin_payload
from schemas.role_schema import RequestRoleSchema


role_router = APIRouter(
    prefix="/role",
    tags=["Roles"],
    dependencies=[Depends(get_current_admin_payload)]
)


@role_router.post("/create")
async def create_role(
    role: RequestRoleSchema,
    role_service=Depends(role_service)
):
    role_id = await role_service.create(role)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"role_id": role_id}
    )


@role_router.get("/{id}")
async def get_role(
    id: int,
    role_service=Depends(role_service)
):
    role = await role_service.get_one(id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=role.model_dump()
    )


@role_router.get("/")
async def get_roles(
    role_service=Depends(role_service)
):
    roles = await role_service.get_all()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[role.model_dump() for role in roles]
    )


@role_router.patch("/{id}")
async def update_role(
    id: int,
    role: RequestRoleSchema,
    role_service=Depends(role_service)
):
    role = await role_service.update(id, role)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=role.model_dump()
    )


@role_router.delete("/{id}")
async def delete_role(
    id: int,
    role_service=Depends(role_service)
):
    await role_service.delete(id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Role deleted successfully'}
    )
