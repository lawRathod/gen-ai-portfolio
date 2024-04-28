start: buildSecrets
	# starts the streamlit app
	python -m streamlit run --server.headless True app.py

deps:
	# installs the dependencies
	pip install -r requirements.txt

buildSecrets:
	# creates .streamlit/secrets.toml file using the environment variables
	bash -c ./buildSecrets.sh

start_jupyter:
	# starts the jupyter notebook
	jupyter notebook Task_1_Test_Cases.ipynb