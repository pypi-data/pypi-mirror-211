import base64
import json
import os.path
import sys
from typing import Union

import mlflow
import pyrebase
import requests
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError
from mlflow.entities import Run
from mlflow.tracking import MlflowClient

from .libconfig import libconfig
from .userconfig import userconfig


class Trail:
    ADD_EXPERIMENT_MUTATION = """
        mutation (
            $projectId: String!,
            $parentExperimentId: String!,
            $title: String!,
            $comments: String!,
            $instanceRunParameters: JSONString!,
            $instanceRunMetrics: JSONString!
        ) {
            addExperiment(
                projectId: $projectId,
                parentExperimentId: $parentExperimentId,
                title: $title,
                comments: $comments,
                instanceRuns: {
                    comment: "",
                    parameters: $instanceRunParameters,
                    metrics: $instanceRunMetrics
                }
            ) {
                experiment {
                    id
                    title
                    comments
                    instanceRuns {
                        id
                        comment
                        parameters
                        metrics
                    }
                }
            }
        }
    """

    PUT_ARTIFACT_MUTATION = """
        mutation (
            $experimentId: String!,
            $name: String!,
            $base64Data: String!,
            $tags: [String!]
        ) {
            putArtifact(
                experimentId: $experimentId,
                name: $name,
                base64Data: $base64Data,
                tags: $tags,
            ) {
                artifact {
                    id
                    name
                    contentType
                    size
                    tags
                }
            }
        }
    """

    def __init__(
            self,
            project_alias,
            experiment_title='Unnamed Run',
            parent_experiment_id=None,
            project_id=None,
            username=None,
            password=None
    ):
        userconfig.merge(
            username=username,
            password=password,
            project_alias=project_alias,
            project_id=project_id,
            parent_experiment_id=parent_experiment_id
        )

        token = self._retrieve_jwt_token(
            email=userconfig.username,
            password=userconfig.password
        )
        transport = AIOHTTPTransport(
            libconfig.GQL_ENDPOINT_URL,
            headers={'authorization': f'Bearer {token}'}
        )
        self.client = Client(transport=transport)
        self.project_config = userconfig.project(project_alias)
        self.project_id = self.project_config.id
        self.parent_experiment_id = self.project_config.parent_experiment_id
        self.experiment_title = experiment_title
        self.artifacts = []

    def __enter__(self):
        if mlflow.active_run() is None:
            raise Exception('No active mlflow run found!')

        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        run = mlflow.active_run()
        if run is None:
            raise Exception('No active mlflow run found!')

        # we fetch the run like this because of
        # https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.active_run
        materialized_run = mlflow.get_run(run_id=run.info.run_id)

        if materialized_run:
            self._log_experiment(materialized_run)
            self._upload_artifacts(materialized_run)

    def put_artifact(
            self,
            src:  Union[str, bytes],
            name: str,
            tags: Union[str, list] = None
    ):
        """Queues an artifact for upload to Trail. The artifact is uploaded when
        leaving the `with Trail` block.
        The `src` parameter can be either a string or a bytes object. In case
        of a string, it is assumed to be a path to a file. In case of a bytes
        object, it is assumed to be the raw data of the artifact.

        :param src: The artifact path or bytes to upload
        :param name: The name of the artifact
        :param tags: A single tag or a list of tags
        """

        if isinstance(src, str):
            with open(src, 'rb') as f:
                data = f.read()
        elif isinstance(src, bytes):
            data = src
        else:
            raise ValueError('Artifact source must be of type string or bytes')

        if not tags:
            tags = []
        elif isinstance(tags, str):
            tags = [tags]

        self.artifacts.append((data, name, tags,))

    def _upload_artifact(self, data: bytes, name: str, tags: list):
        self.client.execute(
            document=gql(self.PUT_ARTIFACT_MUTATION),
            variable_values={
                'experimentId': self.parent_experiment_id,
                'name': name,
                'base64Data': base64.b64encode(data).decode(),
                'tags': tags
            }
        )

    def _log_experiment(self, run: Run):
        run_id = run.info.run_id
        tags = {
            k: v for k, v in run.data.tags.items()
            if not k.startswith('mlflow.')
        }
        mlflow_artifacts = [
            artifact.path
            for artifact in MlflowClient().list_artifacts(run_id, 'model')
        ]
        d = {  # noqa: F841
            'run_id': run_id,
            'timestamp': run.info.start_time / 1000.0,
            'user': run.info.user_id,
            'artifacts': mlflow_artifacts,
            'tags': tags
        }

        try:
            result = self.client.execute(
                document=gql(self.ADD_EXPERIMENT_MUTATION),
                variable_values={
                    'projectId': self.project_id,
                    'parentExperimentId': self.parent_experiment_id,
                    'title': self.experiment_title,
                    'comments': '',
                    'instanceRunParameters': json.dumps(run.data.params),
                    'instanceRunMetrics': json.dumps(run.data.metrics)
                }
            )

            experiment_id = result['addExperiment']['experiment']['id']
            self.project_config.update_parent_experiment_id(experiment_id)
            self.parent_experiment_id = experiment_id
        except TransportQueryError:
            print(
                'Error uploading experiment data to Trail. Please contact us '
                'if the problem persists.',
                file=sys.stderr
            )

    def _upload_artifacts(self, run: Run):
        run_id = run.info.run_id

        try:
            # upload cached artifacts
            mlflow_artifacts = MlflowClient().list_artifacts(run_id, 'model')
            for artifact in mlflow_artifacts:
                path = artifact.path
                with open(path, 'rb') as f:
                    self._upload_artifact(
                        data=f.read(),
                        name=os.path.basename(path),
                        tags=['mlflow'],
                    )

            for artifact in self.artifacts:
                data, name, tags = artifact
                self._upload_artifact(
                    data=data,
                    name=name,
                    tags=tags,
                )
        except TransportQueryError:
            print(
                'Error uploading experiment artifacts to Trail. Please contact '
                'us if the problem persists.',
                file=sys.stderr
            )

    @staticmethod
    def _retrieve_jwt_token(email, password):
        firebase = pyrebase.initialize_app({
            'apiKey': libconfig.FIREBASE_API_KEY,
            'authDomain': libconfig.FIREBASE_AUTH_DOMAIN,
            'databaseURL': 'THIS_IS_NOT_USED',
            'storageBucket': 'THIS_IS_NOT_USED',
        })
        auth = firebase.auth()

        try:
            user = auth.sign_in_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as e:
            if e.errno.response.status_code == 400:
                raise Exception('Invalid credentials') from None

            raise e

        return user['idToken']
