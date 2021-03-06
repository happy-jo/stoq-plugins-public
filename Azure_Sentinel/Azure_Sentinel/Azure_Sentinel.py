
#   Copyright 2014-present PUNCH Cyber Analytics Group
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Overview
========

Send reults to Azure Sentinel (Log Analytics Workspace) within a webhook (http) listener
prerequisites: Setup and configure Azure Logic App webhook listener

"""
import aiohttp

from typing import Dict, Optional
from stoq.plugins import ConnectorPlugin
from stoq.helpers import StoqConfigParser
from stoq.data_classes import StoqResponse

class SentinelConnector(ConnectorPlugin):
    
    def __init__(self, config: StoqConfigParser) -> None:
        super().__init__(config)
        
        self.conn_str = config.get('options', 'conn_str', fallback=None)
        if not self.conn_str:
            raise StoqPluginException('conn_str has not been defined')
            
    async def save(self, response: StoqResponse) -> None:
        
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            
            async with session.post(self.conn_str, data=str(response)) as r:
                
                result = await r.text()
                
                
