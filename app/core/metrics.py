class MetricsTracker:
    _request_counts = 0
    _ai_calls = 0

    @classmethod
    def record_request(cls):
        cls._request_counts += 1

    @classmethod
    def record_ai_call(cls):
        cls._ai_calls += 1

    @classmethod
    def get_metrics(cls) -> dict:
        return {
            "total_api_requests": cls._request_counts,
            "total_ai_invocations": cls._ai_calls
        }
