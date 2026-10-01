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

API_BASE = "https://api.github.com"


# =========================================================
# GitHub API
# =========================================================

def github_request(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
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


def get_languages(repo_name):
    url = f"{API_BASE}/repos/{USERNAME}/{repo_name}/languages"

    data = github_request(url)

    if not data:
        return []

    return [
        language
        for language, _ in sorted(
            data.items(),
            key=lambda item: item[1],
            reverse=True,
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
            },
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode(
                "utf-8",
                errors="ignore",
            )

    except Exception:
        return ""


# =========================================================
# Technology Detection
# =========================================================

FRAMEWORK_RULES = OrderedDict({

    # -------------------------
    # Frontend
    # -------------------------

    "React": [
        '"react"',
        "'react'",
        "react-dom",
    ],

    "Next.js": [
        '"next"',
        "'next'",
    ],

    "Angular": [
        "@angular/core",
    ],

    "Vue.js": [
        '"vue"',
        "'vue'",
    ],

    "Vite": [
        '"vite"',
        "'vite'",
    ],

    "Express.js": [
        '"express"',
        "'express'",
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

    # -------------------------
    # Python
    # -------------------------

    "FastAPI": [
        "fastapi",
    ],

    "Django": [
        "django",
    ],

    "Flask": [
        "flask",
    ],

    # -------------------------
    # AI / ML
    # -------------------------

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

    # -------------------------
    # Java
    # -------------------------

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

    # -------------------------
    # .NET
    # -------------------------

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

    # -------------------------
    # Databases
    # -------------------------

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

    # -------------------------
    # Cloud
    # -------------------------

    "AWS": [
        "@aws-sdk",
        "aws-sdk",
        "boto3",
    ],
})


# =========================================================
# Technology badge configuration
# =========================================================

BADGES = {

    # Languages
    "JavaScript": (
        "JavaScript",
        "F7DF1E",
        "javascript",
        "000000",
    ),

    "TypeScript": (
        "TypeScript",
        "3178C6",
        "typescript",
        "ffffff",
    ),

    "Python": (
        "Python",
        "3776AB",
        "python",
        "ffffff",
    ),

    "Java": (
        "Java",
        "ED8B00",
        "openjdk",
        "ffffff",
    ),

    "C": (
        "C",
        "A8B9CC",
        "c",
        "000000",
    ),

    "C++": (
        "C%2B%2B",
        "00599C",
        "cplusplus",
        "ffffff",
    ),

    "C#": (
        "C%23",
        "512BD4",
        "csharp",
        "ffffff",
    ),

    "HTML": (
        "HTML5",
        "E34F26",
        "html5",
        "ffffff",
    ),

    "CSS": (
        "CSS3",
        "1572B6",
        "css3",
        "ffffff",
    ),

    "SQL": (
        "SQL",
        "4479A1",
        "mysql",
        "ffffff",
    ),

    # Frontend
    "React": (
        "React",
        "61DAFB",
        "react",
        "000000",
    ),

    "Next.js": (
        "Next.js",
        "000000",
        "nextdotjs",
        "ffffff",
    ),

    "Angular": (
        "Angular",
        "DD0031",
        "angular",
        "ffffff",
    ),

    "Vue.js": (
        "Vue.js",
        "4FC08D",
        "vuedotjs",
        "ffffff",
    ),

    "Vite": (
        "Vite",
        "646CFF",
        "vite",
        "ffffff",
    ),

    "Tailwind CSS": (
        "Tailwind CSS",
        "06B6D4",
        "tailwindcss",
        "ffffff",
    ),

    "Redux": (
        "Redux",
        "764ABC",
        "redux",
        "ffffff",
    ),

    "React Router": (
        "React Router",
        "CA4245",
        "reactrouter",
        "ffffff",
    ),

    # Backend
    "Node.js": (
        "Node.js",
        "339933",
        "nodedotjs",
        "ffffff",
    ),

    "Express.js": (
        "Express.js",
        "000000",
        "express",
        "ffffff",
    ),

    "NestJS": (
        "NestJS",
        "E0234E",
        "nestjs",
        "ffffff",
    ),

    "FastAPI": (
        "FastAPI",
        "009688",
        "fastapi",
        "ffffff",
    ),

    "Django": (
        "Django",
        "092E20",
        "django",
        "ffffff",
    ),

    "Flask": (
        "Flask",
        "000000",
        "flask",
        "ffffff",
    ),

    "Spring Boot": (
        "Spring Boot",
        "6DB33F",
        "springboot",
        "ffffff",
    ),

    "Spring Security": (
        "Spring Security",
        "6DB33F",
        "springsecurity",
        "ffffff",
    ),

    "Spring Data JPA": (
        "Spring Data JPA",
        "6DB33F",
        "spring",
        "ffffff",
    ),

    ".NET": (
        ".NET",
        "512BD4",
        "dotnet",
        "ffffff",
    ),

    "ASP.NET Core": (
        "ASP.NET Core",
        "512BD4",
        "dotnet",
        "ffffff",
    ),

    "Entity Framework Core": (
        "Entity Framework Core",
        "512BD4",
        "dotnet",
        "ffffff",
    ),

    # AI
    "LangChain": (
        "LangChain",
        "1C3C3C",
        "langchain",
        "ffffff",
    ),

    "LangGraph": (
        "LangGraph",
        "1C3C3C",
        "langgraph",
        "ffffff",
    ),

    "OpenAI": (
        "OpenAI",
        "412991",
        "openai",
        "ffffff",
    ),

    "TensorFlow": (
        "TensorFlow",
        "FF6F00",
        "tensorflow",
        "ffffff",
    ),

    "PyTorch": (
        "PyTorch",
        "EE4C2C",
        "pytorch",
        "ffffff",
    ),

    "NumPy": (
        "NumPy",
        "013243",
        "numpy",
        "ffffff",
    ),

    "Pandas": (
        "Pandas",
        "150458",
        "pandas",
        "ffffff",
    ),

    # Database
    "MongoDB": (
        "MongoDB",
        "47A248",
        "mongodb",
        "ffffff",
    ),

    "PostgreSQL": (
        "PostgreSQL",
        "4169E1",
        "postgresql",
        "ffffff",
    ),

    "MySQL": (
        "MySQL",
        "4479A1",
        "mysql",
        "ffffff",
    ),

    "Redis": (
        "Redis",
        "DC382D",
        "redis",
        "ffffff",
    ),

    # Cloud
    "AWS": (
        "AWS",
        "232F3E",
        "amazonaws",
        "ffffff",
    ),

    "AWS SDK": (
        "AWS SDK",
        "232F3E",
        "amazonaws",
        "ffffff",
    ),

    # Tools
    "Docker": (
        "Docker",
        "2496ED",
        "docker",
        "ffffff",
    ),

    "Maven": (
        "Maven",
        "C71A36",
        "apachemaven",
        "ffffff",
    ),

    "npm": (
        "npm",
        "CB3837",
        "npm",
        "ffffff",
    ),
}


# =========================================================
# Badge generator
# =========================================================

def badge(name):

    if name not in BADGES:
        return f"`{name}`"

    label, background, logo, logo_color = BADGES[name]

    return (
        f"![{name}]"
        f"(https://img.shields.io/badge/"
        f"{label}-{background}"
        f"?style=flat-square"
        f"&logo={logo}"
        f"&logoColor={logo_color})"
    )


def badges(items):

    if not items:
        return ""

    return " ".join(
        badge(item)
        for item in items
    )


# =========================================================
# Dependency detection
# =========================================================

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

        content = get_raw_file(
            repo_name,
            path,
        )

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


# =========================================================
# Tools
# =========================================================

def detect_tools(tree, text):

    tools = []

    filenames = {
        path.split("/")[-1].lower()
        for path in tree
    }

    if (
        "dockerfile" in filenames
        or any(
            "docker-compose" in name
            or "compose.yaml" in name
            for name in filenames
        )
    ):
        tools.append("Docker")

    if "pom.xml" in filenames:
        tools.append("Maven")

    if "package.json" in filenames:
        tools.append("npm")

    return tools


# =========================================================
# Categories
# =========================================================

DATABASE_TECHNOLOGIES = {
    "MongoDB",
    "PostgreSQL",
    "MySQL",
    "Redis",
}

CLOUD_TECHNOLOGIES = {
    "AWS",
    "AWS SDK",
}

AI_TECHNOLOGIES = {
    "LangChain",
    "LangGraph",
    "OpenAI",
    "TensorFlow",
    "PyTorch",
    "NumPy",
    "Pandas",
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


def categorize(frameworks):

    result = {
        "Frontend": [],
        "Backend": [],
        "AI / ML": [],
        "Database": [],
        "Cloud": [],
        "Other": [],
    }

    for item in frameworks:

        if item in FRONTEND_TECHNOLOGIES:
            result["Frontend"].append(item)

        elif item in BACKEND_TECHNOLOGIES:
            result["Backend"].append(item)

        elif item in AI_TECHNOLOGIES:
            result["AI / ML"].append(item)

        elif item in DATABASE_TECHNOLOGIES:
            result["Database"].append(item)

        elif item in CLOUD_TECHNOLOGIES:
            result["Cloud"].append(item)

        else:
            result["Other"].append(item)

    return result


# =========================================================
# Project scanning
# =========================================================

def scan_project(repo):

    repo_name = repo["name"]

    print(f"Scanning: {repo_name}")

    languages = get_languages(repo_name)

    tree = get_repository_tree(repo_name)

    dependency_files = find_dependency_files(tree)

    dependency_content = dependency_text(
        repo_name,
        dependency_files,
    )

    frameworks = detect_frameworks(
        dependency_content
    )

    tools = detect_tools(
        tree,
        dependency_content,
    )

    categories = categorize(
        frameworks
    )

    return {
        "name": repo_name,
        "url": repo["html_url"],
        "description": repo.get("description") or "",
        "languages": languages,
        "categories": categories,
        "tools": tools,
        "updated": repo.get("updated_at", ""),
    }


# =========================================================
# README generation
# =========================================================

def build_section(projects):

    output = [
        START_MARKER,
        "",
        "## 🚀 Projects & Technologies",
        "",
        "> Automatically generated from my public GitHub repositories.",
        "",
    ]

    for project in projects:

        output.append(
            f"### 📂 [{project['name']}]"
            f"({project['url']})"
        )

        if project["description"]:
            output.append("")
            output.append(
                project["description"]
            )

        output.append("")

        if project["languages"]:

            output.append(
                "**💻 Languages**"
            )

            output.append(
                badges(
                    project["languages"][:8]
                )
            )

            output.append("")

        categories = project["categories"]

        if categories["Frontend"]:

            output.append(
                "**🎨 Frontend**"
            )

            output.append(
                badges(
                    categories["Frontend"]
                )
            )

            output.append("")

        if categories["Backend"]:

            output.append(
                "**⚙️ Backend**"
            )

            output.append(
                badges(
                    categories["Backend"]
                )
            )

            output.append("")

        if categories["AI / ML"]:

            output.append(
                "**🤖 AI / ML**"
            )

            output.append(
                badges(
                    categories["AI / ML"]
                )
            )

            output.append("")

        if categories["Database"]:

            output.append(
                "**🗄️ Database**"
            )

            output.append(
                badges(
                    categories["Database"]
                )
            )

            output.append("")

        if categories["Cloud"]:

            output.append(
                "**☁️ Cloud**"
            )

            output.append(
                badges(
                    categories["Cloud"]
                )
            )

            output.append("")

        if categories["Other"]:

            output.append(
                "**🧩 Libraries / Frameworks**"
            )

            output.append(
                badges(
                    categories["Other"]
                )

            output.append("")

        if project["tools"]:

            output.append(
                "**🛠️ Tools**"
            )

            output.append(
                badges(
                    project["tools"]
                )
            )

            output.append("")

        output.append("---")
        output.append("")

    if output[-2] == "---":
        output = output[:-2]

    output.extend([
        "",
        END_MARKER,
    ])

    return "\n".join(output)


# =========================================================
# README update
# =========================================================

def update_readme(section):

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
        re.DOTALL,
    )

    if pattern.search(content):

        updated = pattern.sub(
            section,
            content,
            count=1,
        )

    else:

        updated = (
            content.rstrip()
            + "\n\n---\n\n"
            + section
            + "\n"
        )

    README_FILE.write_text(
        updated,
        encoding="utf-8",
    )


# =========================================================
# Main
# =========================================================

def main():

    print("=" * 60)
    print("GitHub Projects & Technology Detector")
    print("=" * 60)

    repositories = get_repositories()

    projects = []

    for repo in repositories:

        if repo["name"].lower() == PROFILE_REPO.lower():
            continue

        if repo.get("fork"):
            continue

        if repo.get("archived"):
            continue

        projects.append(
            scan_project(repo)
        )

    projects.sort(
        key=lambda item: item["updated"],
        reverse=True,
    )

    print(
        f"Generating README for {len(projects)} projects..."
    )

    section = build_section(
        projects
    )

    update_readme(section)

    print("README updated successfully.")


if __name__ == "__main__":
    main()
