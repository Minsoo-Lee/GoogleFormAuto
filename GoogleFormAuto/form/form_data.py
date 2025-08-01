import wx

class FormData:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FormData, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if FormData._initialized:
            return  # 이미 초기화된 경우, 바로 리턴

        self.url = None
        self.count = None

        FormData._initialized = True

    def set_data(self, url, count):
        # 1) 비어있는지 확인
        if not count:
            wx.MessageBox("반복 횟수를 입력해주세요.", "오류", wx.OK | wx.ICON_ERROR)
            return -1

        # 2) 숫자인지 확인
        if not count.isdigit():
            wx.MessageBox("정수만 입력할 수 있습니다.", "오류", wx.OK | wx.ICON_ERROR)
            return -1

        # 3) 정수 변환
        self.count = int(count)

        self.url = url
        return 1

    def get_url(self):
        return self.url

    def get_count(self):
        return self.count
