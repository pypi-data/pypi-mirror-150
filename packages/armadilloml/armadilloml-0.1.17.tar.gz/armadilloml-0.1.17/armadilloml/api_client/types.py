from pydantic import BaseModel


class Model(BaseModel):
    id: str
    description: str
    parent_user_id: str
    github_url: str
