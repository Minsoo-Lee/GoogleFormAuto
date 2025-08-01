import wx
from window import main_frame

if __name__ == "__main__":
    app = wx.App(False)
    frame = main_frame.MainFrame()
    frame.Show()
    app.MainLoop()

    # if open_auth_dialog():
    #     print("인증 성공. 메인 실행")
    #     frame = window.MainFrame()
    #     frame.Show()
    #     app.MainLoop()
    # else:
    #     print("인증 실패. 종료합니다.")