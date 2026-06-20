import streamlit as st
import difflib
from html import escape
from docx import Document

# -------------------------
# Read file (txt or docx)
# -------------------------
def read_file(file):
    if file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        return file.read().decode("utf-8")

# -------------------------
# Tokenizer (word-based)
# -------------------------
def tokenize(text):
    tokens = []
    current = ""

    for char in text:
        if char in " \n\t":
            if current:
                tokens.append(current)
                current = ""
            tokens.append(char)
        else:
            current += char

    if current:
        tokens.append(current)

    return tokens


# -------------------------
# UI
# -------------------------
st.set_page_config(page_title="Document Diff Tool", layout="wide")

st.title("📄 Document Comparison Tool")
st.write("Upload two files (.txt or .docx) to compare them.")

file1 = st.file_uploader("Upload Version 1", type=["txt", "docx"])
file2 = st.file_uploader("Upload Version 2", type=["txt", "docx"])

# -------------------------
# Run diff
# -------------------------
if file1 and file2:

    text1 = read_file(file1)
    text2 = read_file(file2)

    words1 = tokenize(text1)
    words2 = tokenize(text2)

    matcher = difflib.SequenceMatcher(None, words1, words2)
    opcodes = matcher.get_opcodes()

    v1_html = ""
    v2_html = ""

    for tag, i1, i2, j1, j2 in opcodes:

        chunk1 = escape("".join(words1[i1:i2]))
        chunk2 = escape("".join(words2[j1:j2]))

        if tag == "equal":
            v1_html += chunk1
            v2_html += chunk2

        elif tag == "delete":
            v1_html += f"<span style='background:#ff9999'>{chunk1}</span>"

        elif tag == "insert":
            v2_html += f"<span style='background:yellow'>{chunk2}</span>"

        elif tag == "replace":
            v1_html += f"<span style='background:#ff9999'>{chunk1}</span>"
            v2_html += f"<span style='background:yellow'>{chunk2}</span>"

    # -------------------------
    # Layout
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Version 1")
        st.markdown(v1_html, unsafe_allow_html=True)

    with col2:
        st.subheader("Version 2")
        st.markdown(v2_html, unsafe_allow_html=True)