from httpx import URL

from .get_calendar import GetCalendar
from .get_calendar_change import GetCalendarChange
from .get_exam_calendar import GetExamCalendar
from .login_jwmis import LoginJwmis
from .login_webvpn import LoginWebVPN


class WebVPN(
    GetCalendar,
    GetCalendarChange,
    GetExamCalendar,
    LoginJwmis,
    LoginWebVPN,
):
    @staticmethod
    def get_web_vpn_host(url: URL, https: bool = False) -> str:
        return next(
            (
                f"https://clientvpn.cqwu.edu.cn/{'https' if https else 'http'}/{i}"
                for i in str(url).split("/")
                if i.startswith("webvpn")
            ),
            None,
        )
