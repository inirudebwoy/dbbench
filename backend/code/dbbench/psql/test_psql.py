from pytest import fixture
from pytest import mark

from dbbench.base.testing import BaseFixture
from dbbench.sql.command import SqlCommand
from dbbench.sql.models import metadata
from dbbench.sql.query import SqlQuery


@mark.postgresql
class TestsPostgresql(BaseFixture):
    QUERY_CLS = SqlQuery
    COMMAND_CLS = SqlCommand

    @fixture(scope="session", autouse=True)
    def drop_all_finalizer(self, request):
        def finalizer():
            metadata.drop_all()
        request.addfinalizer(finalizer)

    @fixture
    def connection(self, app):
        if metadata.bind != app.psql.bind:
            metadata.bind = app.psql.bind
            metadata.create_all()
        yield app.psql

    @fixture
    def app(self, config):
        with config as app:
            yield app
