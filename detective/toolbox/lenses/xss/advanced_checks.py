import re
import toml
from urllib.parse import urlparse
from detective.toolbox.risk_levels import RiskLevels


class AdvancedChecks:
    @staticmethod
    def blind_xss(request) -> RiskLevels:
        urls_found = re.findall(r"""(?:<|')\s*(?:i?frame|img|embed|ipt)(?:/|\s).*?src\s*=\s*(?:(?:\"|'|`)\s*)?(?:<\s*)?(?P<url>[^\"'`<>]+)""", request)
        urls_found.append(re.findall(r"""<\s*link(?:/|\s).*?href\s*=\s*(?:(?:\"|'|`)\s*)?(?:<\s*)?(?P<url>[^\"'`<>]+)""", request))
        urls_found.append(re.findall(r"""<\s*meta(?:/|\s).*?content\s*=\s*(?:(?:\"|'|`)\s*)?(?:<\s*)?(?P<url>[^\"'`<>]+)""", request))
        urls_found.append(re.findall(r"""<\s*object(?:/|\s).*?data\s*=\s*(?:(?:\"|'|`)\s*)?(?:<\s*)?(?P<url>[^\"'`<>]+)""", request))
        urls_found.append(re.findall(r"""<\s*style(?:/|\s)*>.*?@\s*import\s*(?:(?:\"|'|`)\s*)?(?:<\s*)?(?P<url>[^\"'`<>]+)""", request))
        urls_found.append(re.findall(r"""<\s*style(?:/|\s)*>.*?body\s*{\s*-moz-binding\s*:[^(]+?\((?:(?:\"|'|`)\s*)?(?:<\s*)?(?P<url>[^\"'`<>]+)""", request))
        urls_found.append(re.findall(r"""<\s*a(?:/|\s).*?href\s*=\s*(?:(?:\"|'|`)\s*)?(?:javascript\s*:\s*document\.location\s*=\s*(?:(?:\"|'|`)\s*)?)?(?:<\s*)?(?P<url>[^\"'`<>]+)""", request))
        if urls_found is not None:
            white_spaces = re.compile(r"\s+")
            server_url = toml.load("server_info.toml")["host"]
            for url in urls_found:
                parse_result = urlparse(re.sub(white_spaces, '', url))
                if parse_result.netloc != '' and url not in server_url:
                    return RiskLevels.CATASTROPHIC
            return RiskLevels.MODERATE
        return RiskLevels.NO_RISK
