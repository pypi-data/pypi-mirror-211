import importlib.resources


version = "0.0.0"

if importlib.resources.is_resource("h2o_mlops_scoring_client", "VERSION"):
    version = importlib.resources.read_text(
        "h2o_mlops_scoring_client", "VERSION"
    ).strip()
