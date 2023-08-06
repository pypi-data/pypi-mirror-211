"""
    QuaO Project quao_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit_aer import Aer

from src.quao.enum.provider_type import ProviderType
from src.quao.model.provider.provider import Provider


class QuaoProvider(Provider):
    def __init__(self):
        super().__init__(ProviderType.QUAO_QUANTUM_SIMULATOR)

    def get_backend(self, device_specification):
        """

        @param device_specification:
        @return:
        """

        provider = self.collect_provider()

        return provider.get_backend(device_specification)

    def collect_provider(self):
        """

        @return:
        """
        return Aer
