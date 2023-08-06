import requests


class SendTeams():
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def _get_my_ip(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def _send(self, payload):
        try:
            response = requests.post(
                url=self.webhook_url,
                headers={"Content-Type": "application/json"},
                json=payload)
            return response.status_code
        except requests.RequestException as e:
            return -1

    def send_results(self, project_name: str = "", name: str = "", metrics: list = [], values: list = [], results_path: str = None) -> int:
        """
        :param project_name:
        :param name: Username to be displayed
        :param metrics: list of string of each metric to be sent
        :param values: list of values corresponding to eachmetric to be sent
        :param results_path: Results path to be displayed
        :return:
        """
        assert len(metrics) == len(values)
        results = [{"name": metric, "value": value} for (metric, value) in zip(metrics, values)]
        title = name + "'s run ended"
        sub = "On Project " + project_name + " on " + self._get_my_ip()
        txt = "Results stored in: " + results_path
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "Run results",
            "sections": [{
                "activityTitle": title,
                "activitySubtitle": sub,
                "activityText": txt,
                "facts": results,
                "markdown": True
            }]
        }
        return self._send(payload)
