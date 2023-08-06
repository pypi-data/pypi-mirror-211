from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
import xml.etree.ElementTree as etree
import re

INPUTS_RE = r"\[\[(?P<fields>(?:(?:(?!\[\[).)+?)?)\]\]"


class InputsInlineProcessor(InlineProcessor):

    def handleMatch(self, m, data):
        # 定义正则表达式
        sub_pattern = re.compile(r"(\w+)\s*=\s*('[^']*'|\"[^\"]*\"|\w+)")

        # 查找匹配的字段
        sub_matches = re.findall(sub_pattern, m.group(1))

        # Create the Element
        el = etree.Element('span')

        # 输出结果
        # 格式为： [[id='eid1', type='etype1', value='evalue1', opt='eopt1:eopt2', class=dfaj]]
        input_html = ""

        input_type = ""
        input_value = ""
        input_opt = ""
        input_opt_value = ""

        for sub_match in sub_matches:
            field, value = sub_match[0], sub_match[1].strip("'\"")  # 去除可能存在的引号
            if field == "id" :
                input_id = value
            elif field == "type" :
                input_type = value
            elif field == "value" :
                input_value = value
            elif field == "opt" :
                input_opt = value
            elif field == "opt_value" :
                input_opt_value = value

        if input_type == "":
            el.text = m.group(0)
            return el, m.start(0), m.end(0)

        input_html = ""

        # add input type
        if input_type == "select" :
            input_html = "<select "
        else:
            input_html = "<input type='" + input_type + "' "

        # add other fields
        for sub_match in sub_matches:
            field, value = sub_match[0], sub_match[1].strip("'\"")  # 去除可能存在的引号
            if field == "type" or field == "opt" or field == "opt_value":
                continue

            input_html += field + "='" + value + "' "
        
        # add default value or options and close tag
        if input_type == "select" and input_opt != "":
            input_html += ">"
            input_opt_list = input_opt.split(":")
            input_opt_value_list = input_opt_list
            if input_opt_value != "":
                opt_value_list = input_opt_value.split(":")
                if len(opt_value_list) == len(input_opt_list):
                    input_opt_value_list = opt_value_list
            
            i = 0
            for input_opt_item in input_opt_list:
                selected = ""
                if input_value == str(i) :
                    selected = "selected"
                input_html += "<option value='" + input_opt_value_list[i] + "' " + selected + ">" + input_opt_item + "</option>"
                i += 1

            input_html += "</select>"
        elif (input_type == "checkbox" or input_type == "radio") and input_value == "1":
            input_html += "checked />"
        else:
            input_html += "/>"


        el.text = self.md.htmlStash.store(input_html)
        return el, m.start(0), m.end(0)


    
class MdInputs(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(InputsInlineProcessor(INPUTS_RE, md), 'inputs', 175)


def makeExtension(**kwargs):
    return MdInputs(**kwargs)
