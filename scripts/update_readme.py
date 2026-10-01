import json
import os
import re
import urllib.request
import urllib.error
from pathlib import Path
from collections import OrderedDict


USERNAME = os.getenv("GITHUB_USERNAME", "OmmPrakash-07")
PROFILE_REPO = os.getenv("PROFILE_REPO", "OmmPrakash-07")

README_FILE = Path("README.md")

START_MARKER = "<!-- AUTO_PROJECTS_START -->"
END_MARKER = "<!-- AUTO_PROJECTS_END -->"


# ---------------------------------------------------------
# GitHub API
# ---------------------------------------------------------

API_BASE = "https://api.github.com"


def github_request(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "User-Agent": "github-readme-project-detector",
    }

    token = os.getenv("GITHUB_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as error:
        print(f"GitHub API error: {error.code} - {url}")
        return None

    except Exception as error:
        print(f"Request failed: {error}")
        return None


def get_repositories():
    repositories = []

    page = 1

    while True:
        url = (
            f"{API_BASE}/users/{USERNAME}/repos"
            f"?per_page=100"
            f"&page={page}"
            f"&type=owner"
            f"&sort=updated"
            f"&direction=desc"
        )

        data = github_request(url)

        if not data:
            break

        repositories.extend(data)

        if len(data) < 100:
            break

        page += 1

    return repositories


# ---------------------------------------------------------
# Repository information
# ---------------------------------------------------------

def get_languages(repo_name):
    url = f"{API_BASE}/repos/{USERNAME}/{repo_name}/languages"

    data = github_request(url)

    if not data:
        return []

    # Sort by amount of code
    return [
        language
        for language, _ in sorted(
            data.items(),
            key=lambda item: item[1],
            reverse=True
        )
    ]


def get_repository_tree(repo_name):
    url = (
        f"{API_BASE}/repos/{USERNAME}/{repo_name}"
        f"/git/trees/HEAD?recursive=1"
    )

    data = github_request(url)

    if not data:
        return []

    return [
        item["path"]
        for item in data.get("tree", [])
        if item.get("type") == "blob"
    ]


def get_raw_file(repo_name, path):
    url = (
        f"https://raw.githubusercontent.com/"
        f"{USERNAME}/{repo_name}/HEAD/{path}"
    )

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "github-readme-project-detector"
            }
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8", errors="ignore")

    except Exception:
        return ""


# ---------------------------------------------------------
# Dependency detection
# ---------------------------------------------------------

FRAMEWORK_RULES = OrderedDict({

    # JavaScript / TypeScript
    "React": [
        "react",
        "react-dom",
    ],

    "Next.js": [
        "next",
    ],

    "Angular": [
        "@angular/core",
    ],

    "Vue.js": [
        "vue",
    ],

    "Vite": [
        "vite",
    ],

    "Express.js": [
        "express",
    ],

    "NestJS": [
        "@nestjs/core",
    ],

    "Tailwind CSS": [
        "tailwindcss",
    ],

    "Redux": [
        "redux",
        "@reduxjs/toolkit",
        "react-redux",
    ],

    "React Router": [
        "react-router",
        "react-router-dom",
    ],

    "Axios": [
        "axios",
    ],

    # Python
    "FastAPI": [
        "fastapi",
    ],

    "Django": [
        "django",
    ],

    "Flask": [
        "flask",
    ],

    "LangChain": [
        "langchain",
        "langchain-core",
        "langchain-openai",
    ],

    "LangGraph": [
        "langgraph",
        "langgraph-checkpoint",
    ],

    "OpenAI": [
        "openai",
    ],

    "TensorFlow": [
        "tensorflow",
    ],

    "PyTorch": [
        "torch",
        "pytorch",
    ],

    "NumPy": [
        "numpy",
    ],

    "Pandas": [
        "pandas",
    ],

    # Java
    "Spring Boot": [
        "spring-boot",
        "org.springframework.boot",
    ],

    "Spring Security": [
        "spring-security",
    ],

    "Spring Data JPA": [
        "spring-data-jpa",
    ],

    # .NET
    ".NET": [
        "Microsoft.NET.Sdk",
        "Microsoft.AspNetCore",
        "Microsoft.EntityFrameworkCore",
    ],

    "ASP.NET Core": [
        "Microsoft.AspNetCore",
    ],

    "Entity Framework Core": [
        "Microsoft.EntityFrameworkCore",
    ],

    # Databases
    "MongoDB": [
        "mongodb",
        "mongoose",
        "pymongo",
    ],

    "PostgreSQL": [
        "pg",
        "psycopg",
        "psycopg2",
        "Npgsql",
    ],

    "MySQL": [
        "mysql",
        "mysql2",
        "mysql-connector",
    ],

    "Redis": [
        "redis",
    ],

    # Cloud / infrastructure
    "AWS SDK": [
        "@aws-sdk",
        "aws-sdk",
        "boto3",
    ],

    "Docker": [
        "docker",
    ],
})


