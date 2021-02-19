import c4d
from c4d import gui
from c4d import plugins

PLUGIN_ID = 1000001  # Test plugin id
PLUGIN_ID_ND = 1000002  # Test plugin id


class ListItem(plugins.NodeData):
    def Init(self, node):
        # do stuff here
        return True


class Tvf(gui.TreeViewFunctions):
    def GetFirst(self, root, userdata):
        if not root:
            return None
        return root.GetFirst()


    def GetNext(self, root, userdata, obj):
        return obj.GetNext()


    def GetName(self, root, userdata, obj):
        return obj.GetName()


    def SetName(self, root, userdata, obj, str):
        obj.SetName(str)


class TestDialog(gui.GeDialog):
    def __init__(self):
        self.items = c4d.GeListHead()
        self.treegui = None
        self.tvf = Tvf()


    def add_item(self):
        item = c4d.BaseList2D(PLUGIN_ID_ND)
        item.SetName("ListItem")
        item.InsertUnder(self.items)


    def CreateLayout(self):
        settings = c4d.BaseContainer()
        settings.SetBool(c4d.TREEVIEW_HAS_HEADER, True)

        self.treegui = self.AddCustomGui(0, c4d.CUSTOMGUI_TREEVIEW, "",
                                         c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT,
                                         300,
                                         300,
                                         settings)

        return True


    def InitValues(self):
        for x in range(5):
            self.add_item()

        layout_bc = c4d.BaseContainer()
        layout_bc.SetInt32(0, c4d.LV_TREE)
        self.treegui.SetLayout(1, layout_bc)

        self.treegui.SetHeaderText(0, "Name")
        self.treegui.Refresh()

        self.treegui.SetRoot(self.items, self.tvf, None)
        return True


class TestCommand(plugins.CommandData):
    def __init__(self):
        self.dlg = None


    def Register(self):
        return plugins.RegisterCommandPlugin(PLUGIN_ID, "Test-Plugin", 0, None, None, self)


    def Execute(self, doc):
        if self.dlg is None:
            self.dlg = TestDialog()

        return self.dlg.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaulth=400, defaultw=400)


    def RestoreLayout(self, sec_ref):
        if self.dlg is None:
            self.dlg = TestDialog()

        return self.dlg.Restore(pluginid=PLUGIN_ID, secret=sec_ref)


if __name__ == '__main__':
    TestCommand().Register()
    plugins.RegisterNodePlugin(PLUGIN_ID_ND, "ListItem", c4d.PLUGINFLAG_HIDE, ListItem, None)
