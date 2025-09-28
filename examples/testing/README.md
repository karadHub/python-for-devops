# Python Testing Examples for DevOps 🧪

This directory contains comprehensive testing examples that demonstrate various testing strategies, frameworks, and best practices specifically tailored for DevOps workflows.

## 📁 Directory Structure

```
examples/testing/
├── unit_tests/              # Unit testing examples
│   ├── calculator.py        # Sample module to test
│   ├── test_calculator_unittest.py   # Unit tests using unittest
│   └── test_calculator_pytest.py     # Unit tests using pytest
├── integration_tests/       # Integration testing examples
│   ├── api_client.py        # Sample API client
│   └── test_api_integration.py       # Integration tests
├── automation_scripts/      # CI/CD automation scripts
│   ├── cicd_automation.py   # Complete CI/CD pipeline script
│   └── github_actions_workflow.yml  # GitHub Actions workflow
├── conftest.py             # Shared pytest fixtures
├── pytest.ini             # pytest configuration
└── README.md              # This file
```

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.8+ installed and install the required testing dependencies:

```bash
# Install basic testing tools
pip install pytest pytest-cov pytest-mock

# Install additional dependencies for examples
pip install requests requests-mock coverage
```

### Running the Examples

#### 1. Unit Tests

**Using unittest (built-in framework):**

```bash
# Run unittest tests
cd examples/testing/unit_tests
python test_calculator_unittest.py

# Or using module discovery
python -m unittest discover -s unit_tests -p "test_*.py"
```

**Using pytest (recommended):**

```bash
# Run all unit tests
pytest examples/testing/unit_tests/ -v

# Run specific test file
pytest examples/testing/unit_tests/test_calculator_pytest.py -v

# Run tests with coverage
pytest examples/testing/unit_tests/ --cov=examples/testing/unit_tests --cov-report=html
```

#### 2. Integration Tests

```bash
# Run integration tests
pytest examples/testing/integration_tests/ -v

# Run integration tests with mocking
pytest examples/testing/integration_tests/test_api_integration.py -v

# Run only integration marked tests
pytest -m integration -v
```

#### 3. All Tests with Configuration

```bash
# Run all tests using pytest configuration
pytest examples/testing/

# Run with specific markers
pytest -m "unit or integration" -v

# Run with coverage report
pytest --cov=examples --cov-report=html --cov-report=term-missing
```

### Using the CI/CD Automation Script

The automation script provides a complete CI/CD pipeline for testing:

```bash
# Run complete pipeline
cd examples/testing/automation_scripts
python cicd_automation.py --project-root ../../../

# Run specific steps
python cicd_automation.py --step unit
python cicd_automation.py --step integration
python cicd_automation.py --step security
```

## 📚 Examples Overview

### Unit Tests (`unit_tests/`)

Demonstrates testing of individual functions and classes in isolation:

- **calculator.py**: Simple calculator class with various mathematical operations
- **test_calculator_unittest.py**: Unit tests using Python's built-in `unittest` framework
- **test_calculator_pytest.py**: Unit tests using `pytest` with modern patterns

**Key Concepts Covered:**

- Test fixtures and setup/teardown
- Assertion methods and pytest assertions
- Exception testing
- Parametrized testing
- Test organization and naming conventions

### Integration Tests (`integration_tests/`)

Demonstrates testing of component interactions and external dependencies:

- **api_client.py**: DevOps API client with various operations (server status, deployments, etc.)
- **test_api_integration.py**: Integration tests with mocking and error handling

**Key Concepts Covered:**

- Mocking external dependencies
- HTTP client testing with `requests-mock`
- Error handling and edge cases
- Authentication testing
- Workflow testing

### Automation Scripts (`automation_scripts/`)

Production-ready CI/CD automation examples:

- **cicd_automation.py**: Complete Python script for CI/CD pipeline automation
- **github_actions_workflow.yml**: GitHub Actions workflow for automated testing

**Key Concepts Covered:**

- Dependency installation and management
- Code quality checks (linting, formatting)
- Test execution and reporting
- Security scanning
- Multi-stage pipeline design
- Artifact generation and reporting

## 🛠️ Configuration Files

### pytest.ini

Comprehensive pytest configuration with:

- Test discovery patterns
- Coverage settings
- Custom markers for test categorization
- Output formatting options
- Test filtering and warnings handling

### conftest.py

Shared test fixtures and utilities:

