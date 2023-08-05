"""
    QuaO Project backend.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from .dataUtils import RequestData
from .utilities import JobResponse
from .config.threadConfig import pool
from .config.loggingConfig import logging
from json import JSONDecodeError, dumps

import requests
import io


class Backend:
    def __init__(self, request_data: RequestData, circuit):

        self.server_url = request_data.server_url
        self.sdk = request_data.sdk
        self.input = request_data.input
        self.shots = request_data.shots
        self.required_qubit = self.get_qubit_number(circuit)
        self.backend_request = self.generate_backend_request(request_data.device_id)
        self.backend_data = self.get_backend_data()
        self.circuit_export_url = request_data.circuit_export_url
        pool.apply_async(self.__export_circuit, (circuit,))

    def get_qubit_number(self, circuit) -> int:

        if self.sdk == "qiskit":
            return int(circuit.num_qubits)
        return 0

    def generate_backend_request(self, device_id):

        backend_request = {
            "deviceId": device_id,
            "qubitAmount": self.required_qubit
        }

        return backend_request

    def get_backend_data(self):
        response = requests.get(
            self.server_url,
            params=self.backend_request
        )
        if response.status_code == 200:
            try:
                backend_data = response.json().get("data")
            except JSONDecodeError:
                return None
            return backend_data
        else:
            return None

    def submit_job(self, circuit) -> JobResponse:
        job_response = JobResponse()
        shots = self.shots
        if circuit and self.backend_data:
            if self.sdk == "qiskit":
                from .sdk.qiskit import QiskitFaaS

                be_instance = QiskitFaaS(self.backend_data)
                job_response = be_instance.submit_job(circuit, shots=shots)
            else:
                job_response.job_status = "ERROR"
                job_response.job_result = {"error": "SDK not supported"}
        elif self.backend_data is None:
            job_response.job_status = "ERROR"
            job_response.job_result = {"error": "Backend not found"}

        return job_response

    @staticmethod
    def __prepare_circuit_export_request(data: bytes) -> dict:
        return {
            'circuit': ('circuit_figure', data, 'multipart/form-data')
        }

    def __export_circuit(self, circuit):
        """
            Export circuit to svg file then send to QuaO server for saving
            Args:
                circuit: circuit will be exported
        """

        logging.info("Preparing circuit figure...")
        circuit_figure = circuit.draw(output='mpl', fold=-1)

        logging.info("Converting circuit figure to svg file...")
        buffer = io.BytesIO()
        circuit_figure.savefig(buffer, format='svg')

        logging.info("Sending circuit svg image to [%s] with POST method ...", self.circuit_export_url)
        response = requests.post(url=self.circuit_export_url,
                                 files=self.__prepare_circuit_export_request(buffer.getvalue()))
        if response.ok:
            logging.info("Sending request successfully!")
        else:
            logging.info("Sending request failed with status %s!", response.status_code)
