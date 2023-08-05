if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")
    from demo.demo_00 import demo

    demo()


import json
from copy import deepcopy
import re
import os
import html
from io import BytesIO
from PIL import Image
import base64
import datetime

try:
    from PyQt6.QtGui import QTextDocument

    pyqt6_installed = True
except Exception:
    pyqt6_installed = False


from q2report.q2printer.q2printer import Q2Printer, get_printer
from q2report.q2utils import num, Q2Heap

re_calc = re.compile(r"\{.*?\}")
re_q2image = re.compile(r"\{q2image\s*\(\s*.*?\s*\)\}")

engine_name = None

# TODO: before_print, after_print

def q2image(image, width=0, height=0):
    if os.path.isfile(image):
        image = base64.b64encode(open(image, "rb").read()).decode()
    im = Image.open(BytesIO(base64.b64decode(image)))
    return f"{image}:{width}:{height}:{im.width}:{im.height}:{im.format}"


image = q2image


def set_engine(engine2="PyQt6"):
    global engine
    engine = engine2


class mydata(dict):
    def __init__(self, q2report):
        super().__init__()
        self.rep = self.q2report = q2report

    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        if self.q2report.use_prevrowdata:
            data = self.q2report.prevrowdata
        else:
            data = self.q2report.data
        if key in data:
            return data[key]
        elif key in globals():
            return globals()[key]
        else:
            return ""


