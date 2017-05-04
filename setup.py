########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


from setuptools import setup

# Replace the place holders with values for your project

setup(

    # Do not use underscores in the plugin name.
    name='cloudify-cloudflare-plugin',

    version='0.1',
    author='Kieran Spear',
    author_email='kispear@gmail.com',
    description='Cloudify plugin to interact with the CloudFlare API',

    # This must correspond to the actual packages in the plugin.
    packages=['plugin'],

    license='Apache 2.0',
    zip_safe=False,
    install_requires=[
        # Necessary dependency for developing plugins, do not remove!
        "cloudify-plugins-common>=4.0",
        "cloudflare",
    ],
    test_requires=[
        "cloudify-dsl-parser>=4.0"
        "nose"
    ]
)
