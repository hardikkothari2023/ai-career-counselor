# skills_gap.py
import random
# Predefined required skills for each career
REQUIRED_SKILLS = {

    # 1️⃣ Data Scientist
    'Data Scientist': {
        'python', 'r', 'sql', 'statistics', 'probability', 'machine learning',
        'deep learning', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit-learn',
        'data cleaning', 'data preprocessing', 'feature engineering',
        'data visualization', 'model evaluation', 'big data', 'spark',
        'nlp', 'time series analysis', 'regression', 'classification'
    },

    # 2️⃣ Web Developer
    'Web Developer': {
        'html', 'css', 'javascript', 'typescript', 'react', 'node.js', 'express.js',
        'git', 'bootstrap', 'rest api', 'json', 'frontend', 'backend', 'mongodb',
        'mysql', 'responsive design', 'web hosting', 'version control',
        'problem solving', 'debugging'
    },

    # 3️⃣ Software Engineer
    'Software Engineer': {
        'python', 'java', 'c++', 'c', 'git', 'linux', 'oop', 'data structures',
        'algorithms', 'software development lifecycle', 'debugging',
        'unit testing', 'api integration', 'system design', 'problem solving',
        'communication', 'agile', 'jira'
    },

    # 4️⃣ AI Engineer
    'AI Engineer': {
        'python', 'tensorflow', 'keras', 'pytorch', 'deep learning',
        'machine learning', 'neural networks', 'nlp', 'cv2', 'transformers',
        'data preprocessing', 'hyperparameter tuning', 'model optimization',
        'cloud deployment', 'api development', 'mlops'
    },

    # 5️⃣ DevOps Engineer
    'DevOps Engineer': {
        'docker', 'aws', 'azure', 'linux', 'git', 'ci/cd', 'jenkins',
        'kubernetes', 'terraform', 'ansible', 'bash scripting',
        'monitoring', 'prometheus', 'grafana', 'networking', 'cloud security'
    },

    # 6️⃣ UI/UX Designer
    'UI/UX Designer': {
        'figma', 'adobe xd', 'illustrator', 'photoshop', 'wireframing',
        'prototyping', 'user research', 'creativity', 'interaction design',
        'visual hierarchy', 'typography', 'color theory', 'usability testing',
        'responsive design', 'collaboration'
    },

    # 7️⃣ Database Administrator
    'Database Admin': {
        'sql', 'mysql', 'postgresql', 'oracle', 'mongodb', 'performance tuning',
        'data backup', 'data recovery', 'indexing', 'query optimization',
        'database security', 'stored procedures', 'replication', 'linux',
        'shell scripting'
    },

    # 8️⃣ Cybersecurity Analyst
    'Cybersecurity Analyst': {
        'network security', 'firewalls', 'encryption', 'python', 'linux',
        'penetration testing', 'vulnerability assessment', 'incident response',
        'wireshark', 'nmap', 'malware analysis', 'ethical hacking',
        'threat modeling', 'risk assessment', 'security auditing'
    },

    # 9️⃣ Cloud Engineer
    'Cloud Engineer': {
        'aws', 'azure', 'gcp', 'terraform', 'docker', 'linux', 'kubernetes',
        'cloud formation', 'virtual machines', 'api gateway', 'load balancing',
        'devops', 'networking', 'storage management', 's3', 'ec2', 'lambda'
    },

    # 🔟 Data Analyst
    'Data Analyst': {
        'python', 'r', 'sql', 'excel', 'power bi', 'tableau', 'pandas', 'numpy',
        'data visualization', 'data cleaning', 'statistics', 'report generation',
        'pivot tables', 'business analysis', 'storytelling with data'
    },

    # 11️⃣ Machine Learning Engineer
    'Machine Learning Engineer': {
        'python', 'scikit-learn', 'tensorflow', 'keras', 'pytorch', 'feature selection',
        'model deployment', 'mlops', 'data pipelines', 'docker', 'fastapi',
        'aws sagemaker', 'hyperparameter tuning', 'cross validation'
    },

    # 12️⃣ Backend Developer
    'Backend Developer': {
        'python', 'django', 'flask', 'node.js', 'express.js', 'api development',
        'rest api', 'sql', 'mongodb', 'redis', 'authentication', 'authorization',
        'git', 'testing', 'security', 'microservices', 'cloud deployment'
    },

    # 13️⃣ Frontend Developer
    'Frontend Developer': {
        'html', 'css', 'javascript', 'react', 'angular', 'vue.js', 'bootstrap',
        'sass', 'redux', 'typescript', 'webpack', 'ui design', 'responsive design',
        'figma', 'cross-browser testing'
    }
}


def get_missing_skills(user_skills, predicted_career):
    """
    Finds missing skills for the predicted career and returns 3–4 key ones.
    
    Parameters:
        user_skills (list or set): Skills extracted from the user's resume.
        predicted_career (str): The job role predicted by the model.

    Returns:
        list: 3–4 missing but important skills for that role.
    """
    # Get required skills for the given career
    required = REQUIRED_SKILLS.get(predicted_career, set())
    
    # Convert user skills to set for comparison
    user_skills_set = set(skill.lower().strip() for skill in user_skills)
    
    # Identify missing skills
    missing = list(required - user_skills_set)

    # Randomly select 3–4 skills (or fewer if not enough)
    if len(missing) > 5:
        missing = random.sample(missing, 4)
    
    return missing
# user_skills = ['python', 'sql']
# career = 'Data Scientist'

# missing = analyze_skill_gap(user_skills, career)
# print("Missing Skills:", missing)