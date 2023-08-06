import json
from qiskit import transpile, QiskitError
from qiskit_aer import Aer
from qiskit_ibm_runtime import QiskitRuntimeService, Options, Session, Sampler
from qiskit_ibm_provider import IBMProvider

from ..utilities import JobResponse
from ..enum.providerType import ProviderType


APPLICATION_JSON = 'application/json'


class QiskitFaaS:

    def __init__(self, backend_data):
        self.device_name = backend_data.get("deviceName")
        self.provider_tag = backend_data.get("providerTag")
        self.connection = backend_data.get("authentication")

    def get_aer_backend(self):
        return Aer.get_backend(self.device_name)

    def get_ibm_provider(self, channel):
        token = self.connection.get("token")
        if channel == "ibm_cloud":
            instance = self.connection.get("crn")
            return QiskitRuntimeService(channel=channel, token=token, instance=instance)
        elif channel == "ibm_quantum":
            return IBMProvider(token=token)

    @staticmethod
    def __get_histogram(result):
        try:
            histogram = result.get_counts()
        except QiskitError:
            histogram = None

        return histogram

    def run_circuit_on_ibm_cloud(self, provider, circuit, shots):
        options = Options(optimization_level=1)
        options.execution.shots = shots

        with Session(service=provider, backend=self.device_name) as session:
            sampler = Sampler(session=session, options=options)
            job = sampler.run(circuits=circuit)

            return job

    def is_simulator(self, provider):
        backend = provider.get_backend(self.device_name)
        return backend.configuration().simulator

    def run_ibm_cloud_job(self, channel, circuit, shots) -> JobResponse:
        provider_job_id = ''
        content_type = None
        job_histogram = None

        try:
            provider = self.get_ibm_provider(channel=channel)
            job = self.run_circuit_on_ibm_cloud(provider=provider, circuit=circuit, shots=shots)
            provider_job_id = job.job_id()
            job_status = job.status().name
            job_result = {}
            if self.is_simulator(provider) or job_status == "DONE":
                result = job.result()
                job_status = job.status().name
                job_result = result.__dict__
                content_type = APPLICATION_JSON
                job_histogram = self.__get_histogram(result=result)

        except Exception as exception:
            job_result = {
                "error": "Exception when invoke job on " + channel + " provider",
                "exception": str(exception)
            }
            job_status = "ERROR"

        return JobResponse(
            provider_job_id=provider_job_id,
            job_status=job_status,
            job_result=job_result,
            content_type=content_type,
            job_histogram=job_histogram
        )

    def run_circuit_on_ibm_quantum(self, provider, circuit, shots):
        backend = provider.get_backend(self.device_name)
        transpile_circuit = transpile(circuit, backend)

        return backend.run(transpile_circuit, shots=shots)

    def run_ibm_quantum_job(self, circuit, shots) -> JobResponse:
        provider_job_id = ''
        content_type = None
        job_histogram = None

        try:
            provider = self.get_ibm_provider('ibm_quantum')
            job = self.run_circuit_on_ibm_quantum(provider=provider, circuit=circuit, shots=shots)
            provider_job_id = job.job_id()
            job_status = job.status().name
            job_result = {}
            if self.is_simulator(provider) or job_status == "DONE":
                result = job.result()
                job_status = job.status().name
                job_result = result.to_dict()
                content_type = APPLICATION_JSON
                job_histogram = self.__get_histogram(result=result)

            # handle job result has Statevector Object
            if self.device_name == 'statevector_simulator':
                job_result = json.dumps(job_result)

        except Exception as exception:
            job_result = {
                "error": "Exception when invoke job on IBM Quantum provider",
                "exception": str(exception)
            }
            job_status = "ERROR"

        return JobResponse(
            provider_job_id=provider_job_id,
            job_status=job_status,
            job_result=job_result,
            content_type=content_type,
            job_histogram=job_histogram
        )

    def submit_job(self, qcircuit, shots) -> JobResponse:
        if self.provider_tag == ProviderType.QUAO_QUANTUM_SIMULATOR.value:
            provider_job_id = ''
            content_type = None
            job_histogram = None

            try:
                backend = self.get_aer_backend()
                transpile_circuit = transpile(qcircuit, backend)

                job = backend.run(transpile_circuit, shots=shots)
                provider_job_id = job.job_id()
                result = job.result()
                job_result = result.to_dict()
                job_status = job.status().name
                content_type = APPLICATION_JSON
                job_histogram = self.__get_histogram(result=result)

            except Exception as exception:
                job_result = {
                    "error": "Exception when invoke job with Quao provider",
                    "exception": str(exception)
                }
                job_status = "ERROR"
            return JobResponse(
                provider_job_id=provider_job_id,
                job_status=job_status,
                job_result=job_result,
                content_type=content_type,
                job_histogram=job_histogram
            )
        elif self.provider_tag == ProviderType.IBM_QUANTUM.value:
            return self.run_ibm_quantum_job(circuit=qcircuit, shots=shots)
        elif self.provider_tag == ProviderType.IBM_CLOUD.value:
            return self.run_ibm_cloud_job(channel="ibm_cloud", circuit=qcircuit, shots=shots)

        return JobResponse(
            job_status="ERROR",
            job_result={"error": "Provider not supported"}
        )
