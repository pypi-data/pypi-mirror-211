"""
    QuaO Project response_utils.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from src.quao.data.job.job_response import JobResponse
from src.quao.enum.http_status import HttpStatus
from src.quao.enum.job_status import JobStatus


class ResponseUtils:
    def __init__(self):
        pass

    @staticmethod
    def generate_response(job_response: JobResponse) -> dict:
        if job_response:
            status_code = HttpStatus.NOT_YET_FINISHED.value

            if JobStatus.DONE.value.__eq__(job_response.job_status):
                status_code = HttpStatus.SUCCESS.value

            elif JobStatus.ERROR.value.__eq__(job_response.job_status):
                status_code = HttpStatus.ERROR.value

            job_dict = {
                "providerJobId": job_response.provider_job_id,
                "jobStatus": job_response.job_status,
                "jobResult": job_response.job_result
            }

            response = {"statusCode": status_code, "body": job_dict}
        else:
            response = {
                "statusCode": 500,
                "body": "Error in function code. Please contact the developer.",
            }
        return response
