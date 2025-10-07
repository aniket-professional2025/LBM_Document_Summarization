# Importing Required Packages
import random
import json
import numpy as np

# Possible preferences and behaviours
length_options = ["short", "medium", "long"]
focus_options = ["introduction", "methods", "results", "key_findings"]
tone_options = ["formal", "casual", "analytical", "enthusiastic"]
feedback_options = ["liked", "neutral", "disliked"]

# Documents
documents = [
    "Climate change continues to impact global agriculture and food security.",
    "Artificial intelligence is transforming healthcare diagnostics and treatment.",
    "Quantum computing promises exponential speed-ups for complex problems.",
    "Renewable energy sources are crucial to achieving net-zero emissions.",
    "Social media influences mental health and public opinion in subtle ways."
]

# Function to Generate LBM type data
# Function to Generate LBM type data with all documents per user
def generate_synthetic_user_data(num_users = 10, docs_per_user = 5):
    data = []
    
    for user_id in range(1, num_users + 1):
        profile = {
            "summary_length_preference": random.choice(length_options),
            "focus_area": random.choice(focus_options),
            "tone_preference": random.choice(tone_options)
        }
        
        # Ensure all documents are used for the user
        for doc in documents[:docs_per_user]:  # take first 'docs_per_user' documents
            behaviour = {
                "read_time_sec": random.randint(60, 300),
                "scroll_depth_percent": random.randint(60, 100),
                "highlighted_phrases": random.sample(doc.split(), k=random.randint(2, 4)),
                "edited_summary_length": random.randint(1, 5),
                "user_feedback": random.choice(feedback_options)
            }
            
            # Simulate a "summary" depending on preferences
            if profile["summary_length_preference"] == "short":
                summary = " ".join(doc.split()[:6]) + "..."
            elif profile["summary_length_preference"] == "medium":
                summary = " ".join(doc.split()[:10]) + "..."
            else:
                summary = doc  # long = full doc
            
            data.append({
                "user_id": f"U{user_id:03}",
                "user_profile": profile,
                "document_text": doc,
                "user_behaviour": behaviour,
                "user_generated_summary": summary
            })
    
    return data

# Generate 10 users * 5 documents each = 50 samples
synthetic_data = generate_synthetic_user_data(num_users = 10, docs_per_user = 5)

# Save to JSON file
with open("synthetic_user_behaviour_data.json", "w") as f:
    json.dump(synthetic_data, f, indent = 2)

print(f"Generated {len(synthetic_data)} samples.")