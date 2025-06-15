include .env
export

run-mlflow:
	mlflow server \
	--backend-store-uri sqlite:///mlflow.db \
	--default-artifact-root ./mlruns \
	--host 127.0.0.1 --port $(MLFLOW_PORT)

ngrok-auth:
	ngrok config add-authtoken $(NGROK_TUNNEL_AUTH)

ngrok-mlflow:
	ngrok http $(MLFLOW_PORT)
