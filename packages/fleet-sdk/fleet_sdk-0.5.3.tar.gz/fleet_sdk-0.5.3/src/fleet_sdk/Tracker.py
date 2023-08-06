import time
import json
import requests
import pkg_resources
from functools import wraps
from fastapi import Request, Response, FastAPI
from quart import request as QuartRequest, Quart, Response as QuartResponse
from flask import request as FlaskRequest, Flask, Response as FlaskResponse
import importlib
import os
import sys

# Add the parent directory of 'sdk' to the system path
sdk_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(sdk_dir)
if parent_dir not in sys.path:
  sys.path.insert(0, parent_dir)


class Tracker:
  DEFAULT_HOST = 'middleware.usefleet.ai'
  DEFAULT_DEBUG = True

  def __init__(self, token, app, host=DEFAULT_HOST, debug=DEFAULT_DEBUG):
    """
        Initialize the Tracker with the provided token, host, and debug flag.
    """
    self.token = token
    self.host = host
    self.debug = debug
    self.app = app  # Store the app instance
    self.adapter = self._get_adapter()

  def _get_adapter(self):
    """
    Get the appropriate adapter based on the installed web framework.
    """
    framework_to_adapter_class = {
      'fastapi': ('FastAPIAdapter', 'fastapi', 'FastAPI'),
      'flask': ('FlaskAdapter', 'flask', 'Flask'),
      'quart': ('QuartAdapter', 'quart', 'Quart'),
    }

    for framework, (adapter_class_name, module_name,
                    class_name) in framework_to_adapter_class.items():
      try:
        module = importlib.import_module(module_name)

        if module_name in sys.modules and isinstance(
            self.app, getattr(module, class_name)):
          adapter_module = importlib.import_module(
            f"fleet_sdk.adapters.{framework}_adapter")
          adapter_class = getattr(adapter_module, adapter_class_name)

          return adapter_class()
      except ImportError:
        continue

    raise ImportError('No supported web framework found.')

  def log_event(self, func):
    """
    Decorator function for logging events. This function wraps around the endpoint functions,
    logging the request, response, and latency of each call to the endpoint.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
      start_time = time.time()
      event_name = func.__name__  # extract the event_name
      print(f"appname: {self.app}")
      try:
        if isinstance(self.app, Quart):
          print(f"Request: {QuartRequest}")
          request_data = await QuartRequest.get_json()
          response = await func(
            *args, **kwargs
          )  # Call the function and use its return value as the response
          end_time = time.time()
          latency = end_time - start_time
          data = await self.adapter.extract_data(event_name, QuartRequest,
                                                 response, latency)
  
        elif isinstance(self.app, Flask):
          print(f"Request: {FlaskRequest}")
          request_data = FlaskRequest.get_json()
          response = func(
            *args, **
            kwargs)  # Call the function and use its return value as the response
          end_time = time.time()
          latency = end_time - start_time
          data = await self.adapter.extract_data(event_name, FlaskRequest,
                                                 response, latency)
  
        elif isinstance(self.app, FastAPI):
          response = await func(*args, **kwargs)
          fastRequest = None
          for value in kwargs.values():
            if isinstance(value, Request):
              fastRequest = value
              break
  
          end_time = time.time()
          latency = end_time - start_time
  
          data = await self.adapter.extract_data(event_name, fastRequest,
                                                 response, latency)
      except Exception as e:
        print(f"Error extracting data in log_event: {e}")
        return

      try:
        await self.log_event_post(data)
      except Exception as e:
        print(f"Error posting log event: {e}")
      return response

    return wrapper

  async def log_event_post(self, data):
    try:
      """ Log an event with the provided data. """
      # Construct the payload as a list of objects, one for each event
      payload = [{}]
      # Get the installed version of the SDK
      sdk_version = pkg_resources.get_distribution("fleet-sdk").version
  
      # Add the SDK version
      payload[0]['sdk_version'] = sdk_version
  
      #Add the header data
      payload[0]['headers'] = data.get('headers')  # Add headers
  
      # Add the required fields
      payload[0]['function_name'] = data.get('function_name')
      payload[0]['plugin_analytics_id'] = self.token
      payload[0]['plugin_hostname'] = data.get('plugin_hostname')
      payload[0]['event_time'] = time.time()
  
      # Add endpoint info
      payload[0]['endpoint'] = data.get('endpoint')
      payload[0]['ip_address'] = data.get('ip_address')
      payload[0]['query_params'] = data.get('query_params')
      payload[0]['method'] = data.get('method')
  
      # Add request data
      payload[0]['request_body'] = data.get('request_body')
  
      # Add response data
      payload[0]['response_data'] = data.get('response_data')
  
      # Add response code/size/latency
      payload[0]['response_code'] = data.get('response_code')
      payload[0]['response_size'] = data.get('response_size')
  
      payload[0]['latency'] = data.get('latency')
  
      uri = f"http://{self.host}/log_events/"
      r = requests.post(url=uri, json=payload)
      if self.debug:
        print(f"bot-lens endpoint: {uri}")
        print(f"payload is {payload}")
        print(f"{r.status_code} Response:{r.text}")
    except Exception as e:
        print(f"Error in log_event_post: {e}")
