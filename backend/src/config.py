from os import environ as env

from pydantic import BaseModel, Field


class PostgresConfig(BaseModel):
    host: str = Field(alias='POSTGRES_HOST')
    port: int = Field(alias='POSTGRES_PORT')
    login: str = Field(alias='POSTGRES_USER')
    password: str = Field(alias='POSTGRES_PASSWORD')
    database: str = Field(alias='POSTGRES_DB')


class RedisConfig(BaseModel):
    host: str = Field(alias='REDIS_HOST')
    port: int = Field(alias='REDIS_PORT', default=6379)


class TelegramConfig(BaseModel):
    token: str = Field(alias='TELEGRAM_TOKEN_BOT')


class RabbitMQ(BaseModel):
    user: str = Field(alias='RABBITMQ_DEFAULT_USER')
    password: str = Field(alias='RABBITMQ_DEFAULT_PASS')


class JWT(BaseModel):
    secret_key: str = Field(alias='JWT_SECRET_KEY')
    refresh_secret_key: str = Field(alias='REFRESH_SECRET_KEY')
    algorithm: str = Field(alias='ALGORITHM')
    access_token_expire_minutes: int = Field(alias='ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_expire_days: int = Field(alias='REFRESH_TOKEN_EXPIRE_DAYS')


class Robokassa(BaseModel):
    robokassa_login: str = Field(alias='ROBOKASSA_LOGIN')
    robokassa_password1: str = Field(alias='ROBOKASSA_PASSWORD1')
    robokassa_password2: str = Field(alias='ROBOKASSA_PASSWORD2')
    robokassa_test: str = Field(alias='ROBOKASSA_TEST')


class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    redis: RedisConfig = Field(default_factory=lambda: RedisConfig(**env))
    telegram: TelegramConfig = Field(default_factory=lambda: TelegramConfig(**env))
    rabbitmq: RabbitMQ = Field(default_factory=lambda: RabbitMQ(**env))
    jwt: JWT = Field(default_factory=lambda: JWT(**env))
