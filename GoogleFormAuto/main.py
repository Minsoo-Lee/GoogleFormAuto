import wx

from auth.auth_window import AuthDialog
from window import main_frame

def open_auth_dialog():
    auth_dialog = AuthDialog()
    auth_dialog.ShowModal()
    result = auth_dialog.auth_success
    auth_dialog.Destroy()
    return result

if __name__ == "__main__":
    app = wx.App(False)
    # frame = main_frame.MainFrame()
    # frame.Show()
    # app.MainLoop()

    if open_auth_dialog():
        print("인증 성공. 메인 실행")
        frame = main_frame.MainFrame()
        frame.Show()
        app.MainLoop()
    else:
        print("인증 실패. 종료합니다.")