# Advanced Testing Strategies for DevOps 🚀

Building on testing fundamentals, this guide covers advanced testing techniques essential for DevOps engineers, including integration testing, mocking strategies, API testing, and database testing.

## Table of Contents

- [Integration Testing](#integration-testing)
- [Mocking and Stubbing](#mocking-and-stubbing)
- [API Testing](#api-testing)
- [Database Testing](#database-testing)
- [Testing External Dependencies](#testing-external-dependencies)
- [Performance Testing](#performance-testing)
- [Error Handling and Edge Cases](#error-handling-and-edge-cases)
- [Test Data Management](#test-data-management)

## Integration Testing

Integration testing validates that different components of your system work together correctly. This is crucial for DevOps workflows where multiple services, APIs, and external systems interact.

### **Types of Integration Testing**

#### **1. Component Integration Testing**

Testing interaction between internal components:

```python
# user_service.py
class UserService:
    def __init__(self, db_client, email_service):
        self.db_client = db_client
        self.email_service = email_service

    def create_user(self, user_data):
        # Validate user data
        if not user_data.get('email'):
            raise ValueError("Email is required")

        # Save to database
        user = self.db_client.save_user(user_data)

        # Send welcome email
        self.email_service.send_welcome_email(user['email'], user['name'])

        return user
```

```python
# test_user_service_integration.py
import pytest
from unittest.mock import Mock
from user_service import UserService

class TestUserServiceIntegration:
    def setup_method(self):
        self.mock_db_client = Mock()
        self.mock_email_service = Mock()
        self.user_service = UserService(self.mock_db_client, self.mock_email_service)

    def test_create_user_successful_integration(self):
        # Arrange
        user_data = {"name": "John Doe", "email": "john@example.com"}
        expected_user = {"id": 1, "name": "John Doe", "email": "john@example.com"}

        self.mock_db_client.save_user.return_value = expected_user

        # Act
        result = self.user_service.create_user(user_data)

        # Assert
        assert result == expected_user
        self.mock_db_client.save_user.assert_called_once_with(user_data)
        self.mock_email_service.send_welcome_email.assert_called_once_with(
            "john@example.com", "John Doe"
        )

    def test_create_user_db_failure_no_email_sent(self):
        # Arrange
        user_data = {"name": "John Doe", "email": "john@example.com"}
        self.mock_db_client.save_user.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            self.user_service.create_user(user_data)

        # Verify email service was not called
        self.mock_email_service.send_welcome_email.assert_not_called()
```

#### **2. System Integration Testing**

Testing with real external systems (databases, APIs):

```python
# test_database_integration.py
import pytest
import psycopg2
from contextlib import contextmanager
from user_repository import UserRepository

@pytest.fixture(scope="module")
def test_database():
    """Create test database connection."""
    connection = psycopg2.connect(
        host="localhost",
        database="test_db",
        user="test_user",
        password="test_password"
    )
    yield connection
    connection.close()

@contextmanager
def database_transaction(connection):
    """Context manager for database transactions."""
    cursor = connection.cursor()
    try:
        yield cursor
        connection.rollback()  # Always rollback in tests
    finally:
        cursor.close()

class TestUserRepositoryIntegration:
    def test_create_and_retrieve_user(self, test_database):
        with database_transaction(test_database) as cursor:
            repo = UserRepository(cursor)

            # Create user
            user_data = {"name": "Integration Test User", "email": "test@example.com"}
            user_id = repo.create_user(user_data)

            # Retrieve user
            retrieved_user = repo.get_user(user_id)

            assert retrieved_user["name"] == user_data["name"]
            assert retrieved_user["email"] == user_data["email"]
            assert retrieved_user["id"] == user_id
```

## Mocking and Stubbing

Mocking allows you to isolate units of code by replacing dependencies with controlled fake objects.

### **Using unittest.mock**

```python
from unittest.mock import Mock, patch, MagicMock, call
import requests

# service.py
class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.weather.com"

    def get_temperature(self, city):
        url = f"{self.base_url}/weather"
        params = {"q": city, "key": self.api_key}

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        return data["temperature"]

    def get_forecast(self, city, days=5):
        temperatures = []
        for day in range(days):
            temp = self.get_temperature(city)  # Simplified for example
            temperatures.append(temp)
        return temperatures
```

```python
# test_weather_service.py
import pytest
from unittest.mock import Mock, patch, call
import requests
from weather_service import WeatherService

class TestWeatherService:
    def setup_method(self):
        self.weather_service = WeatherService("test-api-key")

    @patch('weather_service.requests.get')
    def test_get_temperature_success(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {"temperature": 25.5}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Act
        temperature = self.weather_service.get_temperature("London")

        # Assert
        assert temperature == 25.5
        mock_get.assert_called_once_with(
            "https://api.weather.com/weather",
            params={"q": "London", "key": "test-api-key"}
        )

    @patch('weather_service.requests.get')
    def test_get_temperature_api_error(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("API Error")
        mock_get.return_value = mock_response

        # Act & Assert
        with pytest.raises(requests.HTTPError):
            self.weather_service.get_temperature("InvalidCity")

    def test_get_forecast_multiple_calls(self):
        # Use patch as context manager
        with patch.object(self.weather_service, 'get_temperature') as mock_get_temp:
            mock_get_temp.return_value = 20.0

            forecast = self.weather_service.get_forecast("Paris", days=3)

            assert forecast == [20.0, 20.0, 20.0]
            assert mock_get_temp.call_count == 3
            mock_get_temp.assert_has_calls([call("Paris")] * 3)
```

### **pytest-mock Plugin**

```python
# Using pytest-mock (cleaner syntax)
def test_get_temperature_with_pytest_mock(mocker):
    # Arrange
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"temperature": 30.0}
    mock_get = mocker.patch('weather_service.requests.get', return_value=mock_response)

    weather_service = WeatherService("test-key")

    # Act
    temperature = weather_service.get_temperature("Tokyo")

    # Assert
    assert temperature == 30.0
    mock_get.assert_called_once()
```

### **Advanced Mocking Patterns**

```python
class TestAdvancedMocking:
    def test_mock_with_side_effects(self, mocker):
        """Test mocking with different return values for multiple calls."""
        mock_api = mocker.Mock()
        mock_api.get_data.side_effect = [
            {"status": "pending"},
            {"status": "processing"},
            {"status": "completed", "result": "success"}
        ]

        # First call returns pending
        assert mock_api.get_data()["status"] == "pending"
        # Second call returns processing
        assert mock_api.get_data()["status"] == "processing"
        # Third call returns completed
        result = mock_api.get_data()
        assert result["status"] == "completed"
        assert result["result"] == "success"

    def test_mock_context_manager(self, mocker):
        """Test mocking context managers."""
        mock_file = mocker.mock_open(read_data="file content")

        with mocker.patch('builtins.open', mock_file):
            with open('test.txt', 'r') as f:
                content = f.read()

        assert content == "file content"
        mock_file.assert_called_once_with('test.txt', 'r')

    def test_mock_class_methods(self, mocker):
        """Test mocking class methods and attributes."""
        mock_db = mocker.Mock()
        mock_db.connection.execute.return_value = [("user1",), ("user2",)]
        mock_db.connection.fetchall.return_value = [("user1",), ("user2",)]

        # Test the mock
        result = mock_db.connection.execute("SELECT username FROM users")
        users = mock_db.connection.fetchall()

        assert len(users) == 2
        mock_db.connection.execute.assert_called_with("SELECT username FROM users")
```

## API Testing

Testing REST APIs is crucial for validating service integrations and ensuring API contracts are met.

### **Testing with requests-mock**

```bash
pip install requests-mock
```

```python
# api_client.py
import requests

class GitHubClient:
    def __init__(self, token=None):
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})

    def get_user(self, username):
        url = f"{self.base_url}/users/{username}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def create_repo(self, repo_data):
        url = f"{self.base_url}/user/repos"
        response = self.session.post(url, json=repo_data)
        response.raise_for_status()
        return response.json()

    def get_repo_issues(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
```

```python
# test_github_client.py
import pytest
import requests
import requests_mock
from github_client import GitHubClient

class TestGitHubClient:
    def setup_method(self):
        self.client = GitHubClient("test-token")

    def test_get_user_success(self):
        with requests_mock.Mocker() as m:
            # Mock the API response
            user_data = {
                "login": "testuser",
                "id": 12345,
                "name": "Test User",
                "public_repos": 10
            }
            m.get("https://api.github.com/users/testuser", json=user_data)

            # Make the request
            user = self.client.get_user("testuser")

            # Assertions
            assert user["login"] == "testuser"
            assert user["id"] == 12345
            assert user["public_repos"] == 10

    def test_get_user_not_found(self):
        with requests_mock.Mocker() as m:
            # Mock 404 response
            m.get("https://api.github.com/users/nonexistentuser",
                  status_code=404, json={"message": "Not Found"})

            # Test that HTTPError is raised
            with pytest.raises(requests.HTTPError):
                self.client.get_user("nonexistentuser")

    def test_create_repo_success(self):
        with requests_mock.Mocker() as m:
            repo_data = {"name": "test-repo", "description": "Test repository"}
            response_data = {
                "id": 123,
                "name": "test-repo",
                "full_name": "testuser/test-repo",
                "description": "Test repository"
            }

            m.post("https://api.github.com/user/repos",
                   json=response_data, status_code=201)

            created_repo = self.client.create_repo(repo_data)

            assert created_repo["name"] == "test-repo"
            assert created_repo["id"] == 123

            # Verify request was made correctly
            assert m.last_request.json() == repo_data
            assert "Authorization" in m.last_request.headers

    def test_api_rate_limiting(self):
        with requests_mock.Mocker() as m:
            # Mock rate limit response
            m.get("https://api.github.com/users/testuser",
                  status_code=403,
                  json={"message": "API rate limit exceeded"},
                  headers={"X-RateLimit-Remaining": "0"})

            with pytest.raises(requests.HTTPError) as exc_info:
                self.client.get_user("testuser")

            assert exc_info.value.response.status_code == 403
```

### **API Schema Validation**

```bash
pip install jsonschema
```

```python
# test_api_schema.py
import jsonschema
from jsonschema import validate

# Define expected API response schema
USER_SCHEMA = {
    "type": "object",
    "properties": {
        "login": {"type": "string"},
        "id": {"type": "integer"},
        "name": {"type": ["string", "null"]},
        "email": {"type": ["string", "null"]},
        "public_repos": {"type": "integer", "minimum": 0}
    },
    "required": ["login", "id", "public_repos"]
}

def test_api_response_schema_validation():
    with requests_mock.Mocker() as m:
        user_data = {
            "login": "testuser",
            "id": 12345,
            "name": "Test User",
            "email": "test@example.com",
            "public_repos": 15
        }
        m.get("https://api.github.com/users/testuser", json=user_data)

        client = GitHubClient()
        user = client.get_user("testuser")

        # Validate response matches expected schema
        validate(instance=user, schema=USER_SCHEMA)

def test_api_response_invalid_schema():
    with requests_mock.Mocker() as m:
        invalid_user_data = {
            "login": "testuser",
            # Missing required "id" field
            "name": "Test User",
            "public_repos": -5  # Invalid negative value
        }
        m.get("https://api.github.com/users/testuser", json=invalid_user_data)

        client = GitHubClient()
        user = client.get_user("testuser")

        # This should raise a validation error
        with pytest.raises(jsonschema.exceptions.ValidationError):
            validate(instance=user, schema=USER_SCHEMA)
```

## Database Testing

Testing database operations requires careful setup and teardown to maintain test isolation.

### **PostgreSQL Testing Example**

```python
# database.py
import psycopg2
from contextlib import contextmanager

class UserDatabase:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    @contextmanager
    def get_connection(self):
        conn = psycopg2.connect(self.connection_string)
        try:
            yield conn
        finally:
            conn.close()

    def create_user(self, user_data):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                    (user_data["name"], user_data["email"])
                )
                user_id = cursor.fetchone()[0]
                conn.commit()
                return user_id
            except Exception:
                conn.rollback()
                raise

    def get_user(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "name": row[1], "email": row[2]}
            return None

    def delete_user(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
```

```python
# test_database.py
import pytest
import psycopg2
from database import UserDatabase

@pytest.fixture(scope="session")
def test_database():
    """Create test database and tables."""
    # Create test database connection
    conn = psycopg2.connect(
        host="localhost",
        database="test_db",
        user="test_user",
        password="test_pass"
    )

    # Create test table
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

    yield conn

    # Cleanup
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS users")
        conn.commit()
    conn.close()

@pytest.fixture
def clean_database(test_database):
    """Clean database before each test."""
    with test_database.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
        test_database.commit()
    yield test_database

@pytest.fixture
def user_db(clean_database):
    """Create UserDatabase instance for testing."""
    return UserDatabase("host=localhost dbname=test_db user=test_user password=test_pass")

class TestUserDatabase:
    def test_create_user_success(self, user_db):
        # Arrange
        user_data = {"name": "John Doe", "email": "john@example.com"}

        # Act
        user_id = user_db.create_user(user_data)

        # Assert
        assert user_id is not None
        assert isinstance(user_id, int)
        assert user_id > 0

    def test_get_user_exists(self, user_db):
        # Arrange - create user first
        user_data = {"name": "Jane Doe", "email": "jane@example.com"}
        user_id = user_db.create_user(user_data)

        # Act
        retrieved_user = user_db.get_user(user_id)

        # Assert
        assert retrieved_user is not None
        assert retrieved_user["id"] == user_id
        assert retrieved_user["name"] == "Jane Doe"
        assert retrieved_user["email"] == "jane@example.com"

    def test_get_user_not_exists(self, user_db):
        # Act
        retrieved_user = user_db.get_user(999)

        # Assert
        assert retrieved_user is None

    def test_delete_user_success(self, user_db):
        # Arrange
        user_data = {"name": "Delete Me", "email": "delete@example.com"}
        user_id = user_db.create_user(user_data)

        # Act
        deleted = user_db.delete_user(user_id)

        # Assert
        assert deleted is True
        assert user_db.get_user(user_id) is None

    def test_create_user_duplicate_email(self, user_db):
        # Arrange
        user_data = {"name": "User One", "email": "duplicate@example.com"}
        user_db.create_user(user_data)

        # Act & Assert
        duplicate_user = {"name": "User Two", "email": "duplicate@example.com"}
        with pytest.raises(psycopg2.IntegrityError):
            user_db.create_user(duplicate_user)
```

## Testing External Dependencies

When testing code that depends on external services, use various strategies to make tests reliable and fast.

### **Testing with Docker Containers**

```python
# conftest.py
import pytest
import docker
import time
import psycopg2

@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for testing."""
    client = docker.from_env()

    # Start PostgreSQL container
    container = client.containers.run(
        "postgres:13",
        environment={
            "POSTGRES_DB": "test_db",
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_pass"
        },
        ports={"5432/tcp": 5433},
        detach=True,
        remove=True
    )

    # Wait for PostgreSQL to be ready
    max_retries = 30
    for _ in range(max_retries):
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5433,
                database="test_db",
                user="test_user",
                password="test_pass"
            )
            conn.close()
            break
        except psycopg2.OperationalError:
            time.sleep(1)
    else:
        container.stop()
        raise Exception("PostgreSQL container failed to start")

    yield {
        "host": "localhost",
        "port": 5433,
        "database": "test_db",
        "user": "test_user",
        "password": "test_pass"
    }

    # Cleanup
    container.stop()
```

## Performance Testing

Basic performance testing to ensure your DevOps scripts meet performance requirements.

```python
# performance_test.py
import pytest
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def test_api_response_time():
    """Test that API calls complete within acceptable time."""
    start_time = time.time()

    # Make API call
    client = GitHubClient()
    user = client.get_user("octocat")

    end_time = time.time()
    response_time = end_time - start_time

    # Assert response time is under 2 seconds
    assert response_time < 2.0
    assert user["login"] == "octocat"

def test_concurrent_api_calls():
    """Test handling multiple concurrent API calls."""
    client = GitHubClient()
    usernames = ["octocat", "defunkt", "pjhyett"]

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_username = {
            executor.submit(client.get_user, username): username
            for username in usernames
        }

        results = {}
        for future in as_completed(future_to_username):
            username = future_to_username[future]
            try:
                user_data = future.result()
                results[username] = user_data
            except Exception as exc:
                pytest.fail(f"User {username} generated exception: {exc}")

    end_time = time.time()
    total_time = end_time - start_time

    # All requests should complete
    assert len(results) == 3
    # Concurrent requests should be faster than sequential
    assert total_time < 5.0  # Should be much faster than 3 sequential calls

@pytest.mark.parametrize("data_size", [100, 1000, 10000])
def test_data_processing_performance(data_size):
    """Test data processing performance with different data sizes."""
    # Generate test data
    test_data = [{"id": i, "value": f"item_{i}"} for i in range(data_size)]

    start_time = time.time()

    # Process data (example: filter and transform)
    processed_data = [
        {"id": item["id"], "processed_value": item["value"].upper()}
        for item in test_data
        if item["id"] % 2 == 0
    ]

    end_time = time.time()
    processing_time = end_time - start_time

    # Performance expectations based on data size
    if data_size <= 100:
        assert processing_time < 0.01  # 10ms
    elif data_size <= 1000:
        assert processing_time < 0.1   # 100ms
    else:
        assert processing_time < 1.0   # 1 second

    # Verify processing correctness
    expected_count = data_size // 2
    assert len(processed_data) == expected_count
```

## Next Steps

After mastering advanced testing concepts, continue with:

1. **[CI/CD Testing](ci_cd_testing.md)** - Automated testing in pipelines
2. **Security Testing** - Testing for vulnerabilities and security issues
3. **Load Testing** - Testing system performance under load
4. **Contract Testing** - API contract testing and schema validation

---

_Advanced testing ensures your DevOps automation is reliable, maintainable, and production-ready._
