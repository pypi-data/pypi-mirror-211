import os
from typing import Dict, List, Tuple, TypeVar

from jina import Client

from now.app.base.app import JinaNOWApp
from now.constants import (
    ACCESS_PATHS,
    DEMO_NS,
    EXTERNAL_CLIP_HOST,
    NOW_ELASTIC_INDEXER_VERSION,
    NOW_PREPROCESSOR_VERSION,
    Apps,
    DatasetTypes,
    Models,
)
from now.demo_data import AVAILABLE_DATASETS, DemoDataset, DemoDatasetNames
from now.executor.name_to_id_map import name_to_id_map
from now.now_dataclasses import UserInput

JINA_LOG_LEVEL = os.environ.get("JINA_LOG_LEVEL", "DEBUG")
PREPROCESSOR_LOG_LEVEL = os.environ.get("PREPROCESSOR_LOG_LEVEL", JINA_LOG_LEVEL)
INDEXER_LOG_LEVEL = os.environ.get("INDEXER_LOG_LEVEL", JINA_LOG_LEVEL)


class SearchApp(JinaNOWApp):
    def __init__(self):
        super().__init__()

    @property
    def app_name(self) -> str:
        return Apps.SEARCH_APP

    @property
    def is_enabled(self) -> bool:
        return True

    @property
    def description(self) -> str:
        return 'Search app'

    @property
    def required_docker_memory_in_gb(self) -> int:
        return 8

    @property
    def demo_datasets(self) -> Dict[TypeVar, List[DemoDataset]]:
        return AVAILABLE_DATASETS

    @property
    def finetune_datasets(self) -> [Tuple]:
        return DemoDatasetNames.DEEP_FASHION, DemoDatasetNames.BIRD_SPECIES

    def is_demo_available(self, user_input) -> bool:
        if (
            user_input.dataset_type == DatasetTypes.DEMO
            and 'NOW_EXAMPLES' not in os.environ
            and 'NOW_CI_RUN' not in os.environ
        ):
            client = Client(
                host=f'https://{DEMO_NS.format(user_input.dataset_name.split("/")[-1])}.dev.jina.ai'
            )
            try:
                client.post('/dry_run')
            except Exception as e:  # noqa E722
                pass
            return True
        return False

    @staticmethod
    def preprocessor_stub(testing=False) -> Dict:
        return {
            'name': 'preprocessor',
            'needs': 'gateway',
            'uses': f'jinahub+docker://{name_to_id_map.get("NOWPreprocessor")}/{NOW_PREPROCESSOR_VERSION}'
            if not testing
            else 'NOWPreprocessor',
            'jcloud': {
                'autoscale': {
                    'min': 0,
                    'max': 100,
                    'metric': 'concurrency',
                    'target': 1,
                },
                'resources': {'instance': 'C4', 'capacity': 'spot'},
            },
            'env': {'JINA_LOG_LEVEL': PREPROCESSOR_LOG_LEVEL},
        }

    @staticmethod
    def clip_encoder_stub() -> Tuple[Dict, int]:
        return {
            'name': Models.CLIP_MODEL,
            'uses': f'jinahub+docker://CLIPOnnxEncoder/0.8.1-gpu',
            'host': EXTERNAL_CLIP_HOST,
            'port': 443,
            'tls': True,
            'external': True,
            'uses_with': {'access_paths': ACCESS_PATHS, 'name': 'ViT-B-32::openai'},
            'env': {'JINA_LOG_LEVEL': 'DEBUG'},
            'needs': 'preprocessor',
        }, 512

    @staticmethod
    def indexer_stub(
        user_input: UserInput,
        encoder2dim: Dict[str, int],
        testing=False,
    ) -> Dict:
        """Creates indexer stub.

        :param user_input: user input
        :param encoder2dim: maps encoder name to its output dimension
        :param testing: use local executors if True
        """
        document_mappings_list = []

        for encoder, dim in encoder2dim.items():
            document_mappings_list.append(
                [
                    encoder,
                    dim,
                    [
                        user_input.field_names_to_dataclass_fields[
                            index_field.replace('_model', '')
                        ]
                        for index_field, encoders in user_input.model_choices.items()
                        if encoder in encoders
                    ],
                ]
            )
        provision_index = 'yes' if not testing else 'no'
        provision_shards = os.getenv('PROVISION_SHARDS', '1')
        provision_replicas = os.getenv('PROVISION_REPLICAS', '0')

        return {
            'name': 'indexer',
            'needs': list(encoder2dim.keys()),
            'uses': f'jinahub+docker://{name_to_id_map.get("NOWElasticIndexer")}/{NOW_ELASTIC_INDEXER_VERSION}'
            if not testing
            else 'NOWElasticIndexer',
            'uses_with': {
                'document_mappings': document_mappings_list,
            },
            'no_reduce': True,
            'jcloud': {
                'autoscale': {
                    'min': 0,
                    'max': 1,
                    'metric': 'concurrency',
                    'target': 1,
                },
                'labels': {
                    'app': 'indexer',
                    'provision-index': provision_index,
                    'provision-shards': provision_shards,
                    'provision-replicas': provision_replicas,
                    'provision-target-es-cluster': "NOW_DEV_CLUSTER"
                    if 'NOW_CI_RUN' in os.environ
                    else "NOW_PROD_CLUSTER",
                },
                'resources': {'instance': 'C2', 'capacity': 'spot'},
            },
            'env': {'JINA_LOG_LEVEL': INDEXER_LOG_LEVEL},
        }

    def get_executor_stubs(
        self, user_input: UserInput, testing=False, **kwargs
    ) -> List[Dict]:
        """Returns a dictionary of executors to be added in the flow

        :param user_input: user input
        :param testing: use local executors if True
        :return: executors stubs with filled-in env vars
        """
        flow_yaml_executors = [
            self.preprocessor_stub(testing),
        ]

        encoder2dim = {}

        def add_encoders_to_flow(models):
            for model, encoder_stub in models:
                if any(
                    model in user_input.model_choices[f"{field}_model"]
                    for field in user_input.index_fields
                ):
                    encoder, dim = encoder_stub()
                    encoder2dim[encoder['name']] = dim
                    flow_yaml_executors.append(encoder)

        add_encoders_to_flow(
            [
                (Models.CLIP_MODEL, self.clip_encoder_stub),
            ]
        )

        flow_yaml_executors.append(
            self.indexer_stub(
                user_input,
                encoder2dim=encoder2dim,
                testing=testing,
            )
        )

        return flow_yaml_executors

    @property
    def max_request_size(self) -> int:
        """Max number of documents in one request"""
        return 10
