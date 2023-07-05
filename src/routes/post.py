
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status

from db.models import User
from schemas.post import PostCreate, PostOut, PostUpdate
from schemas.base import ResponseDetails
from dependencies.user import get_user_by_token
from repositories.post import PostRepo
from services.post import PostService


posts_router = APIRouter(
    prefix='/community', # can be /network, /forum, etc.
    tags=['community'],
)


@posts_router.get('/posts', response_model=list[PostOut])
async def get_posts(
    post_repo: Annotated[PostRepo, Depends()],
    topic: Optional[str] = Query(None, min_length=1, max_length=50, description='Topic of post'),
    page: int = Query(0, description='Page of pagination'),
    limit: int = Query(100, description='Limit for pagination page'),
) -> list[PostOut]:
    """ Get all posts """
    filters = {}
    if topic:
        filters = {'topic': topic}
    result = await post_repo.filter_with_author(page, limit, **filters)
    return result


@posts_router.get('/posts/{post_id}', response_model=PostOut)
async def get_post(
    post_id: int, 
    post_repo: Annotated[PostRepo, Depends()],
) -> PostOut:
    """ Get post by id """
    post = await post_repo.get_by_id_with_author(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )
    return post


@posts_router.post('/posts', response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    post_service: Annotated[PostService, Depends()],
    user: Annotated[User, Depends(get_user_by_token)],
) -> PostOut:
    """ Create post """
    post = await post_service.create_post(post, user.id)
    return post


@posts_router.put('/posts', response_model=ResponseDetails)
async def update_post(
    post: PostUpdate,
    user: Annotated[User, Depends(get_user_by_token)],
    post_repo: Annotated[PostRepo, Depends()],
) -> ResponseDetails:
    """ Update post """
    result = await post_repo.update_post_if_author(post.id, user.id, **post.dict())
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found or you are not the author',
        )
    return ResponseDetails(
        success=True,
        details='Post updated successfully',
    )


@posts_router.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    user: Annotated[User, Depends(get_user_by_token)],
    post_repo: Annotated[PostRepo, Depends()],
) -> None:
    """ Delete post """
    result = await post_repo.delete_post_if_author(post_id, user.id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found or you are not the author',
        )
