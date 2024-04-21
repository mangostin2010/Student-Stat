import streamlit as st
from openpyxl import load_workbook
from deta import Deta
import io

st.set_page_config(page_title='Student\'s Stat', page_icon="🤨")

'# Student\'s Stat'
'#'

DETA_KEY = 'c0ki5D3avML_gSssDuj33rfuzLDrjwL1gc42oQkbgsHj'
deta = Deta(DETA_KEY)
db = deta.Drive("Leaking")

file_list = db.list()["names"]

for x in file_list:
    file = db.get(x)
    file_stream = io.BytesIO(file.read())

load_wb = load_workbook(file_stream, data_only=True)
# 시트 이름으로 불러오기 
load_ws = load_wb['Spring 2024']


def get_student(sex):
    students = {}
    if sex == "boy":
        words = ["M", "K", "A"]
        number_of_student = 5
    else:
        words = ["Z", "X", "N"]
        number_of_student = 4

    i = 2
    # 남학생 이름 모두 출력
    for x in range(number_of_student): # 남학생이 5명 이므로 5번
        if load_ws[f'{words[0]}{i+10}'].value != None:
            average = round(load_ws[words[0] + str(i+10)].value, 1)
        else:
            average = round(load_ws[words[1] + str(i+11)].value, 1)

        students[load_ws[words[2] + str(i)].value] = [average, load_ws[f'{words[0]}{i+11}'].value]
        i += 13
    return students

boys = get_student('boy')
girls = get_student('girl')

# Listing Students ------------------------------------------------------------------------
students = boys | girls
# Chunking students into groups of 3
chunk_size = 2
chunks = [list(students.items())[i:i + chunk_size] for i in range(0, len(students), chunk_size)]

# Displaying students in a grid layout
for idx, chunk in enumerate(chunks):
    cols = st.columns(chunk_size)
    for col, (name, data) in zip(cols, chunk):
        with col:
            with st.container(height=150):
                st.subheader(name)
                f"""Average: **{data[0]}**  
                Finished PACEs: **{data[1]}**"""
    # Add a divider after each row except for the last row
    if idx < len(chunks) - 1:
        st.divider()
# CSS ------------------------------------------------------------------------
css = """
<style>
header {visibility: hidden;}

.st-emotion-cache-m6izvh {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);    
    transition: box-shadow .15s,transform .15s;
}
h3 {
    padding: 0.5rem 0px 0.2rem;
    line-height: 1.43;
    
}
.st-emotion-cache-m6izvh:hover {
    transform: translateY(-10px);
    background: #eaeaea;
}
@media (max-width: 50.5rem) {
  .st-emotion-cache-gh2jqd {
    max-width: calc(-2.5rem + 100vw);
  }
  h1 {
    font-size:210%;
  }
}

.st-emotion-cache-eczf16 {
    display: none;
}
</style>
"""
st.html(css)
