# -----------------------------------------------------------------------------
# Copyright (C) 2019-2020 The python-ndn authors
#
# This file is part of python-ndn.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------
import time
import logging
import ndn.utils
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import Name, Component, InterestParam

# the global variable below is the channel name.
CHANNEL_ID = "sensor2"
# The global variable below is the path name. Put it simply, this shows where a particular sensor is located
PATH_NAME = "/MQTT/myhome/room1/"

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')


app = NDNApp()


async def main():
    global PATH_NAME, CHANNEL_ID
    i = 0
    while (i<10):
        try:
            timestamp = ndn.utils.timestamp()
            name = Name.from_str(PATH_NAME+CHANNEL_ID) #+ [Component.from_timestamp(timestamp)]
            print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=10000)}')
            data_name, meta_info, content = await app.express_interest(
                name, must_be_fresh=True, can_be_prefix=False, lifetime=10000)

            print(f'Received Data Name: {Name.to_str(data_name)}')
            print(meta_info)
            print(bytes(content) if content else None)
    
        except InterestNack as e:
            print(f'Nacked with reason={e.reason}')
        except InterestTimeout:
            print(f'Timeout')
        except InterestCanceled:
            print(f'Canceled')
        except ValidationFailure:
            print(f'Data failed to validate')
        finally:
            #app.shutdown()
            i=i+1
            time.sleep(6)
    app.shutdown()
        
    """try:
        timestamp = ndn.utils.timestamp()
        name = Name.from_str(PATH_NAME+CHANNEL_ID) #+ [Component.from_timestamp(timestamp)]
        print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=10000)}')
        data_name, meta_info, content = await app.express_interest(
            name, must_be_fresh=True, can_be_prefix=False, lifetime=10000)

        print(f'Received Data Name: {Name.to_str(data_name)}')
        print(meta_info)
        printsensor2(bytes(content) if content else None)
    except InterestNack as e:
        print(f'Nacked with reason={e.reason}')
    except InterestTimeout:
        print(f'Timeout')
    except InterestCanceled:
        print(f'Canceled')
    except ValidationFailure:
        print(f'Data failed to validate')
    finally:
        app.shutdown()"""



if __name__ == '__main__':
    app.run_forever(after_start=main())