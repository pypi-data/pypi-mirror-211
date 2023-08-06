"""
    QuaO Project ibm_cloud_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit_ibm_runtime import Options, Session, Sampler

from src.quao.model.device.qiskit_device import QiskitDevice


class IbmCloudDevice(QiskitDevice):
    def _is_simulator(self) -> bool:
        return self.device.configuration().simulator

    def _parse_job_result(self, job_result) -> dict:
        return job_result.__dict__

    def _create_job(self, circuit, shots):
        options = Options(optimization_level=1)
        options.execution.shots = shots

        with Session(service=self.provider.collect_provider(), backend=self.device) as session:
            sampler = Sampler(session=session, options=options)
            job = sampler.run(circuits=circuit)

            return job
