from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztlV1P2zAUhv9KlCsmMQRZC2h3oXSi09pOELYJhCI3cVOrjh1sZ1Ch/nd8nKT56IdaCT"
    "Qq7S55z2v7nCfOOS92zENM5ZGLBQkm9lfrxWYoxvqhETm0bJQkpQ6CQiNqrKj0jKQSKFBa"
    "HSMqsZZCLANBEkU40ypLKQWRB9pIWFRKKSOPKfYVj7CaYKED9w9aJizEz1gWr8nUHxNMw1"
    "qqJISzje6rWWK0HlPfjBFOG/kBp2nMSnMyUxPOFm7CFKgRZlgghWF7JVJIH7LL6ywqyjIt"
    "LVmKlTUhHqOUqkq5WzIIOAN+OhtpCozglM/OSeusdf7ltHWuLSaThXI2z8ora88WGgIDz5"
    "6bOFIocxiMJbe/WEhIaQleZ4LEanqVJQ2EOvEmwgLYJoaFUEIsL84bUYzRs08xixRccKfd"
    "3sDsl3vduXKvD7TrE1TD9WXO7vggDzlZDMCWIOHX2AFibt9PgCfHx1sA1K61AE2sDlCfqH"
    "D2D9Yhfr8ZDlZDrCxpgLxlusD7kATq0KJEqoePiXUDRagako6lfKRVeAd990+Ta+fH8MJQ"
    "4FJFwuxiNrjQjKFljqeVnx+EEQqmT0iE/lKEO3yddzkUO3FTQQxFhhVUDPXlQ+RWmoa+NF"
    "yMvnG0pIXj/2DZo8ECX80879AUq2vepjO+O8VaX2xv0xbb67tie6kp4hgRugvCxYJ95Pcu"
    "gzkQGAr20YrRcqkjisR4zXiprWwADfOlR8XDx5wwtq4hHDI6y7/dBr5er9+98dz+z9rYuX"
    "S9LkQco84a6sFp41MsNrF+97wrC16tu+Gg25xOC593Z0NOKFXcZ/zJR2HlmhVqAebfDrP5"
    "K5SsMgM="
)
