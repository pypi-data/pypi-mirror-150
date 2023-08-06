from pathlib import Path
from shutil import rmtree, copytree
from requests import get

node_modules = Path(__file__).parent / "node_modules"
static = Path(__file__).parent / "jupyterlab_itables" / "static"

if static.exists():
    rmtree(static)

for library in ['jquery', 'datatables.net', 'datatables.net-dt']:
    copytree(node_modules / library, static / library)

# jquery.dataTables.min.mjs will be included in the npm module version 1.12
dt_mjs = get('https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.mjs').content
(static / 'datatables.net' / 'js' / 'jquery.dataTables.min.mjs').write_bytes(dt_mjs)
