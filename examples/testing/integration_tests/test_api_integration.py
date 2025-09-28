# Integration Tests for DevOps API Client

import pytest
import requests
import requests_mock
import json
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_client import DevOpsAPIClient

class TestDevOpsAPIClientIntegration:
    """Integration tests for DevOps API Client."""

    def setup_method(self):
        """Setup for each test method."""
        self.base_url = "https://api.devops.example.com"
        self.api_key = "test-api-key-123"
        self.client = DevOpsAPIClient(self.base_url, self.api_key)

    def test_client_initialization(self):
        """Test client initialization and configuration."""
        assert self.client.base_url == self.base_url
        assert self.client.timeout == 30
        assert 'Authorization' in self.client.session.headers
        assert self.client.session.headers['Authorization'] == f'Bearer {self.api_key}'
        assert self.client.session.headers['Content-Type'] == 'application/json'

    def test_get_server_status_success(self):
        """Test getting server status successfully."""
        with requests_mock.Mocker() as m:
            server_id = "server-001"
            mock_response = {
                "server_id": server_id,
                "status": "running",
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "uptime": "5 days, 3 hours"
            }

            m.get(f"{self.base_url}/servers/{server_id}/status", json=mock_response)

            result = self.client.get_server_status(server_id)

            assert result is not None
            assert result["server_id"] == server_id
            assert result["status"] == "running"
            assert result["cpu_usage"] == 45.2

    def test_get_server_status_not_found(self):
        """Test getting server status when server not found."""
        with requests_mock.Mocker() as m:
            server_id = "nonexistent-server"

            m.get(f"{self.base_url}/servers/{server_id}/status",
                  status_code=404,
                  json={"error": "Server not found"})

            result = self.client.get_server_status(server_id)

            assert result is None

    def test_deploy_application_success(self):
        """Test successful application deployment."""
        with requests_mock.Mocker() as m:
            app_config = {
                "name": "my-web-app",
                "image": "nginx:latest",
                "replicas": 3,
                "port": 80
            }

            mock_response = {
                "deployment_id": "deploy-12345",
                "status": "started",
                "estimated_time": "5 minutes"
            }

            m.post(f"{self.base_url}/deployments", json=mock_response, status_code=201)

            result = self.client.deploy_application(app_config)

            assert result is not None
            assert result["deployment_id"] == "deploy-12345"
            assert result["status"] == "started"

            # Verify the request payload
            assert m.last_request.json() == app_config

    def test_deploy_application_validation_error(self):
        """Test application deployment with validation error."""
        with requests_mock.Mocker() as m:
            app_config = {
                "name": "",  # Invalid: empty name
                "image": "nginx:latest"
            }

            m.post(f"{self.base_url}/deployments",
                   status_code=400,
                   json={"error": "Invalid configuration", "details": "Name cannot be empty"})

            result = self.client.deploy_application(app_config)

            assert result is None

    def test_get_deployment_logs_success(self):
        """Test getting deployment logs successfully."""
        with requests_mock.Mocker() as m:
            deployment_id = "deploy-12345"
            mock_logs = {
                "logs": [
                    "2023-01-01 10:00:00 - Starting deployment...",
                    "2023-01-01 10:01:00 - Pulling image nginx:latest...",
                    "2023-01-01 10:02:00 - Creating containers...",
                    "2023-01-01 10:03:00 - Deployment completed successfully"
                ]
            }

            m.get(f"{self.base_url}/deployments/{deployment_id}/logs", json=mock_logs)

            result = self.client.get_deployment_logs(deployment_id)

            assert result is not None
            assert len(result) == 4
            assert "Starting deployment" in result[0]
            assert "completed successfully" in result[3]

    def test_scale_service_success(self):
        """Test successful service scaling."""
        with requests_mock.Mocker() as m:
            service_name = "web-service"
            replicas = 5

            m.patch(f"{self.base_url}/services/{service_name}/scale", status_code=200)

            result = self.client.scale_service(service_name, replicas)

            assert result is True
            assert m.last_request.json() == {"replicas": replicas}

    def test_scale_service_invalid_replicas(self):
        """Test service scaling with invalid replica count."""
        with requests_mock.Mocker() as m:
            service_name = "web-service"
            replicas = -1  # Invalid

            m.patch(f"{self.base_url}/services/{service_name}/scale",
                    status_code=400,
                    json={"error": "Invalid replica count"})

            result = self.client.scale_service(service_name, replicas)

            assert result is False

    def test_get_metrics_success(self):
        """Test getting service metrics successfully."""
        with requests_mock.Mocker() as m:
            service_name = "api-service"
            time_range = "24h"

            mock_metrics = {
                "service": service_name,
                "time_range": time_range,
                "metrics": {
                    "requests_per_second": 150.5,
                    "avg_response_time": 0.245,
                    "error_rate": 0.002,
                    "cpu_usage": 45.7,
                    "memory_usage": 512.3
                }
            }

            m.get(f"{self.base_url}/metrics/{service_name}", json=mock_metrics)

            result = self.client.get_metrics(service_name, time_range)

            assert result is not None
            assert result["service"] == service_name
            assert "metrics" in result
            assert result["metrics"]["requests_per_second"] == 150.5

            # Verify query parameters
            assert m.last_request.qs == {"range": [time_range]}

    def test_create_backup_success(self):
        """Test successful backup creation."""
        with requests_mock.Mocker() as m:
            resource_id = "database-001"
            backup_type = "full"

            mock_response = {
                "job_id": "backup-job-789",
                "status": "queued",
                "estimated_duration": "30 minutes"
            }

            m.post(f"{self.base_url}/backups", json=mock_response, status_code=201)

            result = self.client.create_backup(resource_id, backup_type)

            assert result == "backup-job-789"

            # Verify request payload
            expected_payload = {"resource_id": resource_id, "type": backup_type}
            assert m.last_request.json() == expected_payload

    def test_get_backup_status_success(self):
        """Test getting backup status successfully."""
        with requests_mock.Mocker() as m:
            job_id = "backup-job-789"

            mock_status = {
                "job_id": job_id,
                "status": "completed",
                "progress": 100,
                "start_time": "2023-01-01 10:00:00",
                "end_time": "2023-01-01 10:25:00",
                "backup_size": "2.5 GB"
            }

            m.get(f"{self.base_url}/backups/{job_id}/status", json=mock_status)

            result = self.client.get_backup_status(job_id)

            assert result is not None
            assert result["job_id"] == job_id
            assert result["status"] == "completed"
            assert result["progress"] == 100

