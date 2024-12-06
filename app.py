import random
import string
import math
import streamlit as st
import pyperclip

# Function to calculate entropy
def calculate_entropy(password):
    char_set_size = 0
    if any(c.islower() for c in password):
        char_set_size += 26
    if any(c.isupper() for c in password):
        char_set_size += 26
    if any(c.isdigit() for c in password):
        char_set_size += 10
    if any(c in string.punctuation for c in password):
        char_set_size += len(string.punctuation)

    if char_set_size == 0:
        return 0
    return math.log2(char_set_size) * len(password)

# Function to check password strength
def check_password_strength(password):
    entropy = calculate_entropy(password)
    suggestions = []

    if len(password) < 12:
        suggestions.append("Increase the length to at least 12 characters.")
    if not any(c.islower() for c in password):
        suggestions.append("Add lowercase letters.")
    if not any(c.isupper() for c in password):
        suggestions.append("Add uppercase letters.")
    if not any(c.isdigit() for c in password):
        suggestions.append("Include at least one digit.")
    if not any(c in string.punctuation for c in password):
        suggestions.append("Include special characters (e.g., @, #, $).")

    if entropy >= 80:
        return "Very Strong: Your password is excellent.", suggestions
    elif entropy >= 60:
        return "Strong: Your password is good, but could be better.", suggestions
    elif entropy >= 40:
        return "Moderate: Consider improving your password.", suggestions
    else:
        return "Weak: Your password is too weak.", suggestions

# Function to generate a password
def generate_password(length=16, include_upper=True, include_lower=True,
                      include_digits=True, include_special=True):
    if length < 8:
        return "Error: Password length must be at least 8 characters."

    char_pools = {
        "upper": string.ascii_uppercase if include_upper else "",
        "lower": string.ascii_lowercase if include_lower else "",
        "digits": string.digits if include_digits else "",
        "special": string.punctuation if include_special else ""
    }

    active_pools = [pool for pool in char_pools.values() if pool]
    if not active_pools:
        return "Error: At least one character type must be included."

    password = [random.choice(pool) for pool in active_pools]
    all_characters = "".join(active_pools)
    password += random.choices(all_characters, k=length - len(password))
    random.shuffle(password)
    return ''.join(password)

# Streamlit Interface
st.title("🔑 Password Tool")

# Check Password Strength
st.header("🔍 Check Password Strength")
password_input = st.text_input("Enter a password to check strength:")
if st.button("Check Strength"):
    if password_input:
        strength, suggestions = check_password_strength(password_input)
        st.write(f"**Strength:** {strength}")
        if suggestions:
            st.write("**Suggestions to improve your password:**")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
    else:
        st.warning("Please enter a password.")

# Generate Custom Password
st.header("⚙️ Generate Custom Password")
length = st.number_input("Password Length:", min_value=8, max_value=64, value=16, step=1)
include_upper = st.checkbox("Include Uppercase", value=True)
include_lower = st.checkbox("Include Lowercase", value=True)
include_digits = st.checkbox("Include Digits", value=True)
include_special = st.checkbox("Include Special Characters", value=True)


# Generate Button
if st.button("Generate Password"):
    password = generate_password(length, include_upper, include_lower, include_digits, include_special)
    st.write(f"**Generated Password:** {password}")
    
   # Display the password in a text area (this allows user to copy it)
    st.text_area("Generated Password", password)
pyperclip.copy(password)
st.success("Password copied to clipboard!")
# Footer
st.write("---")

