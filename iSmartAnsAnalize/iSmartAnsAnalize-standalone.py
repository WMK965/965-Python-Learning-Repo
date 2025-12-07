import json
import xml.etree.ElementTree as ET
from datetime import datetime
import asyncio
import sys
import signal

# 引入 mitmproxy 核心库
from mitmproxy import options, http, ctx
from mitmproxy.tools.dump import DumpMaster


class AnswerExtractor:
    def __init__(self):
        self.capture_count = 0

    def response(self, flow: http.HTTPFlow):
        # 目标 URL 特征
        target_url_suffix = "/testing/findPaperData.action"

        if target_url_suffix in flow.request.pretty_url:
            self.capture_count += 1
            self.process_data(flow)

    def process_data(self, flow):
        try:
            response_text = flow.response.text
            if not response_text:
                return

            try:
                data = json.loads(response_text)
            except json.JSONDecodeError:
                return

            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except:
                    return

            test_info = data.get("testInfo")
            if not test_info:
                return

            info_list = []
            if isinstance(test_info, dict):
                info_list.append(test_info)
            elif isinstance(test_info, list):
                info_list = test_info
            else:
                return

            current_time = datetime.now().strftime("%H:%M")
            output_lines = []
            output_lines.append(f"### 第{self.capture_count}次捕获({current_time})")

            question_index = 1
            has_answers = False

            for info in info_list:
                if not isinstance(info, dict):
                    continue

                standard_answer_xml = info.get("standardAnswer", "")
                if not standard_answer_xml:
                    continue

                try:
                    xml_content = standard_answer_xml.strip()
                    if not xml_content:
                        continue

                    if xml_content.startswith("<elements>"):
                        root = ET.fromstring(xml_content)
                    else:
                        root = ET.fromstring(f"<root>{xml_content}</root>")

                    elements = root.findall(".//element")

                    for element in elements:
                        answers_list = []
                        for answer in element.findall(".//answer"):
                            ans_id = answer.get("id")
                            ans_text = answer.text
                            if ans_text:
                                answers_list.append(f"{ans_id}.{ans_text.strip()}")

                        if answers_list:
                            has_answers = True
                            formatted_answers = " ".join(answers_list)
                            output_lines.append(f"- 题目{question_index}")
                            output_lines.append(f"\t- 答案：{formatted_answers}")
                            question_index += 1

                except ET.ParseError:
                    pass

            if has_answers:
                final_output = "\n".join(output_lines)
                print("\n" + "=" * 30)
                print(final_output)
                print("=" * 30 + "\n")

                with open("answers_log.md", "a", encoding="utf-8") as f:
                    f.write(final_output + "\n\n")
            else:
                print(f"[{current_time}] null captured")

        except Exception as e:
            print(f"Process error: {e}")


async def start_proxy():
    # 1. 创建选项对象
    # 如果 8080 端口一直报错，可以尝试修改这里的 8080 为 8081
    opts = options.Options(listen_host='0.0.0.0', listen_port=8080)

    # 2. 初始化 Master
    # 【修改点】with_termlog=True 以便查看启动报错信息
    master = DumpMaster(opts, with_termlog=True, with_dumper=True)

    # 3. 设置 TLS 选项
    master.options.update(tls_version_client_min="SSL3")

    # 4. 加载插件
    master.addons.add(AnswerExtractor())

    print("=" * 50)
    print(f"Proxy Started")
    print(f"Port: 8080")
    print(f"Path: ./answers_log.md")
    print("=" * 50)

    try:
        await master.run()
    except KeyboardInterrupt:
        master.shutdown()
    except Exception as e:
        print(f"FATAL ERROR: {e}")


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(start_proxy())
    except KeyboardInterrupt:
        pass