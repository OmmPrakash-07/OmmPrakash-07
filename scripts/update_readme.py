import os
import re
from urllib.parse import quote

import requests


# ============================================================
# CONFIG
# ============================================================

OWNER = os.getenv("GITHUB_USERNAME", "OmmPrakash-07")
PROFILE_REPO = os.getenv("PROFILE_REPO", "OmmPrakash-07")
README_FILE = "README.md"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# ============================================================
# LANGUAGE BADGES
# ============================================================

LANGUAGE_BADGES = {
    "Python": {
        "color": "3776AB",
        "logo": "python",
        "logoColor": "white",
    },
    "JavaScript": {
        "color": "F7DF1E",
        "logo": "javascript",
        "logoColor": "black",
    },
    "TypeScript": {
        "color": "3178C6",
        "logo": "typescript",
        "logoColor": "white",
    },
    "Java": {
        "color": "ED8B00",
        "logo": "openjdk",
        "logoColor": "white",
    },
    "C": {
        "color": "A8B9CC",
        "logo": "c",
        "logoColor": "white",
    },
    "C++": {
        "color": "00599C",
        "logo": "cplusplus",
        "logoColor": "white",
    },
    "C#": {
        "color": "512BD4",
        "logo": "dotnet",
        "logoColor": "white",
    },
    "HTML": {
        "color": "E34F26",
        "logo": "html5",
        "logoColor": "white",
    },
    "CSS": {
        "color": "1572B6",
        "logo": "css3",
        "logoColor": "white",
    },
    "SQL": {
        "color": "4479A1",
        "logo": "mysql",
        "logoColor": "white",
    },
    "Shell": {
        "color": "4EAA25",
        "logo": "gnubash",
        "logoColor": "white",
    },
    "Dart": {
        "color": "0175C2",
        "logo": "dart",
        "logoColor": "white",
    },
    "Kotlin": {
        "color": "7F52FF",
        "logo": "kotlin",
        "logoColor": "white",
    },
    "Swift": {
        "color": "F05138",
        "logo": "swift",
        "logoColor": "white",
    },
    "PHP": {
        "color": "777BB4",
        "logo": "php",
        "logoColor": "white",
    },
    "Go": {
        "color": "00ADD8",
        "logo": "go",
        "logoColor": "white",
    },
    "Rust": {
        "color": "000000",
        "logo": "rust",
        "logoColor": "white",
    },
}


# ============================================================
# TECHNOLOGY BADGES
# ============================================================

BADGES = {
    # Frontend
    "React": ("20232A", "react", "61DAFB"),
    "Next.js": ("000000", "nextdotjs", "white"),
    "Angular": ("DD0031", "angular", "white"),
    "Vue.js": ("4FC08D", "vuedotjs", "white"),
    "Vite": ("646CFF", "vite", "white"),
    "Tailwind CSS": ("06B6D4", "tailwindcss", "white"),
    "Redux": ("764ABC", "redux", "white"),
    "React Router": ("CA4245", "reactrouter", "white"),
    "Axios": ("5A29E4", "axios", "white"),

    # Backend
    "Node.js": ("339933", "nodedotjs", "white"),
    "Express.js": ("000000", "express", "white"),
    "NestJS": ("E0234E", "nestjs", "white"),
    "FastAPI": ("009688", "fastapi", "white"),
    "Django": ("092E20", "django", "white"),
    "Flask": ("000000", "flask", "white"),
    "Spring Boot": ("6DB33F", "springboot", "white"),
    "Spring Security": ("6DB33F", "springsecurity", "white"),
    "Spring Data JPA": ("6DB33F", "spring", "white"),
    ".NET": ("512BD4", "dotnet", "white"),
    "ASP.NET Core": ("512BD4", "dotnet", "white"),
    "Entity Framework Core": ("512BD4", "dotnet", "white"),

    # AI / ML
    "LangChain": ("1C3C3C", "langchain", "white"),
    "LangGraph": ("1C3C3C", "langgraph", "white"),
    "OpenAI": ("412991", "openai", "white"),
    "TensorFlow": ("FF6F00", "tensorflow", "white"),
    "PyTorch": ("EE4C2C", "pytorch", "white"),
    "NumPy": ("013243", "numpy", "white"),
    "Pandas": ("150458", "pandas", "white"),

    # Database
    "MongoDB": ("47A248", "mongodb", "white"),
    "PostgreSQL": ("4169E1", "postgresql", "white"),
    "MySQL": ("4479A1", "mysql", "white"),
    "Redis": ("DC382D", "redis", "white"),
    "DynamoDB": ("4053D6", "amazondynamodb", "white"),

    # Cloud / DevOps
    "AWS": ("232F3E", "amazonaws", "white"),
    "Google Cloud": ("4285F4", "googlecloud", "white"),
    "Docker": ("2496ED", "docker", "white"),
    "Terraform": ("844FBA", "terraform", "white"),
    "GitHub Actions": ("2088FF", "githubactions", "white"),

    # Tools
    "Git": ("F05032", "git", "white"),
    "GitHub": ("181717", "github", "white"),
    "Maven": ("C71A36", "apachemaven", "white"),
}


