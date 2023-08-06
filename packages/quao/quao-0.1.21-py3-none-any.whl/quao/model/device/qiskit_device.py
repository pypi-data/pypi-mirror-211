"""
    QuaO Project qiskit_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from abc import ABC

from qiskit import QiskitError

from ...model.device.device import Device


class QiskitDevice(Device, ABC):

    def _produce_histogram_data(self, job_result) -> dict:
        try:
            histogram_data = job_result.get_counts()
        except QiskitError:
            histogram_data = None

        return histogram_data

    def _get_provider_job_id(self, job) -> str:
        return job.job_id()

    def _get_job_status(self, job) -> str:
        return job.status().name
