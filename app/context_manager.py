import re

class ContextManager:
    def __init__(self):
        self.fields = [
            "full_name",
            "email",
            "phone",
            "experience",
            "position",
            "location",
            "tech_stack"
        ]
        self.questions = {
            "full_name": "Please enter your full name.",
            "email": "Please share your email address.",
            "phone": "Could you provide your phone number?",
            "experience": "How many years of experience do you have? (Give only the number)",
            "position": "What position are you interested in?",
            "location": "Where are you currently located?",
            "tech_stack": "List the tech stack you're proficient in (e.g., Python, React, MySQL)."
        }
        self.responses = {}
        self.state = "awaiting_full_name"
    def update_state(self):
        next_field = self.next_field()
        if next_field:
            self.state = f"awaiting_{next_field}"
        else:
            self.state = "awaiting_tech_questions"

    def validate(self, field, value):
        value = value.strip()
        if field == "full_name":
            return len(value.split()) >= 2 and all(x.isalpha() or x=="-" for x in value.replace(" ",""))
        elif field == "email":
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            return re.match(pattern, value) is not None
        elif field == "phone":
            digits = re.sub(r"\D", "", value)
            return digits.isdigit() and 10 <= len(digits) <= 12
        elif field == "experience":
            if value.isdigit():
                years = int(value)
                return 0 <= years <= 50
            return False
        elif field == "position":
            return len(value) >= 2
        elif field == "location":
            return len(value) >= 2 and all(x.isalpha() or x.isspace() for x in value)
        elif field == "tech_stack":
            items = [i.strip() for i in value.split(",")]
            return len(items) >= 1 and all(len(i) > 1 for i in items)
        else:
            return False

    def next_field(self):
        for field in self.fields:
            if field not in self.responses:
                return field
        return None

    def update_response(self, field, value):
        self.responses[field] = value
        self.update_state()

    def is_complete(self):
        return all(field in self.responses for field in self.fields)

    def summary(self):
        return "\n".join([f"**{k.replace('_', ' ').title()}**: {v}" for k, v in self.responses.items()])