# ============================================================
# FRAMEWORK / TECHNOLOGY DETECTION RULES
# ============================================================

FRAMEWORK_RULES = {
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
    "Tailwind CSS": [
        "tailwindcss",
    ],
    "Redux": [
        "redux",
        "@reduxjs/toolkit",
    ],
    "React Router": [
        "react-router",
        "react-router-dom",
    ],
    "Axios": [
        "axios",
    ],
    "Express.js": [
        "express",
    ],
    "NestJS": [
        "@nestjs/core",
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
        "langchain-openai",
        "langchain-core",
    ],
    "LangGraph": [
        "langgraph",
    ],
    "OpenAI": [
        "openai",
        "langchain-openai",
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
        "springframework.boot",
    ],
    "Spring Security": [
        "spring-security",
    ],
    "Spring Data JPA": [
        "spring-data-jpa",
    ],
    "Maven": [
        "maven",
    ],

    # .NET
    ".NET": [
        "Microsoft.NET.Sdk",
        "dotnet",
    ],
    "ASP.NET Core": [
        "Microsoft.AspNetCore",
        "aspnetcore",
    ],
    "Entity Framework Core": [
        "Microsoft.EntityFrameworkCore",
        "entityframeworkcore",
    ],

    # Database
    "MongoDB": [
        "mongodb",
        "mongoose",
        "pymongo",
    ],
    "PostgreSQL": [
        "postgresql",
        "psycopg",
        "pg",
    ],
    "MySQL": [
        "mysql",
        "mysql2",
        "pymysql",
    ],
    "Redis": [
        "redis",
    ],
    "DynamoDB": [
        "dynamodb",
        "software.amazon.awssdk:dynamodb",
    ],

    # Cloud
    "AWS": [
        "aws-sdk",
        "amazonaws",
        "software.amazon.awssdk",
        "boto3",
    ],
    "Google Cloud": [
        "google-cloud",
        "google-cloud-storage",
    ],

    # DevOps
    "Docker": [
        "dockerfile",
        "docker-compose",
    ],
    "Terraform": [
        "terraform",
    ],
    "GitHub Actions": [
        ".github/workflows",
    ],
}


# ============================================================
# GITHUB API
# ============================================================

def github_get(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30,
        )

        if response.status_code != 200:
            print(
                f"GitHub API error {response.status_code}: {url}"
            )
            return None

        return response.json()

    except requests.RequestException as error:
        print(f"GitHub request failed: {error}")
        return None


def get_repositories():
    repositories = []

    page = 1

    while True:
        url = (
            f"https://api.github.com/users/{OWNER}/repos"
            f"?per_page=100&page={page}&sort=updated"
        )

        data = github_get(url)

        if not data:
            break

        repositories.extend(data)

        if len(data) < 100:
            break

        page += 1

    return repositories


def get_languages(repo_name):
    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{repo_name}/languages"
    )

    return github_get(url) or {}


def get_repository_tree(repo_name, branch):
    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{repo_name}/git/trees/"
        f"{branch}?recursive=1"
    )

    return github_get(url) or {}


