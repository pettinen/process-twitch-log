import toml


license = 'MIT'
package = 'process_twitch_log'

with open('pyproject.toml') as f:
    metadata = toml.load(f)['project']

setup_cfg_parts = [f"""\
[metadata]
name = {metadata['name']}
version = {metadata['version']}
description = {metadata['description']}
author = {metadata['authors'][0]['name']}
author_email = {metadata['authors'][0]['email']}
license = {license}
license_file = {metadata['license']['file']}
url = {metadata['urls']['repository']}

[options]
packages = {package}
"""]

if 'dependencies' in metadata:
    setup_cfg_parts.append("install_requires =\n")
    for dep in metadata['dependencies']:
        setup_cfg_parts.append(f"    {dep}\n")

setup_cfg_parts.append("""
[options.entry_points]
console_scripts =
""")

for script_name, entry_point in metadata['scripts'].items():
    setup_cfg_parts.append(f"    {script_name} = {entry_point}\n")

with open('setup.cfg', 'w') as f:
    f.write(''.join(setup_cfg_parts))

print("Generated setup.cfg successfully.")
