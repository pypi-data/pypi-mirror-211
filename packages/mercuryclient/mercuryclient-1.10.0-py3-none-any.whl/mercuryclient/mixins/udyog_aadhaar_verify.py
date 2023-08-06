import time


class UdyogAadhaarVerifyMixin:
    """
    Mixin for Udyog Aadhaar verification
    """

    def initiate_udyog_verification(
        self, udyog_aadhaar: str, provider: str, profile: str
    ):
        """
        udyog verification using the mercury service

        :param udyog_aadhaar: string
        :param provider: any
        :param profile: An existing profile in Mercury. The profile has to correspond
        to the provider.
        :return: (request_id, data)
        """
        api = "api/v1/udyog_aadhaar/verify/"

        request_dict = {
            "profile": profile,
            "provider": provider,
            "udyog_aadhaar": udyog_aadhaar,
        }

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )
        try:
            response_json = r.json()
        except Exception:
            response_json = {}

        if r.status_code == 201:
            return request_id

        raise Exception(
            f"Error while sending Udyog aadhaar verify request. Status: {r.status_code}, Response is {response_json}"
        )

    def get_udyog_details(self, request_id: str):
        api = "api/v1/udyog_aadhaar/verify/"

        request_id, r = self._get_json_http_request(
            api,
            headers={"X-Mercury-Request-Id": request_id},
            send_request_id=False,
            add_bearer_token=True,
        )

        if r.status_code == 200:
            result = r.json()
            if result["status"] == "FAILURE":
                raise Exception(
                    f"Error verifying Udyog aadhaar. Status: {result['status']} | Message {result['message']}"
                )
            return request_id, result

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            f"Error getting Udyog aadhaar Verification result. Status: {r.status_code}, Response is {response_json}"
        )

    def get_udyog_verification_result(
        self, mercury_request_id: str, max_attempts: int, retry_backoff: int
    ):
        """Retry mechanism for Udyog aadhaar response

        raises:
            Exception: After max attempts, response till remains in progress

        returns mercury_request_id,response from the vendor

        """

        for attempts in range(max_attempts):
            time.sleep(retry_backoff)
            mercury_request_id, result = self.get_udyog_details(mercury_request_id)
            if result.get("status") != "IN_PROGRESS":
                return mercury_request_id, result

            retry_backoff *= 2

        raise Exception(
            "Error while getting Udyog aadhaar response. Status: IN_PROGRESS"
        )

    def verify_udyog_aadhaar(
        self,
        udyog_aadhaar: str,
        provider: str,
        profile: str,
        max_attempts: int = 3,
        retry_backoff: int = 5,
    ):
        """Get OTP from customer and verify with request_id.

        returns: mercury_request_id, verify Udyog aadhaar response from vendor
        """
        mercury_request_id = self.initiate_udyog_verification(
            udyog_aadhaar, provider, profile
        )
        return self.get_udyog_verification_result(
            mercury_request_id, max_attempts, retry_backoff
        )
