# created by Ira Garrett
'''


'''
import random

from matplotlib import pyplot as plt

import file_manipulators.generic_file_operators
import file_manipulators.json_file_operators
from objects.History_of_News_Entry import History_of_News_Entry
import manipulate_history_of_news_entries_db
import cosine_similarity
import news_parser
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from cust_logging.logger import Log
Log = Log('main_gui.py')
import global_vars
import networkx as nx
import matplotlib.pyplot as plt
from objects import News_Source
import time
import gui.nodes_gui

class Gui():
    def __init__(self):
        self.story_text = []

        self.root = tk.Tk()
        self.root.geometry("600x200")
        self.root.title("News Aggregator")

        self.edge_colors = []

        # initial graph
        self.G = nx.Graph()
        # enter main page
        self.main_page()


        #self.headline_relations()

        pass



    # headline relations
    '''
        create graphs of the headlines for rss feeds, and plot relations between them
    '''
    def pull_news_articles(self):
        new_pull_root = tk.Toplevel()
        new_pull_root.geometry('1200x600')

        # start by loading the rss sources file
        sources = file_manipulators.generic_file_operators.read_file(global_vars.rss_feeds_file)

        edge_colors = []

        num = 0

        # 1. Create Canvas
        canvas = tk.Canvas(new_pull_root)
        canvas.pack(fill='both', expand=True)

        text = tk.Text(canvas, width=300, height=200)
        text.pack(fill='both', expand=True)



        for i, src in enumerate(sources):
            src_color = (random.random(), random.random(), random.random())

            Log.log(f'checking source {src}')
            # convert to news source instance
            ns = News_Source.News_Source(src)

            for j, entry in enumerate(ns.entries):
                '''# check if the entry is already in the history of news entries database
                if manipulate_history_of_news_entries_db.entry_title_in_db(entry['title']):
                    Log.log(f"{entry['title']} is in the history of news entries db")
                '''
                Log.log(f"entry num {num} = {entry['title']}")

                # perform 1 request per second
                # time.sleep(1)

                num+=1
                #if num > 5:
                #    break

                body = news_parser.read_page_body(entry['url'])

                # History_Entry = (entry['title'],entry['url'],body,entry['published'])
                History_Entry = History_of_News_Entry(entry['title'], entry['url'], body, entry['published'])

                text.insert(tk.END, f"[{i+1}/{len(sources)}]({j+1}/{len(ns.entries)}) {entry['title']} \t {entry['url']}  \n")
                text.see(tk.END)
                new_pull_root.update()

                self.story_text.append(History_Entry)

                manipulate_history_of_news_entries_db.write_append_history_of_news_entries_json(History_Entry)

                self.G.add_node(entry['title'], color=src_color, source=src, font_size=8)
                # node_colors.append(src_color)

            # Bind mouse wheel to scroll
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))



    def build_graphs(self):
        gui.nodes_gui.display_nodes_gui(self.story_text)
        #gui(self.story_text)

        # try checking cosine similarity between them all
        data_frame = cosine_similarity.data_to_vector(self.story_text)
        similarity_matrix = cosine_similarity.cosine_similarity(data_frame)

        Log.log(f"creating edges for graph")

        # somehow update the graph to match? idk

        Log.log(f"Story text titles\n{[entry.get()['title'] for entry in self.story_text]}")

        for i in range(similarity_matrix.shape[0]):
            i_pos = i
            #Log.log(f"i = {i}")
            for j in range(i_pos + 1, similarity_matrix.shape[1]):
                j_pos = j

                sim = similarity_matrix[i][j]
                # round sim value
                sim = round(sim, 4)
                similarity_delim_line = float(self.label_val.get())

                Log.log(f"entry num {i_pos} = {self.story_text[i_pos].get()['title']}? and entry num {j_pos} = {self.story_text[j_pos].get()['title']}? and sim = {sim} and delim - {similarity_delim_line}")


                # if the similarity is over the line, but not a  perfect match (since a perfect match is suspicious)
                if sim >= similarity_delim_line and sim != 1:

                    print(f" |{i},{j}| ", end="")

                    # add another edge color (r, g, 0*b)
                    self.edge_colors.append((
                        1 - sim,
                        sim,
                        0))
                    self.G.add_edge(self.story_text[i_pos].get()['title'], self.story_text[j_pos].get()['title'], weight=sim * 10)

                    # Log.log(f"edge between ({i},{j}) \t \"{story_text[i]['title']}\" and \"{story_text[j]['title']}\"")



        # 1. Enable interactive mode
        plt.ion()
        fig, ax = plt.subplots()

        nx.draw(self.G, ax=ax, with_labels=True, font_size=8)
        plt.draw()
        plt.pause(0.5)



        #Log.log(f"node colors len={len(node_colors)}\nedge colors len={len(edge_colors)}")
        #Log.log(f"nodes length={len(G.nodes)} = {G.nodes} ")

        # Log.log(f"nodes = {G.nodes}")
        node_colors = []
        for i, node in enumerate(self.G.nodes):
            Log.log(f"node = {node} ; color={self.G.nodes[node]["color"]}")
            node_colors.append(self.G.nodes[node]["color"])

        # Redraw only nodes and edges to update view
        ax.clear()
        pos_G = nx.spring_layout(self.G)
        nx.draw(self.G, pos_G, ax=ax, with_labels=True, node_color=node_colors, edge_color=self.edge_colors, font_size=8)
        plt.draw()
        plt.title("Graph of All Nodes")
        plt.show(block=False)

        # 4. Embed in Tkinter
        #canvas = FigureCanvasTkAgg(fig, master=self.root)
        #canvas.draw()
        #canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 1. Identify Subgraphs (Connected Components)
        components = list(nx.connected_components(self.G))
        print(f"components = {components}")

        subgraphs = [self.G.subgraph(c).copy() for c in components]

        for subgraph in subgraphs:
            # don't load graphs of individual nodes
            if len(subgraph) <= 1:
                continue

            # create edge graph
            H = nx.Graph()
            h_node_colors = []
            for i, node in enumerate(subgraph.nodes):
                Log.log(f"node = {node} ; color={subgraph.nodes[node]["color"]}")

                # if they have edges attached to thme, add to H graph
                # if subgraph.degree(node) != 0:
                h_node_colors.append(self.G.nodes[node]["color"])
                H.add_node(node)

            # h_edge_colors = []
            H.add_edges_from(subgraph.edges)
            pos_H = nx.spring_layout(H)
            plt.figure()
            nx.draw(H, pos_H, with_labels=True, node_color=h_node_colors, edge_color=self.edge_colors, font_size=8)
            plt.title("Graph from Edge Collection")
            plt.show(block=False)

        plt.show(block=True)


    # main page
    '''
        main page
    '''
    def main_page(self):

        # Create a frame
        ''' in a frame '''
        buttons_frame = tk.Frame(self.root, bg="lightblue", padx=10, pady=10, height=50)
        buttons_frame.pack(fill='x',side='top', padx=20, pady=20, expand=True)

        btn = tk.Button(buttons_frame, text='Load News Stories',
                        command=self.pull_news_articles)
        btn.pack(side='left')

        # 5 let's add a button
        btn = tk.Button(buttons_frame, text='Perform Analysis',
                        command=self.build_graphs)
        btn.pack(side='right')


        # another frame
        ''' in a frame '''
        frame = tk.Frame(self.root, bg="lightblue", padx=10, pady=10)
        frame.pack(fill='x', side='top', padx=20, pady=20, expand=True)

        self.label_val = tk.StringVar()
        self.label_val.set(f"{0.25}")

        def slider_changed(event):
            self.label_val.set(round(self.slider.get(),2))

        self.slider = ttk.Scale(
            frame,
            from_=0,
            to=1,
            orient='horizontal',
            command=slider_changed,
            length=400
        )
        self.slider.pack(side='left', padx=20)

        label = tk.Label(frame, textvariable=self.label_val, font=("Arial", 15))
        label.pack(side='left', padx=20)


        self.root.mainloop()
