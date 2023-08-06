__all__ = ('UserPoint',)

from expressmoney.api import *

SERVICE = 'sync'


class UserReadContract(Contract):
    id = serializers.IntegerField(min_value=1)
    last_login = serializers.DateTimeField()
    username = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    date_joined = serializers.DateTimeField()


class UserID(ID):
    _service = SERVICE
    _app = 'auth'
    _view_set = 'user'


class UserPoint(ListPointMixin, ContractPoint):
    _point_id = UserID()
    _read_contract = UserReadContract
