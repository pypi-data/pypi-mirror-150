from pyqtgraph.Qt import QtWidgets
from pyqtgraph.parametertree import Parameter, ParameterTree
from PyQt5.QtWidgets import QApplication
import yaml

if __name__ == '__main__':
    app = QApplication([])

    params = [
        {'name': 'Sample File', 'type': 'group', 'children': [
            {'name': 'viewMode', 'type': 'list', 'values': ["Detail", "List"], 'value': "Detail"},
            {'name': 'directory', 'type': 'str', 'dec': True},
            {'name': 'Remove extra items', 'type': 'bool', 'value': True},
        ]}
    ]
    # params = yaml.load(f, Loader=yaml.FullLoader)

    # Create tree of Parameter objects
    p = Parameter.create(name='params', type='group', children=params)

    # Create two ParameterTree widgets, both accessing the same data
    t = ParameterTree()
    t.setParameters(p, showTop=False)
    t.show()
    t.setWindowTitle('pyqtgraph example: Parameter Tree')

    app.exec()
