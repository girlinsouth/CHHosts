# -*- coding:utf8 -*-

import wx
import os
import platform
import wx.lib.buttons as buttons


class CHHosts(wx.Frame):
    def __init__(self, parent, title):
        if "Windows" in platform.platform():
            self.sysHostsDir = "C:\Windows\System32\drivers\etc"
            self.userHostsDir = "C:\Users\Public\Documents\CHHosts"
        else:
            self.sysHostsDir = "/etc"
            self.userHostsDir = "/etc/CHHosts"
        super(CHHosts, self).__init__(parent, title=title, size=(700, 500))
        self.Center()
        self.panel = wx.Panel(self, -1)
        self.panel.SetBackgroundColour("white")
        self.showUI()
        self.Show()

    def showUI(self):
        addImg = wx.Image("add.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        delImg = wx.Image("del.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        saveImg = wx.Image("save.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        changeImg = wx.Image("ok.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        self.hostNameList = wx.ListBox(self.panel, -1, (20, 20), (80, 120), self.showLeftList(), wx.LB_SINGLE)
        self.hostNameList.SetSelection(0)
        self.hostNameList.Bind(wx.EVT_LISTBOX,self.showHosts)
        self.addBtn = buttons.GenBitmapTextButton(self.panel, -1, addImg, u"添加",size=(90, 30))
        self.addBtn.Bind(wx.EVT_BUTTON,self.addHosts)
        self.delBtn = buttons.GenBitmapTextButton(self.panel, -1, delImg, u"删除",size=(90, 30))
        self.delBtn.Bind(wx.EVT_BUTTON,self.delHosts)
        self.btnBox = wx.BoxSizer(wx.HORIZONTAL)
        self.btnBox.Add(self.addBtn,proportion=0, flag=wx.TOP | wx.RIGHT, border=5)
        self.btnBox.Add(self.delBtn,proportion=0, flag=wx.TOP | wx.RIGHT, border=5)
        self.leftBox = wx.BoxSizer(wx.VERTICAL)
        self.leftBox.Add(self.hostNameList, proportion=1, flag=wx.TOP | wx.EXPAND)
        self.leftBox.Add(self.btnBox, proportion=0, flag=wx.ALIGN_RIGHT|wx.RIGHT)
        self.hostInfoList = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.HSCROLL, size=(450,400))
        hostsFile = self.sysHostsDir
        os.chdir(hostsFile)
        fileInfo = open("hosts")
        self.hostInfoList.SetValue(fileInfo.read().decode("utf8"))
        fileInfo.close()

        self.saveBtnBox = wx.BoxSizer(wx.HORIZONTAL)
        self.saveBtn = buttons.GenBitmapTextButton(self.panel, -1, saveImg, u"保存",size=(90, 30))
        self.changeBtn = buttons.GenBitmapTextButton(self.panel, -1, changeImg, u"切换",size=(90, 30))
        self.saveBtn.Bind(wx.EVT_BUTTON,self.saveHosts)
        self.changeBtn.Bind(wx.EVT_BUTTON,self.changeHosts)
        self.saveBtnBox.Add(self.saveBtn,proportion=0, flag=wx.TOP | wx.RIGHT, border=5)
        self.saveBtnBox.Add(self.changeBtn,proportion=0, flag=wx.TOP | wx.RIGHT, border=5)
        self.rightBox = wx.BoxSizer(wx.VERTICAL)
        self.rightBox.Add(self.hostInfoList,proportion=1, flag=wx.TOP | wx.EXPAND)
        self.rightBox.Add(self.saveBtnBox,proportion=0, flag=wx.ALIGN_RIGHT|wx.RIGHT)

        self.allBox = wx.BoxSizer(wx.HORIZONTAL)
        self.allBox.Add(self.leftBox, proportion=0, flag=wx.TOP | wx.EXPAND)
        self.allBox.Add(self.rightBox, proportion=1, flag=wx.TOP | wx.EXPAND)

        self.panel.SetSizer(self.allBox)

    def showLeftList(self):
        fileNameLists = [u'当前Hosts']
        allFiles = os.listdir(self.userHostsDir)
        for files in allFiles:
            allHostsNames = files.split(".")[0]
            fileNameLists.append(allHostsNames)
        return fileNameLists

    def showHosts(self,event):
        index = event.GetSelection()
        hostname = self.hostNameList.GetString(index)
        if hostname == u'当前Hosts':
            os.chdir(self.sysHostsDir)
            fileInfo = open("hosts")
        else:
            os.chdir(self.userHostsDir)
            fileInfo = open(hostname+".txt")
        self.hostInfoList.SetValue(fileInfo.read().decode("utf8"))
        fileInfo.close()

    def addHosts(self,event):
        dlg = wx.TextEntryDialog(None, u"输入Hosts名称", u"添加Hosts")
        if dlg.ShowModal() == wx.ID_OK:
            hostName = dlg.GetValue()
            if (os.path.exists(self.userHostsDir)) == False:
                os.mkdir(self.userHostsDir)
            os.chdir(self.userHostsDir)
            fileInfo =open((hostName+".txt"),'w')
            self.hostNameList.Append(hostName)
            fileInfo.close()
        dlg.Destroy()

    def saveHosts(self,event):
        hostsInfo = self.hostInfoList.GetValue()
        whichHostsSelect = self.hostNameList.GetSelection()
        hostName = self.hostNameList.GetString(whichHostsSelect)
        os.chdir(self.userHostsDir)
        hostsFile = open((hostName+".txt"),"w")
        hostsFile.write(hostsInfo.encode("utf8"))
        hostsFile.close()
        wx.MessageBox(u"保存成功")

    def changeHosts(self,event):
        hostName = self.hostNameList.GetStringSelection()
        os.chdir(self.sysHostsDir)
        hostsFile = open("hosts",'w')
        hostsInfo = self.hostInfoList.GetValue()
        hostsFile.write(hostsInfo.encode("utf8"))
        hostsFile.close()
        os.chdir(self.userHostsDir)
        hostsFile = open((hostName+".txt"),"w")
        hostsFile.write(hostsInfo.encode("utf8"))
        hostsFile.close()
        wx.MessageBox(u"已切换成"+hostName)

    def delHosts(self,event):
        if self.hostNameList.GetStringSelection() == u'当前Hosts':
            pass
        else:
            dlg = wx.MessageDialog(None,u"是否确认删除："+self.hostNameList.GetStringSelection(), u"提示", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                whichHostsSelect = self.hostNameList.GetSelection()
                hostName = self.hostNameList.GetString(whichHostsSelect)
                os.chdir(self.userHostsDir)
                os.remove(hostName+".txt")
                self.hostNameList.Clear()
                for curlist in self.showLeftList():
                    self.hostNameList.Append(curlist)
            dlg.Destroy()

if __name__ == "__main__":
    app = wx.App()
    CHHosts(None,title='CHHosts V1.0(Windows)')
    app.MainLoop()
