"""Create an admin-panel account.

    docker compose exec backend python -m app.scripts.create_admin you@example.com --role admin

The password is read from the terminal (or ADMIN_PASSWORD) and never echoed.
"""

import argparse
import asyncio
import getpass
import os
import sys

from fastapi import HTTPException

from app.db.session import AsyncSessionLocal, engine
from app.services.site.adminauth import create_admin


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("email")
    parser.add_argument("--role", choices=["admin", "editor"], default="admin")
    parser.add_argument("--name")
    args = parser.parse_args()
    password = os.environ.get("ADMIN_PASSWORD") or getpass.getpass("Password (12+ characters): ")
    try:
        async with AsyncSessionLocal() as db:
            user = await create_admin(db, args.email, password, args.role, args.name)
            await db.commit()
        print(f"Created {user.role} account for {user.email}")
        return 0
    except HTTPException as exc:
        print(f"Error: {exc.detail}", file=sys.stderr)
        return 1
    finally:
        await engine.dispose()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
