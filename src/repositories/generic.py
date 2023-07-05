from typing import TypeVar, Type, Generic, Optional, Any

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import BaseModel


T = TypeVar("T", bound=BaseModel)


class GenericRepo(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        """
        Initializes the repository with the given session and model.

        :param session: The SQLAlchemy session to use.
        :param model: The SQLAlchemy model to use.
        """
        self.session = session
        self.model = model

    async def get_all(self) -> list[T]:
        """
        Retrieves all objects from the database.

        :return: A list of all objects of the model type.
        """
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Optional[T]:
        """
        Retrieves an object by its ID.

        :param id: The ID of the object to retrieve.
        :return: The object if found, None otherwise.
        """
        result = await self.session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def create(self, **kwargs: dict[str, Any]) -> T:
        """
        Creates a new object with the given keyword arguments.

        :param kwargs: The keyword arguments to use for creating the object.
        :return: The newly created object.
        """
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, **kwargs: dict[str, Any]) -> None:
        """
        Updates an object with the given ID and keyword arguments.

        :param id: The ID of the object to update.
        :param kwargs: The keyword arguments to use for updating the object.
        """
        await self.session.execute(update(self.model).where(self.model.id == id).values(**kwargs))
        await self.session.commit()

    async def delete(self, id: int) -> Optional[T]:
        """
        Deletes an object by its ID.

        :param id: The ID of the object to delete.
        :return: The deleted object if found, None otherwise.
        """
        obj = await self.get_by_id(id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return obj

    async def filter(self, page: int = 1, per_page: int = 10, **kwargs: dict[str, Any]) -> list[T]:
        """
        Filters objects based on the given keyword arguments and paginate the result.

        :param page: The page number to retrieve.
        :param per_page: The number of items per page.
        :param kwargs: The keyword arguments to use for filtering the objects.
        :return: A list of objects that match the filter criteria.
        """
        offset = (page) * per_page
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        query = select(self.model).where(and_(*filters)).limit(per_page).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()
