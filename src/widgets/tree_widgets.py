from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.metrics import dp

def populate_tree_view(tree_view, parent, node, node_dict=None):
    if parent is None:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True))
    else:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True), parent)
    if node_dict != None:
        node_dict[tree_node] = node['node_id']

    for child_node in node['children']:
        populate_tree_view(tree_view, tree_node, child_node, node_dict)


# sample const for the testTree widget:
TREE_DEMO = {'node_id': '1',
        'children': [{'node_id': '1.1',
                      'children': [{'node_id': '1.1.1',
                                    'children': [{'node_id': '1.1.1.1',
                                                  'children': []}]},
                                   {'node_id': '1.1.2',
                                    'children': []},
                                   {'node_id': '1.1.3',
                                    'children': []}]},
                      {'node_id': '1.2',
                       'children': []}]}


class TestTreeWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(TestTreeWidget, self).__init__(**kwargs)

        tv = TreeView(root_options=dict(text='Test Tree'),
                      hide_root=False,
                      indent_level=4)

        populate_tree_view(tv, None, TREE_DEMO)

        self.add_widget(tv)

class RowSelectorWidget(BoxLayout):

    def __init__(self,**kwargs):
        super(RowSelectorWidget, self).__init__(**kwargs)
        self.tree_view = TreeView(hide_root=True,indent_level=4)
        self.add_widget(self.tree_view)
        self.row_values = {}
        self.callback = self.null_callback

    def null_callback(self):
        pass

    def set_callback(self, callback_func):
        self.callback = callback_func

    def on_touch_down(self, touch):
        super(RowSelectorWidget, self).on_touch_down(touch)
        self.callback()

    def setDemoRows(self, numRows):
        self.clearRows()
        for i in range(numRows):
            self.addRow('Row ' + str(i))

    def addRow(self, row_val):
        node = TreeViewLabel(text=str(row_val))
        self.tree_view.add_node(node)
        self.row_values[node] = row_val

    def clearRows(self):
        self.row_values = {}
        self.remove_widget(self.tree_view)
        self.tree_view = TreeView(hide_root=True, indent_level=4)
        self.add_widget(self.tree_view)

    def setRows(self, row_list):
        self.clearRows()
        for r in row_list:
            self.addRow(r)

    def get_selected_row(self):
        sel_node = self.tree_view.selected_node
        if sel_node and sel_node in self.row_values.keys():
            return self.row_values[sel_node]
        else:
            return None

    def remove_selected_row(self):
        sel_node = self.tree_view.selected_node
        if sel_node is not None:
            self.row_values[sel_node] = None
            del self.row_values[sel_node]
            self.tree_view.remove_node(sel_node)

    def get_height(self, expected_node_height= 1.0):
        HEIGHT_FACTOR = 1.1575
        height = 0
        for node in self.tree_view.iterate_all_nodes():
            height += dp(node.height*expected_node_height*HEIGHT_FACTOR)
        return height

    def get_num_Rows(self):
        return len(self.row_values)

class InteractiveTreeWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(InteractiveTreeWidget, self).__init__(**kwargs)
        self.tree_view = TreeView(hide_root=True, indent_level=20)
        self.add_widget(self.tree_view)
        self.node_dict = {}
        self.callback = self.null_callback

    def set_tree(self, tree_dict):
        self.node_dict = {}
        self.remove_widget(self.tree_view)
        self.tree_view = TreeView(hide_root=True, indent_level=20)
        populate_tree_view(self.tree_view, None, tree_dict, node_dict=self.node_dict)
        self.add_widget(self.tree_view)

    def get_height(self):
        height = 0
        for node in self.tree_view.iterate_open_nodes(self.tree_view.root):
            height += node.height
        return height

    def set_demo_tree(self):
        self.node_dict = {}
        self.remove_widget(self.tree_view)
        self.tree_view = TreeView(hide_root=True, indent_level=20)
        populate_tree_view(self.tree_view, None, TREE_DEMO, self.node_dict)
        self.add_widget(self.tree_view)

    def null_callback(self):
        pass

    def set_callback(self, callback_func):
        self.callback = callback_func

    def on_touch_down(self, touch):
        super(InteractiveTreeWidget, self).on_touch_down(touch)
        Clock.schedule_once(self.callback, 0.0)



