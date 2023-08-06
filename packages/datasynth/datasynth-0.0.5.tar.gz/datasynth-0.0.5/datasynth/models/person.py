import copy
from typing import List

from faker import Faker
from gytrash.logging_mixin import LoggingMixin


class Person(LoggingMixin):
    """Person object, this is iterable to allow for generation of multiple "People".

    Args:
        LoggingMixin (_type_): Logging object.
    """

    def __init__(self, *, attributes: list = ["name", "address", "ssn"]):
        """Creates a person object with the attributes passed in to the constructor.

        Args:
            attributes (list, optional): List of attributes, these names must match one of the method names in the Faker package (See this list of providers - https://faker.readthedocs.io/en/master/providers.html). Defaults to ["name", "address", "ssn"].
        """
        self.fake = Faker()
        self.attributes = attributes

    def __iter__(self) -> dict:
        """Generates a dictionary object of the person with randomly generated attributes.

        Yields:
            dict: Dictionary with fields matching the attribute names.
        """
        profile = {}
        while True:
            try:
                for attribute in self.attributes:
                    # dynamically calls faker method using the
                    # attribute name as the function name.
                    profile[attribute] = getattr(self.fake, attribute)()
                yield profile
            except AttributeError as ae:
                raise AttributeError(
                    f"Attribute - {attribute} - does not have a Faker provider. Attribute name must be a Faker provider method. See default list here: https://faker.readthedocs.io/en/master/providers.html"
                )
                break

    def generate_people(self, *, number: int) -> List[dict]:
        """Returns N number of person dictionary objects as a list.

        Args:
            number (int): Number of persons to generate

        Returns:
            List[dict]: list of person dictionary objects.
        """
        return [copy.copy(next(iter(self))) for i in range(number)]
