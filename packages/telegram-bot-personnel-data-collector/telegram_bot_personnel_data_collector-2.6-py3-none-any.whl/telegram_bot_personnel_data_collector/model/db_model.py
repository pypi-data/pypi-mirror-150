from abc import ABC, abstractmethod


class ServiceModel(ABC):
    @abstractmethod
    def start(self, **kwargs):
        pass

    def stop(self):
        pass


class DBModel(ABC):

    @abstractmethod
    def set_person(self, **person_properties):
        """
        Adding personnel data entry
        If person username already existing - update entry

        :param person_properties:
        """
        pass

    @abstractmethod
    def is_person_exist(self, **person_properties):
        """
        Looking person entry by 'username'
        Return entry id or last free line number if not exist
        :param person_properties:
        """
        pass
