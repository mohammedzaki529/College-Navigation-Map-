import streamlit as st
import heapq
from collections import deque

st.set_page_config(page_title="College Campus Master Navigation System", layout="wide")
st.title("College Campus Multi-Route AI Navigation System")

# --- 1. MASTER CAMPUS GRAPH (All 6 Routes Integrated) ---
campus_graph = {
    'Main_Gate': {
        'Gate_1': {'cost': 58, 'action': 'Walk 58 steps from Main Gate to Gate 1'}
    },
    'Gate_1': {
        'Gate_Entry_Inner': {'cost': 15, 'action': 'Walk 15 steps inside after entry'}
    },
    
    # --- STARTING JUNCTION FOR ALL ROUTES ---
    'Gate_Entry_Inner': {
        # Route 1 (Via Stairs 1)
        'GF_Classes': {'cost': 79, 'action': 'Take left turn and walk 79 steps to GF classes'},
        # Route 2 & 3 & 4 (Via Stairs 2)
        'Route2_Turn1': {'cost': 30, 'action': 'Walk 30 steps from Inner Gate 1'},
        'Route3_Turn1': {'cost': 70, 'action': 'Take left turn and walk 70 steps towards Stairs 2 path'},
        'Route4_Turn1': {'cost': 70, 'action': 'Take left turn and walk 70 steps towards balcony'},
        # Route 5 (Via Library, Water Hut & Stairs 4)
        'Route5_Start': {'cost': 15, 'action': 'Walk 15 steps from inner gate entry'},
        # Route 6 (Via Stairs 3 & Balcony)
        'Route6_Start': {'cost': 15, 'action': 'Walk 15 steps from inner gate entry'}
    },

    # --- ROUTE 1 (Via Stairs 1) ---
    'GF_Classes': {
        'Corridor_Point_1': {'cost': 10, 'action': 'Take right turn and walk 10 steps'}
    },
    'Corridor_Point_1': {
        'Stairs_1_Base': {'cost': 20, 'action': 'Take left turn and climb 20 steps (Stairs 1)'}
    },
    'Stairs_1_Base': {
        'Corridor_Point_2': {'cost': 10, 'action': 'Take right turn and walk 10 steps on 1st Floor'}
    },
    'Corridor_Point_2': {
        'Water_Hut': {'cost': 42, 'action': 'Take right turn and walk 42 steps to Water Hut landmark'}
    },
    'Water_Hut': {
        'Pre_Auditorium': {'cost': 35, 'action': 'Take right turn and walk 35 steps'}
    },
    'Pre_Auditorium': {
        'Auditorium': {'cost': 5, 'action': 'Take left turn to reach Auditorium'}
    },

    # --- ROUTE 2 (Via Stairs 2 - Standard Corridor) ---
    'Route2_Turn1': {
        'Stairs_2_Base': {'cost': 20, 'action': 'Take left turn and climb 20 stairs (Stairs 2)'}
    },
    'Stairs_2_Base': {
        'Route2_Corridor': {'cost': 15, 'action': 'Take right turn and walk 15 steps'}
    },
    'Route2_Corridor': {
        'Route2_Pre_Auditorium': {'cost': 112, 'action': 'Take right turn and walk 112 steps'}
    },
    'Route2_Pre_Auditorium': {
        'Auditorium': {'cost': 35, 'action': 'Take right turn, walk 35 steps, and left turn to reach Auditorium'}
    },

    # --- ROUTE 3 (Via Stairs 2 - Alternative Corridor) ---
    'Route3_Turn1': {
        'Route3_Turn2': {'cost': 50, 'action': 'Take left turn and walk 50 steps'}
    },
    'Route3_Turn2': {
        'Route3_Turn3': {'cost': 60, 'action': 'Take left turn and walk 60 steps'}
    },
    'Route3_Turn3': {
        'Route3_Turn4': {'cost': 42, 'action': 'Take right turn and walk 42 steps'}
    },
    'Route3_Turn4': {
        'Route3_Pre_Auditorium': {'cost': 36, 'action': 'Take right turn and walk 36 steps'}
    },
    'Route3_Pre_Auditorium': {
        'Auditorium': {'cost': 5, 'action': 'Take left turn to reach Auditorium'}
    },

    # --- ROUTE 4 (Via Stairs 2, Balcony & Stairs 3) ---
    'Route4_Turn1': {
        'Route4_Balcony': {'cost': 50, 'action': 'Take left turn and walk 50 steps near balcony area'}
    },
    'Route4_Balcony': {
        'Route4_Stairs3_Junction': {'cost': 20, 'action': 'Take right turn (10 steps) and left turn (10 steps) near Stairs 3'}
    },
    'Route4_Stairs3_Junction': {
        'Route4_Corridor_Long': {'cost': 70, 'action': 'Walk 70 steps and take left turn'}
    },
    'Route4_Corridor_Long': {
        'Auditorium': {'cost': 30, 'action': 'Walk 30 steps and take right turn to reach Auditorium'}
    },

    # --- ROUTE 5 (Via Library, Water Hut & Stairs 4) ---
    'Route5_Start': {
        'Route5_Library_Area': {'cost': 150, 'action': 'Take left turn and walk 150 steps towards waterhut and library area'}
    },
    'Route5_Library_Area': {
        'Route5_Stairs4_Entry': {'cost': 45, 'action': 'Take right turn and walk 45 steps'}
    },
    'Route5_Stairs4_Entry': {
        'Stairs_4_GF_Base': {'cost': 25, 'action': 'Take left (5 steps), right (20 steps) to reach Stairs 4 Ground Floor'}
    },
    'Stairs_4_GF_Base': {
        'Stairs_4_1F_Top': {'cost': 25, 'action': 'Climb 25 steps up Stairs 4 to First Floor'}
    },
    'Stairs_4_1F_Top': {
        'Route5_Corridor_Walk': {'cost': 45, 'action': 'Take left (5 steps), turn (20 steps), right (20 steps)'}
    },
    'Route5_Corridor_Walk': {
        'Auditorium': {'cost': 5, 'action': 'Take final right turn to reach Auditorium'}
    },

    # --- ROUTE 6 (Via Stairs 3 & Balcony) ---
    'Route6_Start': {
        'Route6_Turn1': {'cost': 70, 'action': 'Take left turn and walk 70 steps'}
    },
    'Route6_Turn1': {
        'Route6_Turn2': {'cost': 50, 'action': 'Take right turn and walk 50 steps'}
    },
    'Route6_Turn2': {
        'Stairs_3_GF_Base': {'cost': 20, 'action': 'Take left turn and walk 20 steps to Stairs 3'}
    },
    'Stairs_3_GF_Base': {
        'Stairs_3_1F_Top': {'cost': 20, 'action': 'Climb 20 steps up Stairs 3 to First Floor'}
    },
    'Stairs_3_1F_Top': {
        'Route6_Balcony': {'cost': 70, 'action': 'Walk 70 steps through balcony area'}
    },
    'Route6_Balcony': {
        'Route6_Pre_Auditorium': {'cost': 30, 'action': 'Take right turn and walk 30 steps'}
    },
    'Route6_Pre_Auditorium': {
        'Auditorium': {'cost': 5, 'action': 'Take final right turn to reach Auditorium'}
    },

    'Auditorium': {}
}

