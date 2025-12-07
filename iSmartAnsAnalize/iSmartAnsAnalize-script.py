# works with mitmdump
# mitmdump -s extract_answers.py --set tls_version_client_min=TLS1_0

import json
import xml.etree.ElementTree as ET
from datetime import datetime
from mitmproxy import http, ctx

class AnswerExtractor:
    def __init__(self):
        self.capture_count = 0

    def response(self, flow: http.HTTPFlow):
        # 目标 URL 特征
        target_url_suffix = "/testing/findPaperData.action"
        
        # 检查 URL 是否匹配
        if target_url_suffix in flow.request.pretty_url:
            self.capture_count += 1
            self.process_data(flow)

    def process_data(self, flow):
        try:
            response_text = flow.response.text
            if not response_text:
                return

            # 1. 解析 JSON
            try:
                data = json.loads(response_text)
            except json.JSONDecodeError:
                return

            # 处理双重编码 (以防万一)
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except:
                    return

            # 2. 获取 testInfo
            test_info = data.get("testInfo")
            if not test_info:
                return

            # 3. 统一化处理：将 testInfo 转换为列表以便统一遍历
            # 如果是字典（实际抓包情况），放入列表中；如果是列表（最初示例），直接使用
            info_list = []
            if isinstance(test_info, dict):
                info_list.append(test_info)
            elif isinstance(test_info, list):
                info_list = test_info
            else:
                ctx.log.warn(f"未知的 testInfo 类型: {type(test_info)}")
                return

            # 准备输出
            current_time = datetime.now().strftime("%H:%M")
            output_lines = []
            output_lines.append(f"### 第{self.capture_count}次捕获({current_time})")
            
            question_index = 1
            has_answers = False

            # 4. 遍历提取答案
            for info in info_list:
                if not isinstance(info, dict):
                    continue

                standard_answer_xml = info.get("standardAnswer", "")
                
                if not standard_answer_xml:
                    continue

                try:
                    # XML 解析
                    # 实际数据以 <elements> 开头
                    xml_content = standard_answer_xml.strip()
                    if not xml_content:
                        continue
                        
                    # 防止 XML 解析报错，确保有根节点
                    if xml_content.startswith("<elements>"):
                        root = ET.fromstring(xml_content)
                    else:
                        # 如果没有根节点，手动包裹
                        root = ET.fromstring(f"<root>{xml_content}</root>")

                    # 查找所有的题目节点 (element)
                    # 结构: <elements><element><answers>...</answers></element></elements>
                    elements = root.findall(".//element")
                    
                    for element in elements:
                        answers_list = []
                        # 查找该题目下的所有答案
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

                except ET.ParseError as e:
                    ctx.log.error(f"XML 解析失败: {e}")

            # 5. 输出结果
            if has_answers:
                final_output = "\n".join(output_lines)
                
                print("\n" + "="*30)
                print(final_output)
                print("="*30 + "\n")
                
                with open("answers_log.md", "a", encoding="utf-8") as f:
                    f.write(final_output + "\n\n")
            else:
                ctx.log.warn("本次捕获未提取到有效答案 (standardAnswer 可能为空或解析失败)")

        except Exception as e:
            ctx.log.error(f"处理错误: {e}")

addons = [
    AnswerExtractor()
]