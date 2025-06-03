import mlflow

if __name__ == "__main__":
    # for sanity check
    mlflow.set_tracking_uri("http://localhost:8550")
    run = mlflow.get_run("d5899ca505ee411fa20ecd8f3197cae3")
    print(run)
