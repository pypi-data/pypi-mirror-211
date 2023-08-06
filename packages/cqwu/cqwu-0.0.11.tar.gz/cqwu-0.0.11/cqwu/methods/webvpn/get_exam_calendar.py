from typing import Union, List

from bs4 import BeautifulSoup

import cqwu
from cqwu.enums import ExamRound
from cqwu.errors import NoExamData
from cqwu.types import AiExam


class GetExamCalendar:
    async def get_exam_calendar(
        self: "cqwu.Client",
        exam_round: Union[str, ExamRound] = ExamRound.Supplementation,
        xue_nian: int = None,
        xue_qi: int = None,
        use_model: bool = False,
    ) -> Union[str, List[AiExam]]:
        """ 获取考试安排表 """
        xue_nian = xue_nian or self.xue_nian
        xue_qi = xue_qi or self.xue_qi
        exam_round = ExamRound(exam_round)
        jw_html = await self.login_jwmis()
        jw_host = self.get_web_vpn_host(jw_html.url, https=True)
        jw_url = f"{jw_host}/cqwljw/student/ksap.ksapb_date.jsp"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-Hans;q=0.8,und;q=0.7,en;q=0.6,zh-Hant;q=0.5,ja;q=0.4',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'DNT': '1',
            'Pragma': 'no-cache',
            'Referer': f'{jw_host}/cqwljw/student/ksap.ksapb.html?menucode=S20403',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        data = {
            'xn': str(xue_nian),
            'xq': str(xue_qi),
            'title': '',
            'xnxq': f'{xue_nian}{xue_qi}',
            'kslc': exam_round.value,
        }
        jw_html = await self.request.post(jw_url, data=data, headers=headers, timeout=60, follow_redirects=True)
        if "没有检索到记录!" in jw_html.text:
            raise NoExamData("没有检索到记录!")
        jw_html = jw_html.text.replace("""<script type="text/javascript" src="//clientvpn.cqwu.edu.cn/webvpn/bundle.debug.js" charset="utf-8"></script>""", "")
        jw_html = jw_html.replace("""<script language='javascript' type='text/javascript' src='../js/Print.js'></script>""", "")
        jw_html = jw_html.replace("charset=GBK", 'charset=UTF-8')
        if not use_model:
            return jw_html
        return parse_html(jw_html, exam_round)


def parse_html(html: str, exam_round: ExamRound) -> List[AiExam]:
    data: List[AiExam] = []
    soup = BeautifulSoup(html, "html.parser")
    trs = soup.find_all("tr")[1:]
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) != 5:
            continue
        data.append(
            AiExam(
                name=tds[0].text,
                credit=float(tds[1].text),
                time=tds[2].text,
                position=tds[3].text,
                seat=tds[4].text,
                exam_round=exam_round,
            )
        )
    return data