# ---------------------------------------------------------
# Dependency files
# ---------------------------------------------------------

DEPENDENCY_FILES = {
    "package.json",
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    "Pipfile",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "go.mod",
    "Cargo.toml",
}


def find_dependency_files(tree):
    found = []

    for path in tree:
        filename = path.split("/")[-1]

        if filename in DEPENDENCY_FILES:
            found.append(path)

        elif filename.endswith(".csproj"):
            found.append(path)

    return found


def dependency_text(repo_name, dependency_files):
    combined = ""

    for path in dependency_files:
        content = get_raw_file(repo_name, path)

        if content:
            combined += "\n" + content.lower()

    return combined


def detect_frameworks(text):
    detected = []

    for framework, packages in FRAMEWORK_RULES.items():

        for package in packages:

            if package.lower() in text:
                detected.append(framework)
                break

    return detected


# ---------------------------------------------------------
# Extra project detection
# ---------------------------------------------------------

def detect_tools(tree, text):
    tools = []

    filenames = {
        path.split("/")[-1].lower()
        for path in tree
    }

    if "dockerfile" in filenames or any(
        "docker-compose" in name or "compose.yaml" in name
        for name in filenames
    ):
        tools.append("Docker")

    if "pom.xml" in filenames:
        tools.append("Maven")

    if "package.json" in filenames:
        tools.append("npm")

    if "requirements.txt" in filenames or "pyproject.toml" in filenames:
        tools.append("Python Package Manager")

    if "terraform" in text or any(
        path.endswith(".tf")
        for path in tree
    ):
        tools.append("Terraform")

    return tools


# ---------------------------------------------------------
# Categories
# ---------------------------------------------------------

DATABASE_TECHNOLOGIES = {
    "MongoDB",
    "PostgreSQL",
    "MySQL",
    "Redis",
}

CLOUD_TECHNOLOGIES = {
    "AWS SDK",
}

AI_TECHNOLOGIES = {
    "LangChain",
    "LangGraph",
    "OpenAI",
    "TensorFlow",
    "PyTorch",
}

FRONTEND_TECHNOLOGIES = {
    "React",
    "Next.js",
    "Angular",
    "Vue.js",
    "Vite",
    "Tailwind CSS",
    "Redux",
    "React Router",
}

BACKEND_TECHNOLOGIES = {
    "Express.js",
    "NestJS",
    "FastAPI",
    "Django",
    "Flask",
    "Spring Boot",
    "Spring Security",
    "Spring Data JPA",
    ".NET",
    "ASP.NET Core",
    "Entity Framework Core",
}


# ---------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------

def code_badges(items):
    if not items:
        return "—"

    return " ".join(
        f"`{item}`"
        for item in items
    )


def project_language_line(languages):
    return code_badges(languages[:8])


def categorized_frameworks(frameworks):
    result = {
        "Frontend": [],
        "Backend": [],
        "AI / ML": [],
        "Database": [],
        "Cloud": [],
        "Other": [],
    }

    for framework in frameworks:

        if framework in FRONTEND_TECHNOLOGIES:
            result["Frontend"].append(framework)

        elif framework in BACKEND_TECHNOLOGIES:
            result["Backend"].append(framework)

        elif framework in AI_TECHNOLOGIES:
            result["AI / ML"].append(framework)

        elif framework in DATABASE_TECHNOLOGIES:
            result["Database"].append(framework)

        elif framework in CLOUD_TECHNOLOGIES:
            result["Cloud"].append(framework)

        else:
            result["Other"].append(framework)

    return result


# ---------------------------------------------------------
# README generation
# ---------------------------------------------------------

