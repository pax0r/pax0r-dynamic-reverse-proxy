import abc


class AuthBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_authorized(self, request, **kwargs) -> bool:
        raise NotImplementedError
