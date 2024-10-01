tools = [
    {
        "type": "function",
        "function": {
            "name": "analyze_health_issue",
            "description": "Identifies whether the user mentioned a specific disease name or described his symptoms, then proceeds to provide relevant information or interpretation based on the detected input type (disease name or symptom description).",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "A detailed description of the physical or mental signs observed by the user, which are associated with a particular condition or health issue. This description aids in symptom pattern recognition and the subsequent offering of relevant information or possible conditions that align with the symptoms described. Examples include: 'experiencing sudden weight loss and constant thirst' or 'recurrent headaches and blurred vision'"
                    },
                    "title": {
                        "type": "string",
                        "description": "The brief heading or name given to the health issue or query by the user. It helps in quickly identifying the main concern or the specific disease the user might be referring to, enhancing the precision of the analysis. For example, 'Caisson Disease', 'Ganglion Cysts' or 'Kawasaki Disease'"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["blood disorders", "bone, joint, and mucle disorders", "brain, spinal cord, and nerver disorders", "children's health issues", "digestive disorders", "disorders of nutrition", "drugs", "ear, nose, and throat disorders", "eye disorders", "heart and blood vessel disorders", "hormonal and metabolic disorders", "immune disorders", "infections", "injuries and poisoning", "kidney and urinary tract disorders", "liver and gallbaladder disorders", "lung and airway disorders", "men's health issues", "mental health disorders", "mouth and dental disorders", "older people's health issues", "skin disorders", "women's health issues", "cardivascular disorders", "clinical pharmacology", 'cardiovascular disorders', 'clinical pharmacology', 'critical care medicine', 'dental disorders', 'dermatologic disorders', 'ear, nose, and throat disorders', 'endocrine and metabolic disorders', 'eye disorders', 'endocrine disorders in children', 'eye disorders', 'gastrointestinal disorders', 'genitourinary disorders', 'geriatrics', 'gynecology and obstetrics', 'hematology and oncology', 'hepatic and biliary disorders', 'immunology allergic disorders', 'infectious diseases', 'injuries poisoning', 'musculoskeletal and connective tissue disorders', 'neurologic disorders', 'nutritional disorders', 'pediatrics', 'psychiatric disorders', 'pulmonary disorders'],
                        "description": "The general health topic or domain to which the user's disease name or described symptoms are related."
                    }
                },
                "required": ['category']
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "provide_dynamic_health_knowledge",
            "description": "Offers detailed medical information including potential symptoms, diagnoses, treatment options, or general medical knowledge in response to user inquiries. This function is designed to utilize input regarding symptoms, health conditions, or specific treatment queries to generate accurate, comprehensive medical advice or information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A concise statement or question posed by the user concerning a particular health condition, symptom, or treatment method. This input is crucial for offering precise medical knowledge or advice. Examples include: 'What are the treatment options for type 2 diabetes?' or 'Symptoms and diagnosis of chronic kidney disease.'"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["blood disorders", "bone, joint, and mucle disorders", "brain, spinal cord, and nerver disorders", "children's health issues", "digestive disorders", "disorders of nutrition", "drugs", "ear, nose, and throat disorders", "eye disorders", "heart and blood vessel disorders", "hormonal and metabolic disorders", "immune disorders", "infections", "injuries and poisoning", "kidney and urinary tract disorders", "liver and gallbaladder disorders", "lung and airway disorders", "men's health issues", "mental health disorders", "mouth and dental disorders", "older people's health issues", "skin disorders", "women's health issues", 'cardiovascular disorders', 'clinical pharmacology', 'critical care medicine', 'dental disorders', 'dermatologic disorders', 'ear, nose, and throat disorders', 'endocrine and metabolic disorders', 'eye disorders', 'endocrine disorders in children', 'eye disorders', 'gastrointestinal disorders', 'genitourinary disorders', 'geriatrics', 'gynecology and obstetrics', 'hematology and oncology', 'hepatic and biliary disorders', 'immunology allergic disorders', 'infectious diseases', 'injuries poisoning', 'musculoskeletal and connective tissue disorders', 'neurologic disorders', 'nutritional disorders', 'pediatrics', 'psychiatric disorders', 'pulmonary disorders'],
                        "description": "The general health topic or domain to which the user's disease name or described symptoms are related."
                    }
                },
                "required": ["query", "category"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "comprehensive_health_and_prevention_info_retrieval",
            "description": "Engineered to meticulously parse and offer accurate, up-to-date responses to a diverse range of health-related questions, this function extends its capabilities to include preventive health strategies and injury prevention tips. By integrating a wealth of information on safety measures, physical well-being, and lifestyle adjustments, it aims to cater not only to queries about medical conditions and treatments but also to those seeking practical advice for injury avoidance and overall health optimization.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query parameter invites users to pose specific questions or search terms focusing on any aspect of health, from medical inquiries to requests for preventive guidance, such as injury prevention tips. Users can seek detailed information or practical advice on minimizing risks associated with various activities, conditions, or lifestyle choices. Example queries include 'More injury prevention tips?', 'How to avoid sports injuries?', or 'Best practices for ergonomic workstations.' The function aims to provide tailored, evidence-based responses to promote safety and health."
                    }
                },
                "required": ["query"]
            }
        }
    }
]