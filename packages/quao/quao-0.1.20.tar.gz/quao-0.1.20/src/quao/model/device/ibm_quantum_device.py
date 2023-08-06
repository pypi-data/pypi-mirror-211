"""
    QuaO Project ibm_quantum_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from qiskit import transpile

from ...model.device.qiskit_device import QiskitDevice


class IbmQuantumDevice(QiskitDevice):

    def _is_simulator(self) -> bool:
        return self.device.configuration().simulator

    def _parse_job_result(self, job_result) -> dict:
        return job_result.to_dict()

    def _create_job(self, circuit, shots):
        transpile_circuit = transpile(circuit, self.device)

        return self.device.run(transpile_circuit, shots=shots)

