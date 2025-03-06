import streamlit as st
import re
from typing import Tuple, List

# Common password list (consider using a larger dataset in production)
COMMON_PASSWORDS = [
    'password', '123456', '123456789', 'qwerty', 'abc123',
    'password1', 'admin', 'welcome', 'letmein', '123qwe'
]

def check_password_strength(password: str, common_passwords: List[str]) -> Tuple[int, List[str], str]:
    """
    Evaluate password strength and return score, feedback messages, and strength level.
    """
    common_passwords_set = set(common_passwords)
    if password in common_passwords_set:
        return 0, ['⚠️ Password is in common use - extremely insecure'], 'Weak'

    score = 0
    messages = []
    
    # Length check
    length = len(password)
    if length >= 16:
        score += 3
        messages.append('✅ Length is excellent (16+ characters)')
    elif length >= 12:
        score += 2
        messages.append('✅ Good length (12-15 characters)')
    elif length >= 8:
        score += 1
        messages.append('✅ Minimum length achieved (8-11 characters)')
    else:
        messages.append('❌ Too short (minimum 8 characters required)')

    # Character diversity checks
    checks = [
        (re.search(r'[A-Z]', password), 'Uppercase letter'),
        (re.search(r'[a-z]', password), 'Lowercase letter'),
        (re.search(r'\d', password), 'Number'),
        (re.search(r'[!@#$%^&*(),.?":{}|<>]', password), 'Special character'),
    ]

    for condition, message in checks:
        if condition:
            score += 1
            messages.append(f'✅ Contains {message}')
        else:
            messages.append(f'❌ Missing {message}')

    # Determine strength level
    if score <= 2:
        strength = 'Weak'
    elif score <= 4:
        strength = 'Moderate'
    elif score <= 6:
        strength = 'Strong'
    else:
        strength = 'Very Strong'

    return score, messages, strength

# Streamlit UI Configuration
st.set_page_config(page_title="Password Strength Meter", layout="centered")
st.title("Password Strength Meter")

# Password input
password = st.text_input(
    "Enter password to analyze:", 
    type="password",
    placeholder="Enter your password..."
)

if password:
    score, feedback, strength = check_password_strength(password, COMMON_PASSWORDS)
    
    # Display strength rating
    st.subheader("Security Assessment:")
    strength_colors = {
        'Very Strong': ('#00ff00', '🛡️'),
        'Strong': ('#7fff00', '🔐'),
        'Moderate': ('#ffd700', '⚠️'),
        'Weak': ('#ff0000', '🔓')
    }
    color, icon = strength_colors[strength]
    st.markdown(f"""
        <div style="
            background-color: {color}20;
            padding: 1rem;
            border-radius: 8px;
            border-left: 6px solid {color};
            margin: 1rem 0;">
            <h3 style="color: {color}; margin:0;">
                {icon} {strength} Security ({score}/10 points)
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # Progress bar
    st.progress(score/10)
    
    # Detailed feedback
    st.subheader("Detailed Analysis:")
    for msg in feedback:
        if '✅' in msg:
            st.success(msg)
        elif '❌' in msg:
            st.error(msg)
        else:
            st.info(msg)

    # Security recommendations
    if strength in ['Weak', 'Moderate']:
        st.warning("🔔 Recommendation: Use a longer password with mix of character types!")
    else:
        st.success("🌟 Good job! This password meets strong security standards.")

else:
    st.warning("⚠️ Please enter a password to check its strength")


   
