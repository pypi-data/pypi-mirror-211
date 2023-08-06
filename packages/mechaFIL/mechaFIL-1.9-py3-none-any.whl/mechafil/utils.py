def validate_qap_method(user_input):
    user_input = user_input.lower()
    if not (user_input == 'basic' or user_input == 'tunable'):
        raise ValueError("qap_method must be either basic or tunable!")