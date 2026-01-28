# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Apache 2.0
#
#      Copyright 2026. ThingsBoard
#  #
#      Licensed under the Apache License, Version 2.0 (the "License");
#      you may not use this file except in compliance with the License.
#      You may obtain a copy of the License at
#  #
#          http://www.apache.org/licenses/LICENSE-2.0
#  #
#      Unless required by applicable law or agreed to in writing, software
#      distributed under the License is distributed on an "AS IS" BASIS,
#      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#      See the License for the specific language governing permissions and
#      limitations under the License.
#

"""
`thingsboard_sdk.tb_device_mqtt`
================================================================================

ThingsBoard CircuitPython client SDK


* Author(s): Vitalii Bidochka

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""

from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException

from sdk_core.device_mqtt import TBDeviceMqttClientBase
from thingsboard_sdk.provision_client import ProvisionClient

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/samson0v/CircuitPython_thingsboard-client-sdk.git"


class TBDeviceMqttClient(TBDeviceMqttClientBase):
    def __init__(
        self,
        host,
        port=1883,
        access_token=None,
        quality_of_service=None,
        client_id=None,
        chunk_size=0,
    ):
        super().__init__(host, port, access_token, quality_of_service, client_id, chunk_size)
        client = MQTT(
            broker=self._host,
            port=self._port,
            client_id=self._client_id,
            username=self._access_token,
            password="pswd",
            keep_alive=120,
        )
        self.set_client(client)

    def connect(self):
        try:
            response = self._client.connect()
            self._client.add_topic_callback("#", self.all_subscribed_topics_callback)

            self.__subscribe_all_required_topics()

            self.connected = True
            return response
        except MMQTTException as e:
            self.connected = False
            print(f"MQTT connection error: {e}")
        except Exception as e:
            self.connected = False
            print(f"Unexpected connection error: {e}", e)

    @staticmethod
    def provision(host, port, provision_request):
        provision_client = ProvisionClient(
            host=host, port=port, provision_request=provision_request
        )
        provision_client.provision()

        if provision_client.credentials:
            print("Provisioning successful. Credentilas obtained.")
            return provision_client.credentials
        else:
            print("Provisioning failed. No credentials obtained.")
            return None
