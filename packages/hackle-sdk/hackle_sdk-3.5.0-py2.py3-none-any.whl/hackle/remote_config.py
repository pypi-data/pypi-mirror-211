from .decision import RemoteConfigDecision, DecisionReason
from .internal.hackle_core import HackleCore
from .internal.type import hackle_types
from .internal.user.hackle_user_resolver import HackleUserResolver
from .model import HackleRemoteConfig, HackleUser


class HackleRemoteConfigImpl(HackleRemoteConfig):
    def __init__(self, user, core, hackle_user_resolver):
        """
        :param HackleUser user:
        :param HackleCore core:
        :param HackleUserResolver hackle_user_resolver:
        """
        self.__user = user
        self.__core = core
        self.__hackle_user_resolver = hackle_user_resolver

    def get(self, key, default=None):
        if hackle_types.is_string(default):
            parameter_value = self.__get(key, 'STRING', default).value
        elif hackle_types.is_number(default):
            parameter_value = self.__get(key, 'NUMBER', default).value
        elif hackle_types.is_bool(default):
            parameter_value = self.__get(key, 'BOOLEAN', default).value
        elif default is None:
            parameter_value = self.__get(key, 'NULL', default).value
        else:
            parameter_value = self.__get(key, 'UNKNOWN', default).value

        return parameter_value

    def __get(self, key, required_type, default):
        hackle_user = self.__hackle_user_resolver.resolve_or_none(self.__user)

        if hackle_user is None:
            return RemoteConfigDecision(default, DecisionReason.INVALID_INPUT)

        if key is None:
            return RemoteConfigDecision(default, DecisionReason.INVALID_INPUT)

        return self.__core.remote_config(key, hackle_user, required_type, default)
