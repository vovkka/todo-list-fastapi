from environs import Env


class Settings:
    env = Env()
    env.read_env()

    DB_HOST = env("DB_HOST")
    DB_PORT = env("DB_PORT")
    DB_USER = env("DB_USER")
    DB_PASS = env("DB_PASS")
    DB_NAME = env("DB_NAME")

    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SECRET_KEY = env("SECRET_KEY")
    ALGORITHM = env("ALGORITHM")


settings = Settings()