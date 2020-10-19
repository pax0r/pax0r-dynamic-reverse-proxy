import abc


class BackendBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_ip(self, domain):
        pass

    @abc.abstractmethod
    def set_ip(self, domain, ip):
        pass