# Heuristics for A* Search
campus_heuristics = {
    'Main_Gate': 300,
    'Gate_1': 242,
    'Gate_Entry_Inner': 227,
    'GF_Classes': 148,
    'Corridor_Point_1': 138,
    'Stairs_1_Base': 118,
    'Corridor_Point_2': 108,
    'Water_Hut': 66,
    'Pre_Auditorium': 31,
    'Route2_Turn1': 197,
    'Stairs_2_Base': 177,
    'Route2_Corridor': 162,
    'Route2_Pre_Auditorium': 50,
    'Route3_Turn1': 157,
    'Route3_Turn2': 107,
    'Route3_Turn3': 47,
    'Route3_Turn4': 36,
    'Route3_Pre_Auditorium': 10,
    'Route4_Turn1': 157,
    'Route4_Balcony': 107,
    'Route4_Stairs3_Junction': 87,
    'Route4_Corridor_Long': 30,
    'Route5_Start': 227,
    'Route5_Library_Area': 77,
    'Route5_Stairs4_Entry': 32,
    'Stairs_4_GF_Base': 55,
    'Stairs_4_1F_Top': 30,
    'Route5_Corridor_Walk': 10,
    'Route6_Start': 227,
    'Route6_Turn1': 157,
    'Route6_Turn2': 107,
    'Stairs_3_GF_Base': 87,
    'Stairs_3_1F_Top': 67,
    'Route6_Balcony': 35,
    'Route6_Pre_Auditorium': 10,
    'Auditorium': 0
}