- Environment configuration
- Mock objects and services
- Test data builders
- Temporary file management
- Database and API mocking

## 📊 Test Categories and Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Fast, isolated unit tests
- `@pytest.mark.integration` - Integration tests with external dependencies
- `@pytest.mark.e2e` - End-to-end tests (full system)
- `@pytest.mark.smoke` - Quick validation tests
- `@pytest.mark.slow` - Tests taking longer than 5 seconds
- `@pytest.mark.security` - Security-related tests
- `@pytest.mark.performance` - Performance and benchmark tests

Run specific test categories:

```bash
pytest -m unit                    # Only unit tests
pytest -m "integration or e2e"    # Integration and e2e tests
pytest -m "not slow"              # Exclude slow tests
```

## 🔧 Advanced Usage

### Test Coverage Analysis

```bash
# Generate HTML coverage report
pytest --cov=examples --cov-report=html

# View coverage in terminal
pytest --cov=examples --cov-report=term-missing

# Fail if coverage below threshold
pytest --cov=examples --cov-fail-under=80
```

### Parallel Test Execution

```bash
# Install pytest-xdist for parallel execution
pip install pytest-xdist

# Run tests in parallel
pytest -n 4  # Use 4 CPU cores
pytest -n auto  # Auto-detect CPU cores
```

### Test Debugging

```bash
# Drop into debugger on failure
pytest --pdb

# Stop on first failure
pytest -x

# Show local variables in traceback
pytest -l

# Verbose output with print statements
pytest -s -v
```

### Custom Test Reports

```bash
# Generate JUnit XML for CI/CD
pytest --junitxml=test-results.xml

# Generate JSON report (requires pytest-json-report)
pip install pytest-json-report
pytest --json-report --json-report-file=report.json
```

## 🎯 Best Practices Demonstrated

### 1. Test Organization

- Clear directory structure separating unit and integration tests
- Descriptive test names following naming conventions
- Logical grouping of related tests

### 2. Test Independence

- Each test is independent and can run in isolation
- Proper setup and teardown using fixtures
- No shared state between tests

### 3. Mocking Strategy

- External dependencies are mocked in unit tests
- Integration tests use service mocking where appropriate
- Real external services only in end-to-end tests

### 4. Test Data Management

- Shared test data through fixtures
- Test data builders for complex objects
- Temporary file management for file operations

### 5. Error Testing

- Comprehensive exception testing
- Edge case validation
- Error condition handling

### 6. CI/CD Integration

- Automated test execution in pipelines
- Quality gates based on test results and coverage
- Multi-environment test configurations

## 🚀 Running in CI/CD

### Local Development

```bash
# Quick test run for development
pytest -m "unit and not slow" --tb=short

# Pre-commit testing
python automation_scripts/cicd_automation.py --step lint
python automation_scripts/cicd_automation.py --step unit
```

### GitHub Actions

Copy `github_actions_workflow.yml` to `.github/workflows/` in your repository for automated testing on every push and pull request.

### Docker-based Testing

```bash
# Build test image
docker build -t python-devops-test .

# Run tests in container
docker run --rm python-devops-test pytest examples/testing/
```

## 📖 Learning Path

1. **Start with Unit Tests**: Understand basic testing concepts with the calculator examples
2. **Explore Integration Tests**: Learn mocking and API testing with the API client examples
3. **Study Configuration**: Examine `pytest.ini` and `conftest.py` to understand test organization
4. **Try Automation**: Run the CI/CD automation script to see complete pipeline testing
5. **Implement in Projects**: Apply these patterns to your own DevOps projects

## 🔗 Related Documentation

- [Testing Fundamentals](../../../Intermediate/testing_fundamentals.md)
- [Advanced Testing](../../../Intermediate/advanced_testing.md)
- [CI/CD Testing](../../../Intermediate/ci_cd_testing.md)

## 📞 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the correct directory and Python path is set
2. **Missing Dependencies**: Install all required packages using pip
3. **Permission Errors**: Ensure you have write permissions for test artifacts
4. **Network Issues**: Integration tests may fail if external services are unavailable

### Getting Help

- Check the main [README.md](../../../README.md) for general repository information
- Review test output carefully for error messages
- Use `pytest --tb=long` for detailed error tracebacks
- Enable debug logging with `-s -v` flags

---

_These examples provide a solid foundation for implementing comprehensive testing in your DevOps Python projects. Adapt and extend them based on your specific requirements._
