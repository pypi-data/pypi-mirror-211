# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pulsar_data_collection', 'pulsar_data_collection.database_connectors']

package_data = \
{'': ['*']}

install_requires = \
['influxdb-client[async]>=1.36.1,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pydantic>=1.6.2,<2.0.0']

setup_kwargs = {
    'name': 'pulsar-data-collection',
    'version': '0.2.0rc0',
    'description': 'sdk enabling data collection from model serving code for our MPM solution',
    'long_description': '# pulsar_data_collection\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/pulsar-data-collection.svg)](https://pypi.org/project/pulsar-data-collection/)\n[![Package Status](https://img.shields.io/pypi/status/pulsar-data-collection.svg)](https://pypi.org/project/pulsar-data-collection/)\n[![License](https://img.shields.io/pypi/l/pulsar-data-collection.svg)](https://github.com/Rocket-Science-Development/pulsar_data_collection/blob/main/LICENSE)\n[![Coverage](https://codecov.io/github/pandas-dev/pandas/coverage.svg?branch=main)](https://codecov.io/gh/pandas-dev/pandas)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n## What is it?\n\n**pulsar-data-collection** is a package for collecting and pushing data (features, predictions, and metadata) from an inference/prediction Jupyter notebook or Python micro-service serving a ML model (Flask, FastAPI) to a Database. It aims to provide an easy and flexible way to log data point used to perform predictions, prediction, and other relevant metadate informing the context in which the model is perform its predection. Once this data is stored, it will be used to compute metrics in order to provide ML models monitoring using our [pulsar-metrics](https://github.com/Rocket-Science-Development/pulsar_metrics) package. Further demonstration on how these packages are leveraged can found in [pulsar-demo](https://github.com/Rocket-Science-Development/pulsar_demo).\n\nWe currently support writing to InfluxDB v2.6.1, support for other technologies is coming\n\n## Main Features\n\nHere are just a few of the things that pandas does well:\n\n- Collect data related to a model\'s lifecycle in production, i.e, data points, predictions, and metadata\n- Can be used inside a Python inference micro-service or a Jupyter Notebook used to perform predictions\n- Easy and flexible interface that has the ability to integrate with provided support of storage solution as well as the ability to easily integrate with custom storage solutions.\n- Lightweight package to limit the impact on the inference/prediction service performance\n\n## Where to get it\n\nThe source code is currently hosted on GitHub at: [https://github.com/Rocket-Science-Development/pulsar_data_collection](https://github.com/Rocket-Science-Development/pulsar_data_collection)\n\nBinary installers for the latest released version are available at the [Python Package Index (PyPI)](https://pypi.org/project/pulsar-data-collection/)\nInstall Pulsar Data Collection with pip:\n\n```sh\npip install pulsar-data-collection\n```\n\n### Example usage\n\n```python\nimport pickle as pkl\nfrom datetime import datetime as dt\nfrom datetime import timezone\nfrom pathlib import Path\n\nimport pandas as pd\n\nfrom pulsar_data_collection.models import DataWithPrediction, PulseParameters\nfrom pulsar_data_collection.pulse import Pulse\n\n# init paths\nmodel_path = Path("path_to_model")\ninference_dataset = pd.read_csv("path_of_data_for_prediction", header=0)\nreference_data = "path_or_location_reference_data_used_to_train_the_model"\n\nparams = PulseParameters(\n    model_id="model_id",\n    model_version="model_version",\n    data_id="reference_data_id",\n    reference_data_storage=reference_data,\n    target_name="target_feature_name",\n    storage_engine="influxdb",\n    timestamp_column_name="_time",\n    login={\n        "url": "url_influxdb",\n        "token": "mytoken",\n        "org": "pulsarml",\n        "bucket_name": "demo",\n    },\n    other_labels={"timezone": "EST", "reference_dataset": reference_data},\n)\n\npulse = Pulse(data=params)\n\npickle_model = pkl.load(open(model_path, "rb"))\nprediction_simple = pickle_model.predict(inference_dataset)\n\ntime = dt.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")\ncapture_params = DataWithPrediction(\n    data_points=inference_dataset,\n    predictions=pd.DataFrame(prediction_simple, columns=["prediction"]),\n    timestamp=time,\n    features_names=inference_dataset.columns.tolist(),\n)\n\npulse.capture_data(data=capture_params)\n```\n\n## About [PulsarML](https://pulsar.ml/)\n\nPulsarML is a project helping with monitoring your models and gain powerful insights into its performance.\n\nWe released two Open Source packages :\n\n- [pulsar-data-collection](https://github.com/Rocket-Science-Development/pulsar_data_collection) :  lightweight python package enabling data collection of features, predictions and metadata from an ML model serving code/micro-service\n\n- [pulsar-metrics](https://github.com/Rocket-Science-Development/pulsar_metrics) : library for evaluating and monitoring data and concept drift with an extensive set of metrics. It also offers the possibility to use custom metrics defined by the user.\n\nWe also created [pulsar demo](https://github.com/Rocket-Science-Development/pulsar_demo) to display an example use-case showing how to leverage both packages to implement model monitoring and performance management.\n\nWant to interact with the community? join our [slack channel](https://pulsarml.slack.com)\n\nPowered by [Rocket Science Development](https://rocketscience.one/)\n\n\n',
    'author': 'Pulsar team',
    'author_email': 'pulsar@data-rs.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Rocket-Science-Development/pulsar_data_collection',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
