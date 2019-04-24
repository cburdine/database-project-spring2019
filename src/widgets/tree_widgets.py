from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.uix.boxlayout import BoxLayout

def populate_tree_view(tree_view, parent, node):
    if parent is None:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True))
    else:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True), parent)

    for child_node in node['children']:
        populate_tree_view(tree_view, tree_node, child_node)


tree = {'node_id': '1',
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

        populate_tree_view(tv, None, tree)

        self.add_widget(tv)

class RowSelectorWidget(BoxLayout):

    def __init__(self,**kwargs):
        super(RowSelectorWidget, self).__init__(**kwargs)
        self.tree_view = TreeView(hide_root=True,indent_level=4)
        self.add_widget(self.tree_view)
        self.row_names = {}
        self.callback = None

    def set_callback(self, callback_func):
        self.callback = callback_func

    def on_touch_down(self, touch):
        super(RowSelectorWidget, self).on_touch_down(touch)
        self.callback()

    def setDemoRows(self, numRows):
        self.clearRows()
        for i in range(numRows):
            self.addRow('Row ' + str(i))

    def addRow(self, row_text):
        node = TreeViewLabel(text=str(row_text))
        self.tree_view.add_node(node)
        self.row_names[node] = str(row_text)

    def clearRows(self):
        self.row_names = {}
        self.remove_widget(self.tree_view)
        self.tree_view = TreeView(hide_root=True, indent_level=4)
        self.add_widget(self.tree_view)

    def setRows(self, row_text_list):
        self.clearRows()
        for r in row_text_list:
            self.addRow(r)

    def get_selected_row(self):
        sel_node = self.tree_view.selected_node
        if sel_node and sel_node in self.row_names:
            return self.row_names[sel_node]
        else:
            return None

    def get_height(self):
        #TODO: Account for text wrapping
        return 14 * len(self.row_names) + 60

    def get_num_Rows(self):
        return len(self.row_names)