class Q2Report:
    def __init__(self):
        self.report_content = None
        # self.data_sources = {}
        self.printer = None
        self.params = {}
        self.prevrowdata = {}
        self.use_prevrowdata = False
        self.mydata = mydata(self)
        self.table_aggregators = {}
        self.table_group_aggregators = []
        self.outline_level = 0
        # self.data_section = []
        # self.current_data_set = -1

        self.data = {}  # current data
        self.data_sets = {}
        self.current_data_set_name = ""
        self.current_data_set_row_number = 0
        # self.current_data_set_lenght = 0
        self.heap = Q2Heap()
        self.d = D(self)

    def load(self, content):
        if os.path.isfile(content):
            self.report_content = json.load(open(content))
        else:
            self.report_content = json.loads(content)
        self.params = self.report_content["params"]
        # count datasources
        # for page in self.report_content.get("pages", []):
        #     for column in page.get("columns", []):
        #         for rows_section in column.get("rows", []):
        #             if rows_section["role"] == "table":
        #                 self.data_section.append(rows_section["data_source"])
        #                 print(rows_section["data_source"])

    def data_start(self):
        self.current_data_set_row_number = 0

    def data_step(self):
        self.current_data_set_row_number += 1

    def data_stop(self):
        self.current_data_set_name = ""

    def get_cell_height(self, cell_data):
        if pyqt6_installed:
            padding = cell_data["style"]["padding"].replace("cm", "").split(" ")
            while len(padding) < 4:
                padding += padding

            cm = num(96 / num(2.54))
            text_doc = QTextDocument()

            text_doc.setTextWidth((num(cell_data["width"]) - num(padding[1]) - num(padding[3])) * cm)

            style = cell_data["style"]
            style = "p {%s}" % ";".join([f"{x}:{style[x]}" for x in style])
            text_doc.setDefaultStyleSheet(style)
            text_doc.setHtml("<p>%s</p>" % cell_data["data"])
            # height = round(num(text_doc.size().height()) / cm, 2) + num(padding[0]) + num(padding[2])
            height = round(num(text_doc.size().height()) / cm, 2)
            return height
        else:
            return 0

    def formulator(self, formula):
        formula = formula[0][1:-1]
        if self.use_prevrowdata:
            data = self.prevrowdata
        else:
            data = self.data
        if formula in data:
            rez = str(data[formula])
        else:
            rez = self.evaluator(formula)
        return html.escape(rez)

    def evaluator(self, formula):
        try:
            rez = str(eval(formula, self.mydata))
        except BaseException:
            rez = f"Evaluating error: {formula}"
        return rez

    def format(self, cell):
        format = cell.get("format", "")
        if format == "D":
            try:
                cell["data"] = datetime.datetime.strptime(cell["data"], "%Y-%m-%d").strftime("%d.%m.%Y")
            except Exception:
                pass
        elif format.upper() == "F":
            cell["xlsx_data"] = num(cell["data"])
            cell["numFmtId"] = "165"
            cell["data"] = ("{:,.2f}".format(num(cell["data"]))).replace(",", " ")
        elif format.upper() == "N":
            cell["xlsx_data"] = num(cell["data"])
            cell["numFmtId"] = "164"

    def render_rows_section(self, rows_section, column_style, aggregator=None):
        if aggregator is None:
            self.use_prevrowdata = False
            self.data.update({x: self.table_aggregators[x]["v"] for x in self.table_aggregators})
            self.data.update(self.params)
        else:
            self.prevrowdata.update({x: aggregator[x]["v"] for x in aggregator})
            self.prevrowdata.update(self.params)
            self.use_prevrowdata = True

        rows_section_style = dict(column_style)
        rows_section_style.update(rows_section.get("style", {}))
        rows_section = deepcopy(rows_section)
        rows_section["style"] = rows_section_style
        for cell in rows_section["cells"]:
            cell_text = rows_section["cells"][cell].get("data")
            cell_style = dict(rows_section_style)
            cell_style.update(rows_section["cells"][cell].get("style", {}))
            rows_section["cells"][cell]["style"] = cell_style
            if cell_text:
                #  images
                cell_text, rows_section["cells"][cell]["images"] = self.extract_images(cell_text)
                #  text data
                rows_section["cells"][cell]["data"] = re_calc.sub(self.formulator, cell_text)
                self.format(rows_section["cells"][cell])

        self.printer.render_rows_section(rows_section, rows_section_style, self.outline_level)

    def extract_images(self, cell_data):
        images_list = []

        def extract_image(formula):
            image_data = self.formulator(formula).split(":")
            if len(image_data) == 6:
                images_list.append(
                    {
                        "image": image_data[0],
                        "width": num(image_data[1]),
                        "height": num(image_data[2]),
                        "pixel_width": num(image_data[3]),
                        "pixel_height": num(image_data[4]),
                    }
                )
            return ""

        cell_data = re_q2image.sub(extract_image, cell_data)
        return cell_data, images_list

    def run(self, output_file="temp/repo.html", output_type=None, data={}, open_output_file=True):
        if data:
            self.data_sets.update(data)
        self.printer: Q2Printer = get_printer(output_file, output_type)
        self.printer.q2report = self
        report_style = dict(self.report_content["style"])

        pages = self.report_content.get("pages", [])
        for index, page in enumerate(pages):
            self.printer.reset_page(
                **{x: page[x] for x in page if x.startswith("page_")}, last_page=(index == (len(pages) - 1))
            )

            page_style = dict(report_style)
            page_style.update(page.get("style", {}))

            for column in page.get("columns", []):
                column_style = dict(page_style)
                column_style.update(column.get("style", {}))
                self.printer.reset_columns(column["widths"])

                for rows_section in column.get("rows", []):
                    data_set = self.data_sets.get(rows_section["data_source"], [])
                    if rows_section["role"] == "table":
                        if not data_set:
                            continue
                        # table rows
                        self.current_data_set_name = rows_section["data_source"]
                        self.aggregators_reset(rows_section)
                        # self.current_data_set_lenght = 0
                        if hasattr(data_set, "len"):
                            self.data["_row_count"] = len(data_set)
                            # self.current_data_set_lenght = len(data_set)
                        self.render_table_header(rows_section, column_style)

                        # self.current_data_set += 1
                        self.data_start()
                        for data_row in data_set:
                            self.data["_row_number"] = self.current_data_set_row_number + 1
                            self.data.update(data_row)

                            self.render_table_groups(rows_section, column_style)
                            self.aggregators_calc()
                            self.outline_level += 1
                            self.render_rows_section(rows_section, column_style)
                            self.outline_level -= 1
                            self.prevrowdata.update(data_row)

                            self.data_step()
                        self.data_stop()

                        self.render_table_groups(rows_section, column_style, True)
                        self.render_table_footer(rows_section, column_style)
                    else:  # Free rows
                        self.render_rows_section(rows_section, column_style)

        self.printer.save()
        if open_output_file:
            self.printer.show()

    def render_table_header(self, rows_section, column_style):
        if rows_section.get("table_header"):
            self.render_rows_section(rows_section["table_header"], column_style)

    def render_table_groups(self, rows_section, column_style, end_of_table=False):
        reset_index = None
        for index, group_set in enumerate(rows_section["table_groups"]):
            agg = self.table_group_aggregators[index]
            group_value = []
            for group in agg["groupby_list"]:
                group_value.append(self.evaluator(group))
            if agg["groupby_values"] != group_value and agg["groupby_values"] != [] or end_of_table:
                reset_index = index
                break
        if reset_index is not None:
            for index in range(len(rows_section["table_groups"]) - 1, index - 1, -1):
                agg = self.table_group_aggregators[index]
                self.render_rows_section(
                    rows_section["table_groups"][index]["group_footer"],
                    column_style,
                    aggregator=agg["aggr"],
                )
                self.outline_level -= 1
                # clear group aggregator
                agg["groupby_values"] = []
                for cell in agg["aggr"]:
                    agg["aggr"][cell]["v"] = num(0)
                agg["aggr"]["_row_number"]["v"] = num(0)
        if end_of_table:
            return
        for index, group_set in enumerate(rows_section["table_groups"]):
            agg = self.table_group_aggregators[index]
            group_value = []
            for group in agg["groupby_list"]:
                group_value.append(self.evaluator(group))
            if agg["groupby_values"] != group_value:
                self.outline_level += 1
                self.render_rows_section(group_set["group_header"], column_style)

    def render_table_footer(self, rows_section, column_style):
        if rows_section.get("table_footer"):
            self.render_rows_section(rows_section["table_footer"], column_style)

    def aggregators_detect(self, rows_section, aggregator):
        if not rows_section:
            return
        formulas = []
        for cell_data in rows_section.get("cells").items():
            cell_data = cell_data[1].get("data", "")
            for x in re_calc.findall(cell_data):
                f = x[1:-1]
                if f not in formulas:
                    formulas.append(f)
        for cell_data in formulas:
            for mode in ["sum"]:
                if cell_data.lower().startswith(f"{mode}:"):
                    aggregator[cell_data] = {
                        "a": mode,  # aggregate function - sum, avg and etc
                        "f": cell_data[1 + len(mode) :],  # cell formula  # noqa: E203
                        "v": num(0),  # initial value
                    }

        aggregator["_row_number"] = {
            "a": "sum",  # aggregate function - sum, avg and etc
            "f": "",  # cell formula
            "v": num(0),  # initial value
        }

    def aggregators_reset(self, rows_section):
        self.table_aggregators = {}
        self.table_group_aggregators = []
        self.aggregators_detect(rows_section.get("table_footer", {}), self.table_aggregators)
        grouper = []
        for group in rows_section["table_groups"]:
            grouper.append(group["group_footer"]["groupby"])
            aggr = {
                "groupby_list": grouper[:],
                "groupby_values": [],
                "aggr": {},
            }
            self.aggregators_detect(group.get("group_footer", {}), aggr["aggr"])
            self.table_group_aggregators.append(aggr)

    def aggregators_calc(self):
        for y, x in self.table_aggregators.items():
            x["v"] += num(self.evaluator(x["f"]))

        for x in self.table_group_aggregators:
            x["groupby_values"] = []
            for y in x["groupby_list"]:
                x["groupby_values"].append(self.evaluator(y))
            for cell in x["aggr"]:
                x["aggr"][cell]["v"] += num(self.evaluator(x["aggr"][cell]["f"]))
            x["aggr"]["_row_number"]["v"] += 1


class D:
    class R:
        def __init__(self, data_set, row_number=0):
            self.data_set = data_set
            self.row_number = row_number

        def __getattr__(self, atr):
            if atr in self.__dict__:
                return self.__dict__[atr]
            elif atr == "r":
                return self.getrow
            elif self.row_number < len(self.data_set) and atr in self.data_set[self.row_number]:
                return self.data_set[self.row_number][atr]
            return ""

        def getrow(self, row_number):
            if row_number >= 0 and row_number < len(self.data_set):
                self.row_number = row_number
            else:
                self.row_number = 0
            return self

    def __init__(self, q2report):
        self.q2report: Q2Report = q2report

    def __getattr__(self, atr):
        if atr in self.q2report.data_sets:
            return self.R(self.q2report.data_sets[atr])
        return None
