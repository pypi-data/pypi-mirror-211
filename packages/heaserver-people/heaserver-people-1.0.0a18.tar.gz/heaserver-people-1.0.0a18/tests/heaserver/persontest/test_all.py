from .testcase import TestCase
from .permissionstestcase import PermissionsTestCase
from heaserver.service.testcase.mixin import GetOneMixin, GetAllMixin, PermissionsGetOneMixin, PermissionsGetAllMixin



class TestGet(TestCase, GetOneMixin):
    pass


class TestGetAll(TestCase, GetAllMixin):
    pass


class TestGetOneWithBadPermissions(PermissionsTestCase, PermissionsGetOneMixin):
    """A test case class for testing GET one requests with bad permissions."""
    pass


class TestGetAllWithBadPermissions(PermissionsTestCase, PermissionsGetAllMixin):
    """A test case class for testing GET all requests with bad permissions."""
    pass

