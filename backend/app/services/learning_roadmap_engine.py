"""
Learning Roadmap Engine.
Generates customized, practical learning targets and coding projects
to bridge candidate technology gaps honestly.
"""

from typing import List, Dict, Any

ROADMAP_DATABASE = {
    "kubernetes": {
        "project": "Build a Local Minikube Cluster: Containerize a mock backend API and deploy it with 3 replicas, setting up local Ingress controllers, secure ConfigMaps, and rolling updates.",
        "concepts": ["Pod lifecycles", "Ingress routing", "Service deployments", "ConfigMaps & Secrets"]
    },
    "docker": {
        "project": "Create Multi-Stage Docker builds: Optimize a backend Python API using multi-stage Dockerfiles, cutting final image footprints by over 60% and locking root permissions.",
        "concepts": ["Multi-stage layers", "Image optimization", "Root security profiles", "Docker-Compose orchestrations"]
    },
    "fastapi": {
        "project": "Design an Async REST API: Develop a high-performance database service in FastAPI with async SQLAlchemy sessions, Pydantic v2 schemas, and OAuth2 security profiles.",
        "concepts": ["Asynchronous query pools", "Dependency injection", "Pydantic parsing schemas", "OAuth2 configurations"]
    },
    "redis": {
        "project": "Implement Rate-Limiting Caching: Deploy a local Redis instance and build caching middleware to throttle backend API request velocities, supporting up to 10k requests/min.",
        "concepts": ["Pub/Sub messaging protocols", "TTL cache strategies", "Middleware rate-limiters", "Data persistence models"]
    },
    "react": {
        "project": "Construct an Interactive State Dashboard: Build a dynamic dashboard to fetch and visualize backend API schema analytics, utilizing React hooks and responsive layout grids.",
        "concepts": ["React state lifecycles", "Hook management (useEffect/useState)", "Client-side routing", "Responsive layout grids"]
    },
    "next.js": {
        "project": "Architect an SEO-Optimized Landing Page: Develop a high-performance website using Next.js Server Components, optimizing rendering velocities and semantic search discoverabilities.",
        "concepts": ["React Server Components", "Static Site Generation (SSG)", "Dynamic API routing", "Asset optimization modules"]
    },
    "postgresql": {
        "project": "Optimize Relational Indexes: Construct complex database schemas in PostgreSQL, writing custom indexing structures and executing query optimizations to reduce search times.",
        "concepts": ["Query index setups", "Normalizations & Schemas", "Execution plans (EXPLAIN)", "Asynchronous connection pooling"]
    },
    "tensorflow": {
        "project": "Train an Image Classification Model: Develop an automated Convolutional Neural Network (CNN) pipeline to categorize custom image repositories, saving weights locally.",
        "concepts": ["Convolutional layers", "Model weight serializations", "Data normalization matrices", "Validation partitions"]
    },
    "pytorch": {
        "project": "Build a Custom Feature Classification Pipeline: Implement a Deep Learning classifier in PyTorch to predict tabular customer retention metrics, mapping feature vectors.",
        "concepts": ["Tensor calculations", "Backpropagation optimizers", "Loss models", "Feature normalizations"]
    }
}


def generate_learning_roadmap(gaps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compiles custom practical project recommendations and core learning syllabus lists from identified technology gaps."""
    if not gaps:
        return {
            "recommended_projects": ["Build an open-source tool targeting your focus domain to showcase systems knowledge."],
            "roadmap_steps": ["Continue mastering standard technical algorithms and systems design concepts."]
        }

    projects = []
    syllabus = []
    
    for gap in gaps:
        skill_lower = gap["skill"].lower()
        
        if skill_lower in ROADMAP_DATABASE:
            data = ROADMAP_DATABASE[skill_lower]
            projects.append(data["project"])
            for concept in data["concepts"]:
                syllabus.append(f"Master {gap['skill']} {concept}")
        else:
            # Generic smart recommendation
            projects.append(
                f"Develop a clean-code implementation of a {gap['skill']} prototype. Write robust README documentation, "
                f"publish on GitHub, and verify compilation using automated unit test integrations."
            )
            syllabus.append(f"Learn core syntax, API boundaries, and deployment patterns of {gap['skill']}.")

    return {
        "recommended_projects": projects[:3],  # Max 3 actionable projects
        "roadmap_steps": list(dict.fromkeys(syllabus))[:6]  # Deduplicated, max 6 core targets
    }
