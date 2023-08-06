
class JobResponse(object):
    def __init__(
            self,
            provider_job_id: str = "",
            job_status: str = "",
            job_result=None,
            content_type=None,
            job_histogram=None
    ):
        self.provider_job_id = provider_job_id if provider_job_id else ""
        self.job_status = job_status if job_status else "ERROR"
        self.job_result = job_result if job_result else None
        self.content_type = content_type if content_type else "*/*"
        self.job_histogram = job_histogram if job_histogram else None


class Utils:
    def __init__(self):
        # do nothing
        pass

    @staticmethod
    def generate_response(job_response: JobResponse) -> dict:
        if job_response:
            status_code = 201  # not yet finished
            if job_response.job_status == "DONE":
                status_code = 200
            elif job_response.job_status == "ERROR":
                status_code = 400
            job_dict = {
                "providerJobId": job_response.provider_job_id,
                "jobStatus": job_response.job_status,
                "jobResult": job_response.job_result,
                "contentType": job_response.content_type,
                "histogram": job_response.job_histogram
            }  # Object to directory
            response = {"statusCode": status_code, "body": job_dict}
        else:
            response = {
                "statusCode": 500,
                "body": {"error": "Error in function code. Please contact the developer."},
            }
        return response
