import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Binary Decoder Activity", layout="wide")
st.title("🧠 Binary Decoder Activity")

st.markdown("""
You're given 8 decimal numbers. Convert each to an **8-bit binary number** and enter your answers in the sidebar.  
Your binary inputs will reveal a hidden image!
""")

# The decimal values representing each row of the image (you can change these for a new puzzle)
decimal_values = [112, 208, 112, 120, 127, 126, 120, 16]

# Sidebar input – this column is automatically narrow and mobile-friendly
st.sidebar.header("Your Binary Inputs")
binary_inputs = []
for i, dec in enumerate(decimal_values):
    prompt = str(dec)
    bin_input = st.sidebar.text_input(prompt, value="", max_chars=8, key=f"row_{i}")
    binary_inputs.append(bin_input.strip())
_ = """
if st.sidebar.button("Show Image"):
    binary_grid = []
    for bin_input in binary_inputs:
        if len(bin_input) == 8 and set(bin_input).issubset({'0', '1'}):
            # Convert valid binary string to a list of ints
            binary_grid.append([int(bit) for bit in bin_input])
        else:
            # If invalid, use a blank row as a placeholder
            binary_grid.append([0] * 8)
"""
if st.sidebar.button("Show Image"):
    binary_grid = []
    normalized_inputs = []
    for bin_input in binary_inputs:
        bin_input = bin_input.strip()
        if set(bin_input).issubset({'0', '1'}) and len(bin_input) <= 8:
            padded = bin_input.zfill(8)  # Pad with leading zeros
            normalized_inputs.append(padded)
            binary_grid.append([int(bit) for bit in padded])
        else:
            normalized_inputs.append("00000000")
            binary_grid.append([0] * 8)

    # Create a 2D NumPy array from the binary grid
    image_array = np.array(binary_grid)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(image_array, cmap='Greys', vmin=0, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)

    # Optional: Check correctness against the true binary conversion of the given decimals
    # correct = all(format(decimal_values[i], '08b') == binary_inputs[i] for i in range(8))
    correct = all(format(decimal_values[i], '08b') == normalized_inputs[i] for i in range(8))

    if correct:
        st.success("✅ All correct! You decoded the image!")
    else:
        st.info("🔍 Some rows may be incorrect. Please double-check your binary conversions.")
