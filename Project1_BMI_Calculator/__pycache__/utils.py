def calculate_bmi(weight, height):
    try:
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        return round(bmi, 2)
    except ZeroDivisionError:
        return None

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def get_health_tip(category):
    tips = {
        "Underweight": "Eat more calories and nutritious foods. Include protein and healthy fats.",
        "Normal": "Great job! Maintain your weight with a balanced diet and regular exercise.",
        "Overweight": "Incorporate cardio and a healthy diet. Avoid sugary and fried foods.",
        "Obese": "Consult a healthcare provider. Focus on lifestyle changes and physical activity."
    }
    return tips.get(category, "")