#======A* Search Algot=rtihm ====

def a_star(graph, heuristics, start, goal):
    open_set = []
    heapq.heappush(open_set, (0 + heuristics.get(start, 0), start, [start], 0))
    visited = set()
    while open_set:
        f_score, current, path, g_score = heapq.heappop(open_set)
        if current == goal:
            return path, g_score
        if current in visited:
            continue
        visited.add(current)
        for neighbor , edge_info in graph.get(current, {}).items():
            if neighbor not in visited:
                cost = edge_info['cost']
                new_g = g_score + cost
                new_f = new_g + heuristics.get(neighbor, 0)
                heapq.heappush(open_set, (new_f, neighbor, path + [neighbor], new_g))
    return None, float('inf')
#======bfs search===============\
def bfs(graph, start, goal):
    queue = deque([(start, [start],0)])
    visited = {start}
    while queue:
        current, path, total_cost = queue.popleft()
        if current == goal:
            return path , total_cost
        for neighbor , edge_info in graph.get(current ,{}).items():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor,path + [neighbor], total_cost + edge_info['cost']))
    return None, float('inf')

#========dfs search===========
def dfs(graph , start , goal):
    stack = [(start, [start], 0)]
    visited = set()
    while stack:
        current, path, total_cost = stack.pop()
        if current == goal:
            return path, total_cost
        if current not in visited:
            visited.add(current)
            for neighbor,edge_info in graph.get(current,{}).items():
                if neighbor not in visited:
                    stack.append((neighbor,path+[neighbor], total_cost+edge_info['cost']))
    return None, float('inf')

#hanji steamlit se ui bane ab=======
all_nodes = list(campus_graph.keys())

col1, col2, col3 = st.columns(3)
with col1:
    start_node = st.selectbox("Select Start Location jahan aap:", all_nodes, index=0)
with col2:
    goal_node = st.selectbox("Select Destination:", all_nodes, index=all_nodes.index('Auditorium'))
with col3:
    algo_choice = st.selectbox("konsa Ai istemaal karoge :", ["A* Search", "BFS", "DFS"])

if st.button("Find Navigation Route"):
    if start_node == goal_node:
        st.warning("Start aur Destination same nahi ho sakte!")
    else:
        if algo_choice == "A* Search":
            path, cost = a_star(campus_graph, campus_heuristics, start_node, goal_node)
        elif algo_choice == "BFS":
            path, cost = bfs(campus_graph, start_node, goal_node)
        else:
            path, cost = dfs(campus_graph, start_node, goal_node)

        if path:
            st.success(f"Path successfully mil gaya using {algo_choice}! Total Cost: {cost} steps")
            
            st.markdown("### Turn-by-Turn Navigation Instructions:")
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i+1]
                action_detail = campus_graph[u][v]['action']
                step_cost = campus_graph[u][v]['cost']
                st.info(f"**Step {i+1}:** {action_detail} *(Approx. {step_cost} steps)*")
            
            st.markdown("### Complete Node Traversal Sequence:")
            st.code(" -> ".join(path))
        else:
            st.error("Selected locations ke beech koi valid path nahi mila.")