"""
    QuaO Project quao_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit import transpile

from ...model.device.qiskit_device import QiskitDevice


class QuaoDevice(QiskitDevice):

    def _create_job(self, circuit, shots):
        transpiled_circuit = transpile(circuits=circuit, backend=self.device)

        return self.device.run(transpiled_circuit, shots=shots)

    def _is_simulator(self) -> bool:
        return True

    def _parse_job_result(self, job_result) -> dict:
        return job_result.to_dict()
