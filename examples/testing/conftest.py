# Shared pytest fixtures and configuration

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import json
import logging

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)

def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    # Register custom markers
    config.addinivalue_line(
        "markers",
        "unit: marks tests as unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests (medium speed)"
    )
    config.addinivalue_line(
        "markers",
        "e2e: marks tests as end-to-end tests (slow, full system)"
    )
    config.addinivalue_line(
        "markers",
        "smoke: marks tests as smoke tests (quick validation)"
    )
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (longer than 5 seconds)"
    )
    config.addinivalue_line(
        "markers",
        "security: marks tests as security tests"
    )
    config.addinivalue_line(
        "markers",
        "performance: marks tests as performance tests"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test items during collection."""
    for item in items:
        # Auto-mark tests based on file location
        if "unit_tests" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration_tests" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e_tests" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)

        # Auto-mark slow tests (those with 'slow' in the name)
        if "slow" in item.name:
            item.add_marker(pytest.mark.slow)

# Session-scoped fixtures
@pytest.fixture(scope="session")
def test_environment():
    """Determine test environment and provide configuration."""
    env = os.getenv("TEST_ENV", "local")

    config = {
        "local": {
            "database_url": "sqlite:///:memory:",
            "redis_url": "redis://localhost:6379/15",  # Use DB 15 for tests
            "api_base_url": "http://localhost:8000",
            "timeout": 5
        },
        "ci": {
            "database_url": "postgresql://postgres:postgres@postgres:5432/test_db",
            "redis_url": "redis://redis:6379/0",
            "api_base_url": "http://api:8000",
            "timeout": 30
        },
        "docker": {
            "database_url": "postgresql://test_user:test_pass@db:5432/test_db",
            "redis_url": "redis://redis:6379/0",
            "api_base_url": "http://api:8000",
            "timeout": 30
        }
    }

    return {
        "environment": env,
        **config.get(env, config["local"])
    }

@pytest.fixture(scope="session")
def temp_directory():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp(prefix="pytest_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

# Module-scoped fixtures
@pytest.fixture(scope="module")
def sample_config():
    """Provide sample configuration data for tests."""
    return {
        "app": {
            "name": "test-app",
            "version": "1.0.0",
            "debug": True
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "test_db"
        },
        "cache": {
            "type": "redis",
            "host": "localhost",
            "port": 6379
        }
    }

# Function-scoped fixtures
@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    fd, path = tempfile.mkstemp()
    yield path
    os.close(fd)
    os.unlink(path)

@pytest.fixture
def temp_json_file():
    """Create a temporary JSON file with sample data."""
    data = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ],
        "settings": {
            "debug": True,
            "timeout": 30
        }
    }

    fd, path = tempfile.mkstemp(suffix='.json')
    with os.fdopen(fd, 'w') as f:
        json.dump(data, f)

    yield path, data
    os.unlink(path)

@pytest.fixture
def mock_requests():
    """Mock the requests library for testing."""
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post, \
         patch('requests.put') as mock_put, \
         patch('requests.delete') as mock_delete:

        # Configure default responses
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_response.text = "Success"

        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        mock_put.return_value = mock_response
        mock_delete.return_value = mock_response

        yield {
            'get': mock_get,
            'post': mock_post,
            'put': mock_put,
            'delete': mock_delete,
            'response': mock_response
        }

@pytest.fixture
def mock_database():
    """Mock database connection and operations."""
    mock_db = Mock()

    # Mock common database operations
    mock_db.connect.return_value = True
    mock_db.execute.return_value = Mock(fetchall=lambda: [], fetchone=lambda: None)
    mock_db.commit.return_value = None
    mock_db.rollback.return_value = None
    mock_db.close.return_value = None

    return mock_db

@pytest.fixture
def sample_users():
    """Provide sample user data for tests."""
    return [
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "role": "admin",
            "active": True
        },
        {
            "id": 2,
            "name": "Bob Smith",
            "email": "bob@example.com",
            "role": "user",
            "active": True
        },
        {
            "id": 3,
            "name": "Charlie Brown",
            "email": "charlie@example.com",
            "role": "user",
            "active": False
        }
    ]

@pytest.fixture
def mock_logger():
    """Mock logger for testing log operations."""
    mock_log = Mock()

    # Mock all log levels
    mock_log.debug = Mock()
    mock_log.info = Mock()
    mock_log.warning = Mock()
    mock_log.error = Mock()
    mock_log.critical = Mock()

    return mock_log

@pytest.fixture
def environment_variables():
    """Temporarily set environment variables for testing."""
    original_env = os.environ.copy()

    # Set test environment variables
    test_env_vars = {
        "TEST_MODE": "true",
        "LOG_LEVEL": "DEBUG",
        "API_KEY": "test-api-key",
        "DATABASE_URL": "sqlite:///:memory:"
    }

    for key, value in test_env_vars.items():
        os.environ[key] = value

    yield test_env_vars

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)

# Autouse fixtures (run automatically)
@pytest.fixture(autouse=True)
def cleanup_files():
    """Automatically clean up test files after each test."""
    # Setup
    test_files = []

    yield test_files

    # Cleanup
    for file_path in test_files:
        if os.path.exists(file_path):
            try:
                os.unlink(file_path)
            except OSError:
                pass  # File may have been deleted already

@pytest.fixture(autouse=True, scope="function")
def reset_singletons():
    """Reset singleton instances between tests."""
    # This is useful if your code uses singleton patterns
    # Add any singleton reset code here
    yield
    # Reset code would go here

# Parameterized fixtures
@pytest.fixture(params=[
    {"name": "test1", "value": 100},
    {"name": "test2", "value": 200},
    {"name": "test3", "value": 300}
])
def sample_data_parametrized(request):
    """Provide parametrized test data."""
    return request.param

# Async fixtures (for async testing)
@pytest.fixture
async def async_client():
    """Provide async HTTP client for testing."""
    # This would require aiohttp or similar
    # async with aiohttp.ClientSession() as session:
    #     yield session
    pass

# Conditional fixtures
@pytest.fixture
def database_connection(test_environment):
    """Provide database connection only if database is available."""
    if "sqlite" in test_environment["database_url"]:
        # Return mock for SQLite
        return Mock()
    else:
        # Return real connection for other databases
        # This would require actual database connection code
        return Mock()

# Helper functions for tests
def create_test_file(directory: Path, filename: str, content: str = "") -> Path:
    """Helper function to create test files."""
    file_path = directory / filename
    file_path.write_text(content)
    return file_path

def assert_file_exists(file_path: Path):
    """Helper function to assert file existence."""
    assert file_path.exists(), f"File {file_path} does not exist"

def assert_file_contains(file_path: Path, content: str):
    """Helper function to assert file content."""
    assert_file_exists(file_path)
    file_content = file_path.read_text()
    assert content in file_content, f"Content '{content}' not found in {file_path}"

# Test data builders
class TestDataBuilder:
    """Builder class for creating test data."""

    @staticmethod
    def user(name="Test User", email="test@example.com", **kwargs):
        """Build user test data."""
        user = {
            "name": name,
            "email": email,
            "active": True,
            "role": "user"
        }
        user.update(kwargs)
        return user

    @staticmethod
    def server(name="test-server", status="running", **kwargs):
        """Build server test data."""
        server = {
            "name": name,
            "status": status,
            "cpu_usage": 50.0,
            "memory_usage": 60.0,
            "uptime": "1 day"
        }
        server.update(kwargs)
        return server
