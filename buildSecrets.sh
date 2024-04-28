USER=$(whoami)
echo "
[connections.main]
url = \"sqlite:////Users/${USER}/.toduh/data.sqlite\"" > .streamlit/secrets.toml