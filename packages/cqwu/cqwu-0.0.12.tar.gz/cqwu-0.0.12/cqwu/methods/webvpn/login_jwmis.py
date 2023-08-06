from httpx import Response

import cqwu
from cqwu.errors import CookieError


class LoginJwmis:
    async def login_jwmis(
        self: "cqwu.Client",
    ) -> Response:
        """ 登录教学管理平台 """
        jw_html = await self.request.get(
            f"{self.web_ehall_path}/appShow?appId=5299144291521305", follow_redirects=True
        )
        if "教学管理服务平台" not in jw_html.text:
            raise CookieError
        return jw_html
