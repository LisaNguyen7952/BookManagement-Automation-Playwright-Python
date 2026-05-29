def get_response_data(response):
    content_type = response.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            return response.json()
        except Exception:
            return response.text()
    return response.text()