def get_missing_skills(resume_skills, job_skills):
    """
    Compares the skills extracted from the resume against the required skills 
    from the job description to identify the skill gaps.
    """
    missing_skills = []
    for skill in job_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)
    return missing_skills

def generate_recommendations(ats_score, missing_skills):
    """
    Generates personalized career recommendations based on ATS score and missing skills.
    """
    recommendations = []
    
    # Generate recommendations for missing skills
    if missing_skills:
        # Suggest learning the top missing skills
        for skill in missing_skills[:3]: 
            recommendations.append(f"Learn {skill.title()}")
            
        if "machine learning" in missing_skills or "deep learning" in missing_skills:
            recommendations.append("Add more ML projects")
            
    # Generate recommendations based on ATS Score
    if ats_score < 75:
        recommendations.append("Improve resume keywords")
        recommendations.append("Tailor your experience to match the job description more closely")
        
    # If the score is high and everything looks good
    if not recommendations:
        recommendations.append("Your resume looks strong! Ensure the formatting is clean.")
        
    return recommendations
