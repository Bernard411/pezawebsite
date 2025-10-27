import os
import django
from django.utils import timezone
import random

# ---- Django setup ----
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pezawebsite.settings')
django.setup()

# ---- Import models ----
from core.models import Category, Article, Tool, Resource

# ---- Real-world data ----
CATEGORY_INFO = {
    "Artificial Intelligence": "Latest trends, tools, and techniques in AI and machine learning.",
    "Cybersecurity": "Learn how to protect systems and data from modern threats.",
    "Web Development": "Frontend and backend frameworks, tutorials, and best practices.",
    "Mobile Development": "Building mobile apps using Android, iOS, and cross-platform tools.",
    "Data Science": "Data analytics, visualization, and model training with Python and R.",
    "DevOps": "Continuous integration, automation, and cloud infrastructure management.",
    "UI/UX Design": "Design principles, prototyping, and user research insights.",
    "Programming Languages": "Tutorials and updates on popular languages like Python, JavaScript, and Go."
}

ARTICLES = [
    {
        "title": "How Artificial Intelligence is Transforming Healthcare",
        "content": "AI is revolutionizing healthcare with predictive analytics, diagnostic imaging, and patient data management. Machine learning models are now capable of detecting diseases faster and more accurately than ever before.",
        "tags": ["AI", "Machine Learning", "Healthcare"]
    },
    {
        "title": "Cybersecurity Best Practices for 2025",
        "content": "With cyber threats evolving daily, organizations must implement zero-trust architectures, endpoint security, and threat intelligence systems to stay secure.",
        "tags": ["Cybersecurity", "Network Security", "Zero Trust"]
    },
    {
        "title": "Building Modern Web Apps with Django and React",
        "content": "Django provides a robust backend while React offers a dynamic frontend. Combining them enables developers to build scalable, maintainable web apps quickly.",
        "tags": ["Django", "React", "Web Development"]
    },
    {
        "title": "Getting Started with Data Science Using Python",
        "content": "Learn how to use pandas, NumPy, and Matplotlib to analyze data efficiently. Python remains the top choice for data scientists worldwide.",
        "tags": ["Data Science", "Python", "Pandas"]
    },
    {
        "title": "Mobile App Security: Protecting User Data",
        "content": "App developers must adopt encryption, secure authentication, and secure APIs to protect user information on mobile devices.",
        "tags": ["Mobile Security", "Cybersecurity", "Encryption"]
    },
    {
        "title": "Continuous Integration and Deployment with GitHub Actions",
        "content": "Automate your testing and deployment pipeline using GitHub Actions, enabling faster and more reliable releases.",
        "tags": ["DevOps", "CI/CD", "Automation"]
    },
    {
        "title": "Designing User-Friendly Interfaces with Figma",
        "content": "Figma enables designers to collaborate and prototype in real-time, making it easier to create seamless UI/UX experiences.",
        "tags": ["UI/UX", "Design", "Figma"]
    },
    {
        "title": "Exploring Natural Language Processing in Python",
        "content": "Using libraries like NLTK and spaCy, developers can build text analysis tools, chatbots, and sentiment analysis systems.",
        "tags": ["NLP", "AI", "Python"]
    },
    {
        "title": "Understanding Containerization with Docker and Kubernetes",
        "content": "Learn how Docker simplifies app deployment and how Kubernetes orchestrates scalable containerized environments.",
        "tags": ["DevOps", "Docker", "Kubernetes"]
    },
    {
        "title": "Top Programming Languages to Learn in 2025",
        "content": "Python, JavaScript, and Go remain at the top for web and AI development, while Rust is gaining popularity for its performance and safety.",
        "tags": ["Programming", "Python", "Go"]
    }
]

TOOLS = [
    ("TensorFlow", "An open-source machine learning framework for training and deploying neural networks."),
    ("Wireshark", "A powerful network protocol analyzer for security professionals."),
    ("VS Code", "A lightweight and versatile code editor by Microsoft."),
    ("Postman", "A collaboration platform for API development and testing."),
    ("Docker", "A containerization platform that simplifies application deployment.")
]

RESOURCES = [
    ("FreeCodeCamp", "Learn coding for free through interactive tutorials and projects.", "https://www.freecodecamp.org/"),
    ("Kaggle", "A platform for data science competitions, datasets, and learning resources.", "https://www.kaggle.com/"),
    ("OWASP", "Resources for securing web applications and understanding common vulnerabilities.", "https://owasp.org/"),
    ("GitHub", "A platform for version control and collaborative software development.", "https://github.com/"),
    ("Coursera AI Courses", "Professional AI and ML courses from leading universities.", "https://www.coursera.org/learn/ai")
]


def create_categories():
    categories = []
    for name, desc in CATEGORY_INFO.items():
        category, _ = Category.objects.get_or_create(name=name, defaults={"description": desc})
        categories.append(category)
    print(f"✅ Created {len(categories)} categories.")
    return categories


def create_articles(categories):
    for data in ARTICLES:
        category = random.choice(categories)
        article, created = Article.objects.get_or_create(
            title=data["title"],
            defaults={
                "content": data["content"],
                "category": category,
                "read_time": random.randint(3, 15),
                "is_tutorial": random.choice([True, False]),
                "is_featured": random.choice([True, False]),
                "published_at": timezone.now(),
                "views": random.randint(50, 1000),
            }
        )
        if created:
            article.tags.add(*data["tags"])
    print(f"✅ Added {len(ARTICLES)} real tech articles.")


def create_tools(categories):
    for name, desc in TOOLS:
        category = random.choice(categories)
        Tool.objects.get_or_create(
            name=name,
            defaults={
                "description": desc,
                "category": category,
                "external_link": f"https://www.google.com/search?q={name}",
            }
        )
    print(f"✅ Added {len(TOOLS)} developer tools.")


def create_resources(categories):
    for name, desc, link in RESOURCES:
        category = random.choice(categories)
        Resource.objects.get_or_create(
            name=name,
            defaults={
                "description": desc,
                "category": category,
                "external_link": link,
            }
        )
    print(f"✅ Added {len(RESOURCES)} tech learning resources.")


def main():
    print("🚀 Populating database with real tech content...")
    categories = create_categories()
    create_articles(categories)
    create_tools(categories)
    create_resources(categories)
    print("🎉 Done populating database with real-world tech data!")


if __name__ == "__main__":
    main()
