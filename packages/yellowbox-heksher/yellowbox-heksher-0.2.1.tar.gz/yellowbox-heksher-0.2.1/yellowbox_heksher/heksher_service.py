from typing import Any, Dict, Iterable, List, Optional, Sequence, Union

import httpx
import requests  # type: ignore
from docker import DockerClient
from requests import HTTPError, exceptions
from yellowbox.containers import create_and_pull, get_ports
from yellowbox.extras.postgresql import PostgreSQLService
from yellowbox.networks import anonymous_network
from yellowbox.retry import RetrySpec
from yellowbox.subclasses import RunMixin, SingleContainerService
from yellowbox.utils import docker_host_name

try:
    from yellowbox.subclasses import AsyncRunMixin  # async mixins only available in yellowbox 7.1
except ImportError:
    class AsyncRunMixin:  # type: ignore[no-redef]
        # a dummy class we can base the service on
        @classmethod
        async def arun(cls, *args, **kwargs):
            raise NotImplementedError("AsyncRunMixin is only available in yellowbox 7.1")


class HeksherService(SingleContainerService, RunMixin, AsyncRunMixin):
    def __init__(self, docker_client: DockerClient, postgres_image: str = 'postgres:latest',
                 heksher_image: str = 'biocatchltd/heksher:latest', port: int = 0, *,
                 heksher_startup_context_features: Union[str, Sequence[str], None] = None, **kwargs):
        self.heksher_image = heksher_image
        self.docker_client = docker_client

        self.postgres_service = PostgreSQLService(docker_client, image=postgres_image, default_db='heksher')

        heksher_env = {
            'HEKSHER_DB_CONNECTION_STRING': self.postgres_service.container_connection_string("postgres"),
        }
        if isinstance(heksher_startup_context_features, Iterable) \
                and not isinstance(heksher_startup_context_features, str):
            heksher_env['HEKSHER_STARTUP_CONTEXT_FEATURES'] = ';'.join(heksher_startup_context_features)
        elif heksher_startup_context_features is not None:
            heksher_env['HEKSHER_STARTUP_CONTEXT_FEATURES'] = heksher_startup_context_features

        self.heksher = create_and_pull(
            docker_client, heksher_image, publish_all_ports=True, ports={80: port}, detach=True, environment=heksher_env
        )

        self.http_client: Optional[httpx.Client] = None

        self.network = anonymous_network(docker_client)
        self.postgres_service.connect(self.network, aliases=['postgres'])
        self.network.connect(self.heksher, aliases=['heksher'])
        super().__init__(self.heksher, **kwargs)

    def start(self, retry_spec: Optional[RetrySpec] = None):
        self.postgres_service.start()
        self._run_db_migration()
        super().start()
        retry_spec = retry_spec or RetrySpec(attempts=20)
        retry_spec.retry(
            lambda: requests.get(self.local_url + '/api/health', timeout=3).raise_for_status(),  # type: ignore
            (ConnectionError, HTTPError, exceptions.ConnectionError)
        )
        self.http_client = httpx.Client(base_url=self.local_url)
        return self

    async def astart(self, retry_spec: Optional[RetrySpec] = None):
        await self.postgres_service.astart()
        self._run_db_migration()
        super().start()
        retry_spec = retry_spec or RetrySpec(attempts=20)
        await retry_spec.aretry(
            lambda: requests.get(self.local_url + '/api/health', timeout=3).raise_for_status(),  # type: ignore
            (ConnectionError, HTTPError, exceptions.ConnectionError)
        )
        self.http_client = httpx.Client(base_url=self.local_url)
        return self

    def stop(self, signal='SIGKILL'):
        # difference in default signal
        self.http_client.close()
        self.postgres_service.disconnect(self.network)
        self.network.disconnect(self.heksher)
        self.network.remove()
        self.postgres_service.stop(signal)
        super().stop(signal)

    @property
    def heksher_port(self):
        return get_ports(self.heksher)[80]

    @property
    def local_url(self):
        return f'http://127.0.0.1:{self.heksher_port}'

    @property
    def container_url(self):
        return f'http://{docker_host_name}:{self.heksher_port}'

    @property
    def _single_endpoint(self):
        return self.heksher

    def get_rules(self, setting_names: Optional[Sequence[str]] = None) -> Dict[str, List[Any]]:
        """
        Args:
            setting_names: the settings names to retrieve the rules for, will retrieve all rules for all settings
            if None
        """
        params: Dict[str, Any] = {
            "include_metadata": True,
        }
        if setting_names is not None:
            params['settings'] = ','.join(setting_names)
        response = self.http_client.get('/api/v1/query', params=params)
        response.raise_for_status()
        result = response.json()
        return {setting: data['rules'] for setting, data in result['settings'].items()}

    def get_setting_names(self) -> List[str]:
        response = self.http_client.get('/api/v1/settings', params={"include_additional_data": False})
        response.raise_for_status()
        result = response.json()
        return [s['name'] for s in result["settings"]]

    def clear_settings(self):
        settings_names = self.get_setting_names()
        for setting_name in settings_names:
            (self.http_client.delete(f'/api/v1/settings/{setting_name}')).raise_for_status()

    def clear_rules(self):
        rules = self.get_rules()
        rules_ids = [rule["rule_id"] for ruleset in rules.values() for rule in ruleset]
        for rule_id in rules_ids:
            (self.http_client.delete(f'/api/v1/rules/{rule_id}')).raise_for_status()

    def clear(self):
        self.clear_rules()
        self.clear_settings()

    def _run_db_migration(self):
        heksher_db_migrator = create_and_pull(
            self.docker_client, self.heksher_image, "alembic upgrade head", publish_all_ports=True, detach=True,
            environment={
                'HEKSHER_DB_CONNECTION_STRING': self.postgres_service.container_connection_string("postgres"),
            }
        )
        self.network.connect(heksher_db_migrator, aliases=['heksher-db-migrator'])
        heksher_db_migrator.start()
        heksher_db_migrator.wait()
        self.network.disconnect(heksher_db_migrator)
        heksher_db_migrator.remove(v=True)
