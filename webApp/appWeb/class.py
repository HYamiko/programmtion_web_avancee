from django.middleware.clickjacking import XFrameOptionsMiddleware

class CustomXFrameOptionsMiddleware(XFrameOptionsMiddleware):
    def get_xframe_options_value(self, request, response):
        # Return "ALLOWALL" to allow framing from any origin
        return "ALLOWALL"
