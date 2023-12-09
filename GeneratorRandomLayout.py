import streamlit as st
import pandas as pd
import random

# Python functions from your initial code

def calculate_layout_value(layout, value_map):
    return sum(value_map[letter] for letter in layout) / len(layout)

def generate_random_layout(value_map):
    return ''.join(random.choices(list(value_map.keys()), k=5))

def validate_layout_for_W_and_S_constraints(layout, sets_with_W_count, sets_with_S_count, max_W_per_set, max_S_per_set):
    return (sets_with_W_count + layout.count('W') <= max_W_per_set) and \
           (sets_with_S_count + layout.count('S') <= max_S_per_set)

def generate_varied_layouts_with_all_constraints(layouts_per_set, overall_target_avg, min_avg, max_avg, max_S_per_set, max_W_per_set):
    value_map = {'S': 5, 'G': 4, 'M': 3, 'P': 2, 'A': 1, 'W': 0}
    layouts = []
    sets_with_S_count = 0
    sets_with_W_count = 0

    for _ in range(layouts_per_set):
        layout = generate_random_layout(value_map)
        layout_avg = calculate_layout_value(layout, value_map)

        while not (min_avg <= layout_avg <= max_avg and 
                   validate_layout_for_W_and_S_constraints(layout, sets_with_W_count, sets_with_S_count, max_W_per_set, max_S_per_set)):
            layout = generate_random_layout(value_map)
            layout_avg = calculate_layout_value(layout, value_map)

        layouts.append(layout)
        sets_with_S_count += layout.count('S')
        sets_with_W_count += layout.count('W')

    return layouts

def generate_sets_of_layouts_with_all_constraints(num_sets, layouts_per_set, overall_target_avg, min_avg, max_avg, max_S_per_set, max_W_per_set):
    sets_of_layouts = []
    for _ in range(num_sets):
        set_layouts = generate_varied_layouts_with_all_constraints(layouts_per_set, overall_target_avg, min_avg, max_avg, max_S_per_set, max_W_per_set)
        sets_of_layouts.append(set_layouts)
    return sets_of_layouts

# Streamlit app layout
st.title('Layout Generator')

# Sidebar for input parameters
num_sets = st.sidebar.number_input('Number of Sets', min_value=1, value=6)
layouts_per_set = st.sidebar.number_input('Layouts Per Set', min_value=1, value=5)
overall_target_avg = st.sidebar.number_input('Overall Target Average', min_value=0.0, value=2.6)
min_avg = st.sidebar.number_input('Min Average', min_value=0.0, value=0.875)
max_avg = st.sidebar.number_input('Max Average', min_value=0.0, value=3.0)
max_S_per_set = st.sidebar.number_input('Max S Per Set', min_value=0, value=3)
max_W_per_set = st.sidebar.number_input('Max W Per Set', min_value=0, value=2)

# Button to generate layouts
if st.sidebar.button('Generate Layouts'):
    sets_of_layouts = generate_sets_of_layouts_with_all_constraints(num_sets, layouts_per_set, overall_target_avg, min_avg, max_avg, max_S_per_set, max_W_per_set)
    
    # Displaying the generated sets of layouts
    for i, set_layout in enumerate(sets_of_layouts, start=1):
        st.subheader(f'Set {i}')
        df = pd.DataFrame({'Layout': set_layout})
        df['Average'] = df['Layout'].apply(lambda x: calculate_layout_value(x, {'S': 5, 'G': 4, 'M': 3, 'P': 2, 'A': 1, 'W': 0}))

        # Calculate and append the overall set average
        overall_set_avg = df['Average'].mean()
        overall_set_avg_row = pd.DataFrame([{'Layout': 'Average', 'Average': overall_set_avg}])
        df = pd.concat([df, overall_set_avg_row], ignore_index=True)
        
        st.table(df)
