from Logic.run_case import RunTest
from Common.excel_pub import ExcelDeal
from Logic.log_print import LogPrint
from Logic.pressure_test_run import PressureTest


class ExecuteMain:
    @staticmethod
    def execute():
        test_case_file = ExcelDeal.read_excel()                         # 读取测试用例文件的路径信息

        for i in test_case_file:
            LogPrint().info("---------开始执行测试用例文件,路径是-----------:" + i)
            # 如果路径名称包括PressureTestCase,则该PressureTestCase.xlsx文件中只能包含压力测试的接口信息内容,压力测试需要另外处理,所以需要其他函数执行
            if 'PressureTestCase' in i:
                PressureTest().run_pressure_test(i)
            else:
                RunTest().run_interface_test(i)


if __name__ == '__main__':
    ExecuteMain.execute()
