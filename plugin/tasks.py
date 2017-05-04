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


# ctx is imported and used in operations
from cloudify import ctx

# put the operation decorator on any function that is a task
from cloudify.decorators import operation

import CloudFlare as cloudflare


CF_CONFIG = 'cloudflare_config'


@operation
def update_record(name, ip, **kwargs):
    # setting node instance runtime property
    ctx.logger.info("name: %s", name)
    ctx.logger.info("ip: %s", ip)

    try:
        config = ctx.node.properties[CF_CONFIG]
    except NonRecoverableError:
        config = ctx.source.node.properties[CF_CONFIG]

    cf = cloudflare.CloudFlare(email=config['email'], token=config['key'])
    zone_name = config['domain_name']
    try:
        params = {'name':zone_name}
        zones = cf.zones.get(params=params)
    except cloudflare.exceptions.CloudFlareAPIError as e:
        ctx.logger.error("Error retrieving zone info from CloudFlare")
        raise

    ctx.logger.info("Found zone: %s", zone_name)

    zone = zones[0]
    zone_id = zone['id']

    record_type = 'A'
    name = '.'.join([name, zone_name])

    try:
        params = {'name': name, 'match':'all', 'type': record_type}
        dns_records = cf.zones.dns_records.get(zone_id, params=params)
    except cloudflare.exceptions.CloudFlareAPIError as e:
        ctx.logger.error("Error getting DNS records from CloudFlare")
        raise

    new_record = {
        'name': name,
        'type': record_type,
        'content': ip,
    }

    for dns_record in dns_records:
        ctx.logger.info("Found existing record: %s = %s", dns_record['name'], dns_record['content'])
        if ip == dns_record['content']:
            ctx.logger.info("Nothing to do.")
            break

        ctx.logger.info("Updating record %s to %s", dns_record['name'], new_record['content'])
        dns_record_id = dns_record['id']
        try:
            dns_record = cf.zones.dns_records.put(zone_id, dns_record_id, data=new_record)
        except cloudflare.exceptions.CloudFlareAPIError as e:
            ctx.logger.error("Error updating DNS record")
            raise

    if not dns_records:
        ctx.logger.info("Creating new record %s = %s", new_record['name'], new_record['content'])
        try:
            dns_record = cf.zones.dns_records.post(zone_id, data=new_record)
        except cloudflare.exceptions.CloudFlareAPIError as e:
            ctx.logger.error("Error creating DNS record")
            raise