def get_raw_file(repo_name, branch, path):
    url = (
        f"https://raw.githubusercontent.com/"
        f"{OWNER}/{repo_name}/{branch}/{path}"
    )

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30,
        )

        if response.status_code == 200:
            return response.text

    except requests.RequestException:
        pass

    return ""


# ============================================================
# LANGUAGE PERCENTAGES
# ============================================================

def calculate_language_percentages(languages):
    if not languages:
        return []

    total = sum(languages.values())

    if total == 0:
        return []

    percentages = []

    for language, byte_count in languages.items():
        percentage = (byte_count / total) * 100

        # Hide languages contributing less than 1%
        if percentage >= 1:
            percentages.append(
                (language, percentage)
            )

    return percentages


def language_badge(language, percentage):
    config = LANGUAGE_BADGES.get(language)

    label = quote(language, safe="")

    if config:
        color = config["color"]
        logo = config.get("logo")
        logo_color = config.get("logoColor", "white")

        return (
            f"![{language}]"
            f"(https://img.shields.io/badge/"
            f"{label}-{percentage:.1f}%25-{color}"
            f"?style=flat-square"
            f"&logo={logo}"
            f"&logoColor={logo_color})"
        )

    return (
        f"![{language}]"
        f"(https://img.shields.io/badge/"
        f"{label}-{percentage:.1f}%25-555555"
        f"?style=flat-square)"
    )


def generate_language_section(languages):
    percentages = calculate_language_percentages(languages)

    if not percentages:
        return ""

    badges = []

    for language, percentage in percentages:
        badges.append(
            language_badge(
                language,
                percentage,
            )
        )

    return (
        "**💻 Languages**\n\n"
        + " ".join(badges)
        + "\n\n"
    )


# ============================================================
# TECHNOLOGY DETECTION
# ============================================================

def normalize_text(text):
    return text.lower()


def detect_technologies(repo_name, branch, tree):
    detected = set()

    paths = []

    for item in tree.get("tree", []):
        path = item.get("path", "")

        if path:
            paths.append(path)

    path_text = normalize_text(
        "\n".join(paths)
    )

    # --------------------------------------------------------
    # Read important dependency/configuration files
    # --------------------------------------------------------

    important_files = [
        "package.json",
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "setup.py",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
    ]

    dependency_text = path_text

    for filename in important_files:
        if filename.lower() in [
            p.lower()
            for p in paths
        ]:
            content = get_raw_file(
                repo_name,
                branch,
                filename,
            )

            if content:
                dependency_text += "\n" + content

    # Add .NET project files
    for path in paths:
        if path.endswith(".csproj"):
            content = get_raw_file(
                repo_name,
                branch,
                path,
            )

            if content:
                dependency_text += "\n" + content

    dependency_text = normalize_text(
        dependency_text
    )

    # --------------------------------------------------------
    # Detect technologies
    # --------------------------------------------------------

    for technology, patterns in FRAMEWORK_RULES.items():
        for pattern in patterns:
            if pattern.lower() in dependency_text:
                detected.add(technology)
                break

    # --------------------------------------------------------
    # Node.js
    # --------------------------------------------------------

    if (
        "package.json" in path_text
        and (
            "express.js" in detected
            or "nestjs" in detected
            or "next.js" in detected
        )
    ):
        detected.add("Node.js")

    # --------------------------------------------------------
    # Docker
    # --------------------------------------------------------

    if any(
        path.lower().endswith("dockerfile")
        or "docker-compose" in path.lower()
        for path in paths
    ):
        detected.add("Docker")

    # --------------------------------------------------------
    # GitHub Actions
    # --------------------------------------------------------

    if ".github/workflows/" in path_text:
        detected.add("GitHub Actions")

    # --------------------------------------------------------
    # AWS
    # --------------------------------------------------------

    aws_indicators = [
        "aws",
        "boto3",
        "amazonaws",
        "software.amazon.awssdk",
        "s3",
        "dynamodb",
    ]

    if any(
        indicator in dependency_text
        for indicator in aws_indicators
    ):
        detected.add("AWS")

    # --------------------------------------------------------
    # Google Cloud
    # --------------------------------------------------------

    google_indicators = [
        "google-cloud",
        "google cloud",
        "gcp",
        "storage.googleapis.com",
    ]

    if any(
        indicator in dependency_text
        for indicator in google_indicators
    ):
        detected.add("Google Cloud")

    return sorted(detected)