class TestDevOpsAPIClientErrorHandling:
    """Test error handling scenarios for DevOps API Client."""

    def setup_method(self):
        """Setup for each test method."""
        self.client = DevOpsAPIClient("https://api.devops.example.com", "test-key")

    def test_network_timeout(self):
        """Test handling of network timeout."""
        with requests_mock.Mocker() as m:
            m.get(requests_mock.ANY, exc=requests.exceptions.ConnectTimeout)

            result = self.client.get_server_status("server-001")
            assert result is None

    def test_connection_error(self):
        """Test handling of connection error."""
        with requests_mock.Mocker() as m:
            m.get(requests_mock.ANY, exc=requests.exceptions.ConnectionError)

            result = self.client.get_server_status("server-001")
            assert result is None

    def test_http_500_error(self):
        """Test handling of HTTP 500 error."""
        with requests_mock.Mocker() as m:
            m.get(requests_mock.ANY, status_code=500, json={"error": "Internal server error"})

            result = self.client.get_server_status("server-001")
            assert result is None

    def test_invalid_json_response(self):
        """Test handling of invalid JSON response."""
        with requests_mock.Mocker() as m:
            m.get(requests_mock.ANY, text="Invalid JSON response")

            with pytest.raises(requests.exceptions.JSONDecodeError):
                self.client.get_server_status("server-001")

class TestDevOpsAPIClientAuthentication:
    """Test authentication scenarios for DevOps API Client."""

    def test_authentication_headers(self):
        """Test that authentication headers are properly set."""
        api_key = "super-secret-key"
        client = DevOpsAPIClient("https://api.example.com", api_key)

        assert client.session.headers['Authorization'] == f'Bearer {api_key}'
        assert client.session.headers['Content-Type'] == 'application/json'
        assert 'DevOps-Python-Client' in client.session.headers['User-Agent']

    def test_unauthorized_request(self):
        """Test handling of unauthorized (401) response."""
        with requests_mock.Mocker() as m:
            m.get(requests_mock.ANY,
                  status_code=401,
                  json={"error": "Unauthorized", "message": "Invalid API key"})

            client = DevOpsAPIClient("https://api.example.com", "invalid-key")
            result = client.get_server_status("server-001")

            assert result is None

# Fixtures for integration testing
@pytest.fixture
def api_client():
    """Fixture to provide API client instance."""
    return DevOpsAPIClient("https://api.devops.example.com", "test-api-key")

@pytest.fixture
def mock_server_response():
    """Fixture to provide mock server response."""
    return {
        "server_id": "server-001",
        "status": "running",
        "cpu_usage": 45.2,
        "memory_usage": 67.8,
        "uptime": "5 days, 3 hours"
    }

# Integration test using fixtures
def test_server_monitoring_workflow(api_client, mock_server_response):
    """Test complete server monitoring workflow."""
    with requests_mock.Mocker() as m:
        server_id = "server-001"

        # Mock server status endpoint
        m.get(f"{api_client.base_url}/servers/{server_id}/status",
              json=mock_server_response)

        # Mock metrics endpoint
        mock_metrics = {
            "service": "web-service",
            "metrics": {"cpu_usage": 45.2, "memory_usage": 67.8}
        }
        m.get(f"{api_client.base_url}/metrics/web-service",
              json=mock_metrics)

        # Test workflow
        server_status = api_client.get_server_status(server_id)
        assert server_status["status"] == "running"

        metrics = api_client.get_metrics("web-service")
        assert metrics["metrics"]["cpu_usage"] == 45.2

        # Verify both endpoints were called
        assert len(m.request_history) == 2
