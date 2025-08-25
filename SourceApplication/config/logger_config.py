# import logging
# from datetime import datetime
# from flask import request

# # Custom Log Format
# log_format = "%(client_ip)s - %(timestamp)s - %(api_title)s - [%(request_method)s %(route)s %(http_version)s %(response_status)s]"

# # API Title Mapping
# ROUTE_TO_TITLE = {
#     "/auth/login": "LOGIN_API",
#     "/auth/signup": "ADD_USER_API",
#     "/auth/protected": "PROTECTED_API",
#     "/auth/logout": "LOGOUT_API",
#     "/": "HOME_API",
#     "/login": "SIGNIN_API",
#     "/signup": "SIGNUP_API",
#     "/home": "PROFILE_API", 
# }

# # Custom Formatter
# class CustomFormatter(logging.Formatter):
#     def format(self, record):
#         record.client_ip = request.remote_addr or "Unknown IP"
#         record.timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

#         # Get API title from route mapping or mark as UNKNOWN
#         record.api_title = ROUTE_TO_TITLE.get(request.path, "STATIC")

#         record.request_method = request.method
#         record.route = request.path
#         record.http_version = request.environ.get("SERVER_PROTOCOL", "HTTP/1.1")
#         record.response_status = getattr(record, "response_status", "N/A")

#         return super().format(record)

# # Custom Logger Setup
# def setup_logger():
#     logger = logging.getLogger("flask_logger")

#     # Check if logger already has handlers (avoid duplicates)
#     if not logger.hasHandlers():
#         handler = logging.StreamHandler()  # Console output
#         # If you want to log to a file instead:
#         # handler = logging.FileHandler('app_logs.log')

#         formatter = CustomFormatter(log_format)
#         handler.setFormatter(formatter)
#         logger.addHandler(handler)
#         logger.setLevel(logging.INFO)

#     return logger

# import logging
# from datetime import datetime
# from flask import request, jsonify

# # Standard Log Format
# default_log_format = "%(client_ip)s - %(timestamp)s - %(api_title)s - [%(request_method)s %(route)s %(http_version)s %(response_status)s]"

# # Login API Log Format (with Username)
# login_log_format = "%(client_ip)s - %(timestamp)s - %(api_title)s - [%(request_method)s %(route)s %(http_version)s %(response_status)s] - USERNAME: %(username)s"

# # API Title Mapping
# ROUTE_TO_TITLE = {
#     "/auth/login": "LOGIN_API",
#     "/auth/signup": "ADD_USER_API",
#     "/auth/protected": "PROTECTED_API",
#     "/auth/logout": "LOGOUT_API",
#     "/": "HOME_API",
#     "/login": "SIGNIN_API",
#     "/signup": "SIGNUP_API",
#     "/home": "PROFILE_API", 
# }

# # Custom Formatter
# class CustomFormatter(logging.Formatter):
#     def format(self, record):
#         record.client_ip = request.remote_addr or "Unknown IP"
#         record.timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

#         # Get API title from route mapping or mark as STATIC/UNKNOWN
#         record.api_title = ROUTE_TO_TITLE.get(request.path, "STATIC")

#         record.request_method = request.method
#         record.route = request.path
#         record.http_version = request.environ.get("SERVER_PROTOCOL", "HTTP/1.1")
#         record.response_status = getattr(record, "response_status", "N/A")

#         # Check if the route is /auth/login and set custom format
#         if request.path == "/auth/login": # and request.method == "POST":
#             try:
#                 data = request.json or {}
#                 record.username = data.get("username", "UNKNOWN_USER")
#             except Exception:
#                 record.username = "ERROR_PARSING"
#             self._fmt = login_log_format  # Use login-specific log format
#         else:
#             record.username = "N/A"
#             self._fmt = default_log_format  # Use default log format

#         return super().format(record)

# # Custom Logger Setup
# def setup_logger():
#     logger = logging.getLogger("flask_logger")

#     # Check if logger already has handlers (avoid duplicates)
#     if not logger.hasHandlers():
#         handler = logging.StreamHandler()  # Console output
#         # If you want to log to a file instead:
#         # handler = logging.FileHandler('app_logs.log')

#         formatter = CustomFormatter(default_log_format)
#         handler.setFormatter(formatter)
#         logger.addHandler(handler)
#         logger.setLevel(logging.INFO)

#     return logger


import logging
from datetime import datetime
from flask import request

# Standard Log Format
default_log_format = (
    "%(client_ip)s - %(timestamp)s - %(api_title)s - "
    "[%(request_method)s %(route)s %(http_version)s %(response_status)s]"
)

# Login API Log Format (with Username)
login_log_format = (
    "%(client_ip)s - %(timestamp)s - %(api_title)s - "
    "[%(request_method)s %(route)s %(http_version)s %(response_status)s] - USERNAME: %(username)s"
)

# API Title Mapping
ROUTE_TO_TITLE = {
    "/auth/login": "LOGIN_API",
    "/auth/signup": "ADD_USER_API",
    "/auth/protected": "PROTECTED_API",
    "/auth/logout": "LOGOUT_API",
    "/": "HOME_API",
    "/login": "SIGNIN_API",
    "/signup": "SIGNUP_API",
    "/home": "PROFILE_API",
}

# Custom Formatter
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Basic request details
        record.client_ip = request.remote_addr or "Unknown IP"
        record.timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        record.api_title = ROUTE_TO_TITLE.get(request.path, "STATIC")
        record.request_method = request.method
        record.route = request.path
        record.http_version = request.environ.get("SERVER_PROTOCOL", "HTTP/1.1")
        record.response_status = getattr(record, "response_status", "N/A")

        # Dynamic username extraction for POST /auth/login
        if request.path == "/auth/login" and request.method == "POST":
            try:
                data = request.get_json() or {}
                record.username = data.get("username", "UNKNOWN_USER")
            except Exception:
                record.username = "ERROR_PARSING"
            self._style._fmt = login_log_format  # Dynamic format
        else:
            record.username = "N/A"
            self._style._fmt = default_log_format

        return super().format(record)

# Logger Setup
def setup_logger():
    logger = logging.getLogger("flask_logger")

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = CustomFormatter(default_log_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