def build_project_section(repositories):

    rows = []

    for repo in repositories:

        repo_name = repo["name"]

        # Don't show the profile repository itself
        if repo_name.lower() == PROFILE_REPO.lower():
            continue

        # Don't include forks
        if repo.get("fork"):
            continue

        # Skip archived repositories
        if repo.get("archived"):
            continue

        print(f"Scanning: {repo_name}")

        languages = get_languages(repo_name)

        tree = get_repository_tree(repo_name)

        dependency_files = find_dependency_files(tree)

        dependency_content = dependency_text(
            repo_name,
            dependency_files
        )

        frameworks = detect_frameworks(
            dependency_content
        )

        tools = detect_tools(
            tree,
            dependency_content
        )

        categories = categorized_frameworks(
            frameworks
        )

        rows.append({
            "name": repo_name,
            "description": repo.get("description") or "",
            "url": repo.get("html_url"),
            "languages": languages,
            "frameworks": frameworks,
            "categories": categories,
            "tools": tools,
            "updated": repo.get("updated_at", ""),
        })

    if not rows:
        return (
            f"{START_MARKER}\n"
            "## 🚀 Projects & Technologies\n\n"
            "_No public repositories detected yet._\n\n"
            f"{END_MARKER}"
        )

    # Most recently updated projects first
    rows.sort(
        key=lambda item: item["updated"],
        reverse=True
    )

    markdown = []

    markdown.append(START_MARKER)
    markdown.append("")
    markdown.append("## 🚀 Projects & Technologies")
    markdown.append("")
    markdown.append(
        "> Automatically generated from my public GitHub repositories. "
        "Languages are read from GitHub repository statistics, while "
        "frameworks and libraries are detected from project dependencies."
    )
    markdown.append("")

    for project in rows:

        markdown.append(
            f"### [{project['name']}]({project['url']})"
        )

        if project["description"]:
            markdown.append(
                f"{project['description']}"
            )

        markdown.append("")

        if project["languages"]:
            markdown.append(
                f"**Languages:** "
                f"{project_language_line(project['languages'])}"
            )

        categories = project["categories"]

        if categories["Frontend"]:
            markdown.append(
                f"**Frontend:** "
                f"{code_badges(categories['Frontend'])}"
            )

        if categories["Backend"]:
            markdown.append(
                f"**Backend:** "
                f"{code_badges(categories['Backend'])}"
            )

        if categories["AI / ML"]:
            markdown.append(
                f"**AI / ML:** "
                f"{code_badges(categories['AI / ML'])}"
            )

        if categories["Database"]:
            markdown.append(
                f"**Database:** "
                f"{code_badges(categories['Database'])}"
            )

        if categories["Cloud"]:
            markdown.append(
                f"**Cloud:** "
                f"{code_badges(categories['Cloud'])}"
            )

        if categories["Other"]:
            markdown.append(
                f"**Libraries / Frameworks:** "
                f"{code_badges(categories['Other'])}"
            )

        if project["tools"]:
            markdown.append(
                f"**Tools:** "
                f"{code_badges(project['tools'])}"
            )

        markdown.append("")
        markdown.append("---")
        markdown.append("")

    # Remove final separator
    if markdown[-2] == "---":
        markdown = markdown[:-2]

    markdown.append("")
    markdown.append(END_MARKER)

    return "\n".join(markdown)


# ---------------------------------------------------------
# README replacement
# ---------------------------------------------------------

def update_readme(new_section):

    if not README_FILE.exists():
        raise FileNotFoundError(
            "README.md was not found."
        )

    content = README_FILE.read_text(
        encoding="utf-8"
    )

    pattern = re.compile(
        re.escape(START_MARKER)
        + r".*?"
        + re.escape(END_MARKER),
        re.DOTALL
    )

    if pattern.search(content):

        updated = pattern.sub(
            new_section,
            content,
            count=1
        )

    else:

        # If markers don't exist, add the generated section
        # at the end of the README.
        updated = (
            content.rstrip()
            + "\n\n---\n\n"
            + new_section
            + "\n"
        )

    README_FILE.write_text(
        updated,
        encoding="utf-8"
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("GitHub README Project Detector")
    print("=" * 60)

    print(f"GitHub user: {USERNAME}")

    repositories = get_repositories()

    print(
        f"Found {len(repositories)} repositories."
    )

    section = build_project_section(
        repositories
    )

    update_readme(section)

    print("")
    print("README successfully updated.")
    print("=" * 60)


if __name__ == "__main__":
    main()
