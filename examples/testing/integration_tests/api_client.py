# API Client for Integration Testing Examples

import requests
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class DevOpsAPIClient:
    """A sample API client for DevOps operations."""

    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        """
        Initialize the API client.

        Args:
            base_url: The base URL of the API
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'DevOps-Python-Client/1.0'
        })

    def get_server_status(self, server_id: str) -> Optional[Dict]:
        """
        Get the status of a server.

        Args:
            server_id: The ID of the server

        Returns:
            Server status information or None if not found
        """
        url = f"{self.base_url}/servers/{server_id}/status"
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get server status for {server_id}: {e}")
            return None

    def deploy_application(self, app_config: Dict) -> Optional[Dict]:
        """
        Deploy an application.

        Args:
            app_config: Application configuration

        Returns:
            Deployment information or None if failed
        """
        url = f"{self.base_url}/deployments"
        try:
            response = self.session.post(url, json=app_config, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to deploy application: {e}")
            return None

    def get_deployment_logs(self, deployment_id: str) -> Optional[List[str]]:
        """
        Get deployment logs.

        Args:
            deployment_id: The deployment ID

        Returns:
            List of log entries or None if not found
        """
        url = f"{self.base_url}/deployments/{deployment_id}/logs"
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get('logs', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get deployment logs for {deployment_id}: {e}")
            return None

    def scale_service(self, service_name: str, replicas: int) -> bool:
        """
        Scale a service to the specified number of replicas.

        Args:
            service_name: Name of the service to scale
            replicas: Number of replicas

        Returns:
            True if successful, False otherwise
        """
        url = f"{self.base_url}/services/{service_name}/scale"
        payload = {'replicas': replicas}

        try:
            response = self.session.patch(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to scale service {service_name}: {e}")
            return False

    def get_metrics(self, service_name: str, time_range: str = "1h") -> Optional[Dict]:
        """
        Get metrics for a service.

        Args:
            service_name: Name of the service
            time_range: Time range for metrics (e.g., "1h", "24h")

        Returns:
            Metrics data or None if failed
        """
        url = f"{self.base_url}/metrics/{service_name}"
        params = {'range': time_range}

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get metrics for {service_name}: {e}")
            return None

    def create_backup(self, resource_id: str, backup_type: str = "full") -> Optional[str]:
        """
        Create a backup of a resource.

        Args:
            resource_id: ID of the resource to backup
            backup_type: Type of backup ("full" or "incremental")

        Returns:
            Backup job ID or None if failed
        """
        url = f"{self.base_url}/backups"
        payload = {
            'resource_id': resource_id,
            'type': backup_type
        }

        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get('job_id')
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create backup for {resource_id}: {e}")
            return None

    def get_backup_status(self, job_id: str) -> Optional[Dict]:
        """
        Get the status of a backup job.

        Args:
            job_id: The backup job ID

        Returns:
            Backup job status or None if not found
        """
        url = f"{self.base_url}/backups/{job_id}/status"

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get backup status for {job_id}: {e}")
            return None
