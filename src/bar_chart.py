import streamlit as st
import matplotlib.pyplot as plt


def visualise_bar_chart(question_ids: list, grades: list): 
  # Adjusting the size of the graph
  fig, ax = plt.subplots(figsize=(4, 3))
  font_size = 10
  title_size = 11
  tick_size = 9

  ax.bar(question_ids, grades, color='skyblue')
  ax.set_xlabel('Questions', fontsize=font_size)
  ax.set_ylabel('Grades', fontsize=font_size)
  ax.set_title('Grades per Question and Final Grade', fontsize=title_size)
  ax.set_ylim(0, 5)  # Grade Scale 
  # Adjust tick sizes
  ax.tick_params(axis='both', which='major', labelsize=tick_size)

  st.pyplot(fig, use_container_width=True)