# ============================================================
# TECHNOLOGY BADGES
# ============================================================

def technology_badge(technology):
    config = BADGES.get(technology)

    if not config:
        return ""

    color, logo, logo_color = config

    label = quote(
        technology,
        safe="",
    )

    return (
        f"![{technology}]"
        f"(https://img.shields.io/badge/"
        f"{label}-{color}"
        f"?style=flat-square"
        f"&logo={logo}"
        f"&logoColor={logo_color})"
    )


def generate_technology_section(technologies):
    if not technologies:
        return ""

    badges = []

    for technology in technologies:
        badge = technology_badge(
            technology
        )

        if badge:
            badges.append(badge)

    if not badges:
        return ""

    return (
        "**⚙️ Technologies & Frameworks**\n\n"
        + " ".join(badges)
        + "\n\n"
    )


# ============================================================
# PROJECT GENERATION
# ============================================================

def generate_project(repo):
    repo_name = repo["name"]
    branch = repo.get(
        "default_branch",
        "main",
    )

    description = (
        repo.get("description")
        or "No description provided."
    )

    languages = get_languages(
        repo_name
    )

    language_section = generate_language_section(
        languages
    )

    tree = get_repository_tree(
        repo_name,
        branch,
    )

    technologies = detect_technologies(
        repo_name,
        branch,
        tree,
    )

    technology_section = generate_technology_section(
        technologies
    )

    stars = repo.get(
        "stargazers_count",
        0,
    )

    forks = repo.get(
        "forks_count",
        0,
    )

    html_url = repo.get(
        "html_url",
        f"https://github.com/{OWNER}/{repo_name}",
    )

    return f"""
### 📂 [{repo_name}]({html_url})

{description}

⭐ **Stars:** {stars} &nbsp;&nbsp; 🍴 **Forks:** {forks}

{language_section}{technology_section}---
"""


# ============================================================
# README UPDATE
# ============================================================

def update_readme(projects_markdown):
    if not os.path.exists(README_FILE):
        print("README.md not found.")
        return

    with open(
        README_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        readme = file.read()

    start_marker = "<!-- AUTO_PROJECTS_START -->"
    end_marker = "<!-- AUTO_PROJECTS_END -->"

    start_index = readme.find(
        start_marker
    )

    end_index = readme.find(
        end_marker
    )

    if start_index == -1 or end_index == -1:
        print(
            "README markers not found."
        )
        print(
            "Add AUTO_PROJECTS_START and "
            "AUTO_PROJECTS_END markers first."
        )
        return

    section = f"""
{start_marker}

## 🚀 Projects & Technologies

_This section is automatically generated from my GitHub repositories._

{projects_markdown}
{end_marker}
"""

    new_readme = (
        readme[:start_index]
        + section
        + readme[end_index + len(end_marker):]
    )

    with open(
        README_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(new_readme)

    print(
        "README.md updated successfully."
    )


# ============================================================
# MAIN
# ============================================================

def main():
    print(
        f"Scanning GitHub repositories for {OWNER}..."
    )

    repositories = get_repositories()

    if not repositories:
        print(
            "No repositories found."
        )
        return

    projects = []

    for repo in repositories:

        # Ignore profile README repository
        if repo["name"].lower() == PROFILE_REPO.lower():
            continue

        # Ignore forks
        if repo.get("fork"):
            continue

        # Ignore archived repositories
        if repo.get("archived"):
            continue

        print(
            f"Scanning: {repo['name']}"
        )

        project = generate_project(
            repo
        )

        projects.append(project)

    if not projects:
        print(
            "No eligible repositories found."
        )
        return

    update_readme(
        "\n".join(projects)
    )


if __name__ == "__main__":
    main()
