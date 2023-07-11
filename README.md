```bash
# Virtual env
python3.8 -m venv .venv
source .venv/bin/activate
python3.8 -m pip install -r requirements.txt

pip freeze | xargs pip uninstall -y
```