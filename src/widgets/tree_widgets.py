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
        self.tree_view = TreeView(hide_root=True,
                      indent_level=4)
        self.add_widget(self.tree_view)

    def addRow(self, row_text):
        node = TreeViewLabel(text=row_text)
        self.tree_view.add_node(node)

    def setRows(self, row_text_list):
        for node in self.tree_view.iterate_all_nodes():
            self.tree_view.remove_node(node)

        for r in row_text_list:
            self.addRow(r)

