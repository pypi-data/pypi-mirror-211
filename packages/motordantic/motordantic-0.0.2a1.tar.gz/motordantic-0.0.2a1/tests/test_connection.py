import os

from motordantic.connection import (
    connect,
    MotordanticConnection,
    DEFAULT_ENV_NAME,
    _connections,
)

from motor.motor_asyncio import AsyncIOMotorClient


class TestWriteConnectionParams:
    def setup(self):
        connect("mongodb://127.0.0.1:27017", "test")
        self.connection = _connections[DEFAULT_ENV_NAME]
        assert isinstance(self.connection, MotordanticConnection)

    def test_envirnament_values(self):
        database_name = os.getenv('MOTORDANTIC_DATABASE')
        assert database_name == 'test'

        address = os.getenv('MOTORDANTIC_ADDRESS')
        assert address == "mongodb://127.0.0.1:27017"

        env_name = os.getenv('MOTORDANTIC_ENV_NAME')
        assert env_name == DEFAULT_ENV_NAME

    def test_connection_params(self):
        database_name = self.connection.database_name
        conn_string = self.connection.address
        assert database_name == "test"
        assert conn_string == "mongodb://127.0.0.1:27017"

    def test_connection(self):
        motor_client = self.connection._get_motor_client()
        assert isinstance(motor_client, AsyncIOMotorClient)

    def test_conection_database(self):
        motor_client = self.connection._get_motor_client()
        assert motor_client.get_database('test') == AsyncIOMotorClient(
            "mongodb://127.0.0.1:27017"
        ).get_database("test")
