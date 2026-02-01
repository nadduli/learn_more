import asyncio
import logging
from sqlalchemy import select
from app.db.database import SessionLocal
from app.models.role import Role

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db() -> None:
    async with SessionLocal() as session:
        try:
            result = await session.execute(select(Role).where(Role.name == "user"))
            user_role = result.scalars().first()
            
            if not user_role:
                user_role = Role(name="user")
                session.add(user_role)
                await session.commit()
                await session.refresh(user_role)
                logger.info(f"Created 'user' role with ID: {user_role.id}")
            else:
                logger.info(f"Role 'user' already exists with ID: {user_role.id}")

            result = await session.execute(select(Role).where(Role.name == "admin"))
            admin_role = result.scalars().first()
            
            if not admin_role:
                admin_role = Role(name="admin")
                session.add(admin_role)
                await session.commit()
                await session.refresh(admin_role)
                logger.info(f"Created 'admin' role with ID: {admin_role.id}")
            else:
                logger.info(f"Role 'admin' already exists with ID: {admin_role.id}")
                
        except Exception as e:
            logger.error(f"Error seeding database: {e}")
            raise
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(init_db())
