import wx
from apex_legends import ApexLegends

apex = ApexLegends("43c7f765-299a-435f-875f-a85bf9e95466")
#キャラステータスを格納する辞書の宣言
Char_Status = {}
#キャラごとのボックスを作るためのリスト
Char_box = []
#for文中の回数用の変数の宣言 改善できる(?)
num = 0

#メインのクラス
class MyApp():

    def __init__(self):
        super(MyApp,self).__init__()
        self.ui()

    def ui(self):
        #メインのフレーム
        self.frame = wx.Frame(None, wx.ID_ANY,"Apex Legend Status Tracker",size=(550,350))
        self.frame.Center()
        self.frame.CreateStatusBar()
        self.frame.SetStatusText("AL Status Tracker  Status: None")
        #レイアウトの実装
        self.layout = wx.BoxSizer(wx.VERTICAL)
        layout1 = wx.BoxSizer(wx.HORIZONTAL)
        self.layout2 = wx.BoxSizer(wx.VERTICAL)
        self.layout.Add(layout1)
        self.layout.Add(self.layout2,0,wx.GROW)
        self.layout3 = wx.GridSizer(rows=2, cols=4, gap=(0, 0))
        self.layout.Add(self.layout3,1,wx.GROW)
        self.layout4 = wx.BoxSizer(wx.HORIZONTAL)
        self.layout.Add(self.layout4,0)

        #メニューバーの実装
        menu_plat = wx.Menu()
        self.Origin = menu_plat.AppendCheckItem(1, 'Origin')
        self.PSN = menu_plat.AppendCheckItem(2, 'PSN')
        self.XBOX = menu_plat.AppendCheckItem(3, 'Xbox Live')
        self.Origin.Check(False)
        self.PSN.Check(False)
        self.XBOX.Check(False)

        menu_op = wx.Menu()
        menu_op.Append(4, '初期化')
        menu_op.Append(5, '終了')

        menu_bar = wx.MenuBar()
        menu_bar.Append(menu_plat,"プラットフォーム")
        menu_bar.Append(menu_op,"設定")
        self.frame.Bind(wx.EVT_MENU, self.Menu_action)
        self.frame.SetMenuBar(menu_bar)

        #パネルの実装
        self.panel = wx.Panel(self.frame,wx.ID_ANY)
        self.panel.SetBackgroundColour('#bfbfbf')

        #テキストの実装
        text = wx.StaticText(self.panel,wx.ID_ANY,"Enter Your ID here:")
        font1 = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        text.SetFont(font1)
        layout1.Add(text)
        self.text1 = wx.StaticText(self.panel,wx.ID_ANY,"Profile Get Mode: False")
        self.font1 = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.text1.SetForegroundColour('blue')
        self.text1.SetFont(font1)
        self.layout4.Add(self.text1,wx.ALIGN_RIGHT)

        #入力バーの実装
        self.InputID = wx.TextCtrl(self.panel,wx.ID_ANY)
        font2 = wx.Font(14, wx.FONTFAMILY_DEFAULT,
               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.InputID.SetFont(font2)
        layout1.Add(self.InputID, 1)

        #ボタンの実装
        button1 = wx.Button(self.panel,wx.ID_ANY,'Confirm')
        button2 = wx.Button(self.panel,wx.ID_ANY,'Reset')
        button3 = wx.Button(self.panel,wx.ID_ANY,"Start")
        button4 = wx.Button(self.panel,wx.ID_ANY,"Stop")
        layout1.Add(button1)
        layout1.Add(button2)
        self.layout4.Add(button3,wx.ALIGN_RIGHT)
        self.layout4.Add(button4,wx.ALIGN_RIGHT)

        #自分のステータスと8キャラ分のTextCtrlの用意
        self.MySts = wx.TextCtrl(self.panel,wx.ID_ANY, style=wx.TE_CENTER)
        self.layout2.Add(self.MySts, 1, wx.GROW)
        self.MySts.SetFont(font1)
        for i in range(1,9):
            Char_box.append(wx.TextCtrl(self.panel,wx.ID_ANY,style = wx.TE_MULTILINE))
            self.layout3.Add(Char_box[i-1],1,wx.GROW)
            Char_box[i-1].SetFont(font1)

        #ボタンが押されたときの処理
        button1.Bind(wx.EVT_BUTTON, self.clicked1)
        button2.Bind(wx.EVT_BUTTON, self.clicked2)
        button3.Bind(wx.EVT_BUTTON, self.clicked3)
        button4.Bind(wx.EVT_BUTTON, self.clicked4)

        self.panel.SetSizer(self.layout)
        self.frame.Show()

    #メニューのアクションの実装
    def Menu_action(self,event):
        if event.GetId() == 4:
            self.InputID.Clear()
            for i in range(8):
                Char_box[i].Clear()
            self.MySts.Clear()

        if event.GetId() == 5:
            wx.Exit()

    #ステータス取得をする関数
    def Update_Status(self,event):
        try:
            self.PlayerID = self.InputID.GetValue()
            player = apex.player(self.PlayerID)
        #何かしらエラー出たらタイマーを止めて終了処理をする
        except:
            self.timer.Stop()
            self.frame.SetStatusText("AL Status Tracker V.UNK  Status: Some error happened")
            self.text1.SetLabel('Profile Get Mode: False')
            self.text1.SetForegroundColour('blue')

    #Confirmボタンが押されたときの処理
    def clicked1(self,event):
        global num
        #textctrlの初期化
        for i in range(8):
            Char_box[i].Clear()

        self.PlayerID = self.InputID.GetValue()
        player = apex.player(self.PlayerID)
        Player_kills = player.kills
        Player_level = player.level
        #AppendでCharのtextctrlにkill数を渡していく
        self.MySts.SetValue("Level:" + Player_level + "  Total_Kills:" + Player_kills)
        for i in player.legends:
            Char_Status[i.legend_name] = i.kills
            Char_box[num].SetValue(i.legend_name + "_Kills:\n" + i.kills)
            num += 1
        else:
            num = 0

    #Resetボタンが押されたときの処理
    def clicked2(self,event):
        self.InputID.Clear()
        for i in range(8):
            Char_box[i].Clear()
        self.MySts.Clear()

    #StatusGetModeのStartを押したときの処理 wxtimerで一定時間ごとの処理を実装
    def clicked3(self,event):
        self.timer = wx.Timer()
        self.timer.Bind(wx.EVT_TIMER, self.Update_Status)
        self.timer.Start(6000)
        self.frame.SetStatusText("AL Status Tracker V.UNK  Status: Getting Status Per 6000ms")
        self.text1.SetLabel('Profile Get Mode: True')
        self.text1.SetForegroundColour('red')

    #wxtimerを止める
    def clicked4(self,event):
        self.timer.Stop()
        self.frame.SetStatusText("AL Status Tracker V.UNK  Status: None")
        self.text1.SetLabel('Profile Get Mode: False')
        self.text1.SetForegroundColour('blue')


app = wx.App()
MyApp()
app.MainLoop()
