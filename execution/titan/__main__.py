"""Allow running with: python -m titan.run"""
import asyncio
from .run import main

if __name__ == "__main__":
    asyncio.run(main())
