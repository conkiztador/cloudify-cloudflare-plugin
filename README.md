cloudify-cloudflare-plugin
========================

Updates CloudFlare DNS records from cloudify.

## Usage

See `plugin/tests/blueprint/blueprint.yaml` for an example blueprint.

## Tests

To run the plugin tests, the included `dev-requirements.txt` should be installed.

```
pip install -r dev-requirements.txt
python -m unittest plugin.tests.test_plugin
```
