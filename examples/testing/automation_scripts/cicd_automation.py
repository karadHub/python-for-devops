# CI/CD Automation Scripts for Testing

import os
import subprocess
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Optional

class CICDAutomation:
    """Automation scripts for CI/CD pipeline testing."""

    def __init__(self, project_root: str):
        """
        Initialize CI/CD automation.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root)
        self.test_results = {}

    def run_command(self, command: str, cwd: Optional[str] = None) -> Dict:
        """
        Run a shell command and return the result.

        Args:
            command: Command to execute
            cwd: Working directory for command execution

        Returns:
            Dictionary with command results
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': command
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'returncode': -1,
                'stdout': '',
                'stderr': 'Command timed out after 5 minutes',
                'command': command
            }
        except Exception as e:
            return {
                'success': False,
                'returncode': -1,
                'stdout': '',
                'stderr': str(e),
                'command': command
            }

    def install_dependencies(self) -> bool:
        """
        Install project dependencies.

        Returns:
            True if successful, False otherwise
        """
        print("📦 Installing dependencies...")

        # Check if requirements.txt exists
        req_file = self.project_root / "requirements.txt"
        if not req_file.exists():
            print("⚠️  requirements.txt not found")
            return True

        # Install dependencies
        result = self.run_command(f"{sys.executable} -m pip install -r requirements.txt")

        if result['success']:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result['stderr']}")
            return False

    def install_test_dependencies(self) -> bool:
        """
        Install test dependencies.

        Returns:
            True if successful, False otherwise
        """
        print("🧪 Installing test dependencies...")

        test_deps = [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "requests-mock>=1.10.0",
            "coverage>=7.0.0"
        ]

        for dep in test_deps:
            result = self.run_command(f"{sys.executable} -m pip install {dep}")
            if not result['success']:
                print(f"❌ Failed to install {dep}: {result['stderr']}")
                return False

        print("✅ Test dependencies installed successfully")
        return True

    def run_linting(self) -> bool:
        """
        Run code linting checks.

        Returns:
            True if all linting passes, False otherwise
        """
        print("🔍 Running linting checks...")

        # Install linting tools
        linting_tools = ["flake8", "black", "isort"]
        for tool in linting_tools:
            result = self.run_command(f"{sys.executable} -m pip install {tool}")
            if not result['success']:
                print(f"⚠️  Could not install {tool}")

        # Run black formatting check
        print("  🔸 Checking code formatting with black...")
        result = self.run_command("black --check --diff .")
        if not result['success']:
            print(f"❌ Code formatting issues found:\n{result['stdout']}")
            self.test_results['linting'] = {'black': False}
        else:
            print("✅ Code formatting is correct")
            self.test_results['linting'] = {'black': True}

        # Run flake8 linting
        print("  🔸 Running flake8 linting...")
        flake8_result = self.run_command("flake8 --max-line-length=88 --ignore=E203,W503 .")
        if not flake8_result['success'] and flake8_result['stdout']:
            print(f"❌ Linting issues found:\n{flake8_result['stdout']}")
            self.test_results['linting']['flake8'] = False
            return False
        else:
            print("✅ No linting issues found")
            self.test_results['linting']['flake8'] = True

        return True

    def run_unit_tests(self) -> bool:
        """
        Run unit tests with coverage.

        Returns:
            True if all tests pass, False otherwise
        """
        print("🧪 Running unit tests...")

        # Find test directories
        test_paths = []
        for pattern in ["tests/", "test/", "*/test_*.py", "*/tests/"]:
            matches = list(self.project_root.glob(pattern))
            test_paths.extend(matches)

        if not test_paths:
            print("⚠️  No test directories found")
            return True

        # Run pytest with coverage
        test_command = (
            f"{sys.executable} -m pytest "
            f"--cov=. "
            f"--cov-report=term-missing "
            f"--cov-report=xml "
            f"--cov-report=html "
            f"--junitxml=test-results.xml "
            f"-v"
        )

        result = self.run_command(test_command)

        if result['success']:
            print("✅ All unit tests passed")
            self.test_results['unit_tests'] = True

            # Extract coverage information
            if 'TOTAL' in result['stdout']:
                coverage_line = [line for line in result['stdout'].split('\n') if 'TOTAL' in line]
                if coverage_line:
                    print(f"📊 {coverage_line[0]}")

            return True
        else:
            print(f"❌ Unit tests failed:\n{result['stdout']}\n{result['stderr']}")
            self.test_results['unit_tests'] = False
            return False

    def run_integration_tests(self) -> bool:
        """
        Run integration tests.

        Returns:
            True if all tests pass, False otherwise
        """
        print("🔗 Running integration tests...")

        # Look for integration test markers or directories
        integration_command = (
            f"{sys.executable} -m pytest "
            f"-m integration "
            f"--tb=short "
            f"-v"
        )

        result = self.run_command(integration_command)

        if result['success'] or "no tests collected" in result['stdout'].lower():
            print("✅ Integration tests completed successfully")
            self.test_results['integration_tests'] = True
            return True
        else:
            print(f"❌ Integration tests failed:\n{result['stdout']}\n{result['stderr']}")
            self.test_results['integration_tests'] = False
            return False

    def run_security_checks(self) -> bool:
        """
        Run security checks on dependencies and code.

        Returns:
            True if no security issues found, False otherwise
        """
        print("🔒 Running security checks...")

        # Install security tools
        security_tools = ["safety", "bandit"]
        for tool in security_tools:
            install_result = self.run_command(f"{sys.executable} -m pip install {tool}")
            if not install_result['success']:
                print(f"⚠️  Could not install {tool}")
                continue

        # Run safety check for known vulnerabilities
        print("  🔸 Checking for known vulnerabilities...")
        safety_result = self.run_command("safety check --json")
        if not safety_result['success'] and safety_result['returncode'] != 0:
            print(f"❌ Security vulnerabilities found:\n{safety_result['stdout']}")
            self.test_results['security'] = {'safety': False}
        else:
            print("✅ No known vulnerabilities found")
            self.test_results['security'] = {'safety': True}

        # Run bandit for security issues in code
        print("  🔸 Checking code for security issues...")
        bandit_result = self.run_command("bandit -r . -f json")
        if bandit_result['success']:
            try:
                bandit_data = json.loads(bandit_result['stdout'])
                if bandit_data.get('results'):
                    print(f"❌ Security issues found in code: {len(bandit_data['results'])} issues")
                    self.test_results['security']['bandit'] = False
                else:
                    print("✅ No security issues found in code")
                    self.test_results['security']['bandit'] = True
            except json.JSONDecodeError:
                print("⚠️  Could not parse bandit results")
                self.test_results['security']['bandit'] = True

        return all(self.test_results.get('security', {}).values())

    def generate_test_report(self) -> Dict:
        """
        Generate a comprehensive test report.

        Returns:
            Test report dictionary
        """
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'project_root': str(self.project_root),
            'results': self.test_results,
            'summary': {
                'total_checks': 0,
                'passed_checks': 0,
                'failed_checks': 0,
                'success_rate': 0.0
            }
        }

        # Calculate summary statistics
        for category, results in self.test_results.items():
            if isinstance(results, bool):
                report['summary']['total_checks'] += 1
                if results:
                    report['summary']['passed_checks'] += 1
                else:
                    report['summary']['failed_checks'] += 1
            elif isinstance(results, dict):
                for check, result in results.items():
                    report['summary']['total_checks'] += 1
                    if result:
                        report['summary']['passed_checks'] += 1
                    else:
                        report['summary']['failed_checks'] += 1

        if report['summary']['total_checks'] > 0:
            report['summary']['success_rate'] = (
                report['summary']['passed_checks'] /
                report['summary']['total_checks'] * 100
            )

        return report

    def save_test_report(self, filename: str = "test-report.json"):
        """
        Save test report to file.

        Args:
            filename: Name of the report file
        """
        report = self.generate_test_report()

        report_file = self.project_root / filename
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📄 Test report saved to {report_file}")

    def run_complete_pipeline(self) -> bool:
        """
        Run the complete CI/CD testing pipeline.

        Returns:
            True if all checks pass, False otherwise
        """
        print("🚀 Starting CI/CD Pipeline")
        print("=" * 50)

        pipeline_steps = [
            ("Installing dependencies", self.install_dependencies),
            ("Installing test dependencies", self.install_test_dependencies),
            ("Running linting checks", self.run_linting),
            ("Running unit tests", self.run_unit_tests),
            ("Running integration tests", self.run_integration_tests),
            ("Running security checks", self.run_security_checks)
        ]

        all_passed = True

        for step_name, step_function in pipeline_steps:
            print(f"\n🔄 {step_name}...")
            try:
                if not step_function():
                    all_passed = False
                    print(f"💥 {step_name} failed")
                else:
                    print(f"✅ {step_name} completed successfully")
            except Exception as e:
                print(f"💥 {step_name} failed with exception: {e}")
                all_passed = False

        # Generate final report
        print(f"\n📊 Generating test report...")
        self.save_test_report()

        report = self.generate_test_report()
        success_rate = report['summary']['success_rate']

        print("\n" + "=" * 50)
        if all_passed:
            print("🎉 CI/CD Pipeline PASSED!")
        else:
            print("💥 CI/CD Pipeline FAILED!")

        print(f"📊 Success Rate: {success_rate:.1f}%")
        print(f"✅ Passed: {report['summary']['passed_checks']}")
        print(f"❌ Failed: {report['summary']['failed_checks']}")
        print("=" * 50)

        return all_passed

def main():
    """Main entry point for the CI/CD automation script."""
    import argparse

    parser = argparse.ArgumentParser(description="CI/CD Testing Automation")
    parser.add_argument(
        "--project-root",
        default=".",
        help="Root directory of the project"
    )
    parser.add_argument(
        "--step",
        choices=["deps", "test-deps", "lint", "unit", "integration", "security", "all"],
        default="all",
        help="Specific step to run"
    )

    args = parser.parse_args()

    cicd = CICDAutomation(args.project_root)

    if args.step == "all":
        success = cicd.run_complete_pipeline()
    elif args.step == "deps":
        success = cicd.install_dependencies()
    elif args.step == "test-deps":
        success = cicd.install_test_dependencies()
    elif args.step == "lint":
        success = cicd.run_linting()
    elif args.step == "unit":
        success = cicd.run_unit_tests()
    elif args.step == "integration":
        success = cicd.run_integration_tests()
    elif args.step == "security":
        success = cicd.run_security_checks()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
