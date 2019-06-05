# coding=utf-8
import os

titles = '接口测试'


def title(title_content):
    head = '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>%s</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 引入 Bootstrap -->
    <link href="https://cdn.bootcss.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
    <!-- HTML5 Shim 和 Respond.js 用于让 IE8 支持 HTML5元素和媒体查询 -->
    <!-- 注意： 如果通过 file://  引入 Respond.js 文件，则该文件无法起效果 -->
    <!--[if lt IE 9]>
     <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
     <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
    <style type="text/css">
        .hidden-detail,
        .hidden-tr{display:none;}
    </style>
    </head>
    <body>''' % title_content
    return head


content = '''
<div  class='col-md-4 col-md-offset-4' style='margin-left:3%;'>
<h1>接口测试的结果</h1>'''


def test_result_data(start_time, end_time, pass_num, fail_num, exception_num, error_num):
    end_value = '''
    <table  class="table table-hover table-condensed">
    <tbody>
    <tr>
        <td><strong>开始时间:</strong> %s</td></tr>
        <td><strong>结束时间:</strong> %s</td></tr>
        <td><strong>耗时:</strong> %s</td></tr>
        <td><strong>结果:</strong>
            <span >Pass: <strong >%s</strong>
                Fail: <strong >%s</strong>
                Exception: <strong >%s</strong>
                Error_Case : <strong >%s
                </strong>
            </span>
        </td></tr>
    </tbody>
    </table>
    </div> ''' % (start_time, end_time, (end_time-start_time), pass_num, fail_num, exception_num, error_num)
    return end_value


case_content = '''
        <div class="row " style="margin:60px">
        <div style='    margin-top: 18%;' >
        <div class="btn-group" role="group" aria-label="...">
            <button type="button" id="check-all" class="btn btn-primary">所有用例</button>
            <button type="button" id="check-pass" class="btn btn-success">成功用例</button>
            <button type="button" id="check-fail" class="btn btn-danger">失败用例</button>
            <button type="button" id="check-error" class="btn btn-warning">错误用例</button>
            <button type="button" id="check-exception" class="btn btn-defult">异常用例</button>
        </div>
        <div class="btn-group" role="group" aria-label="...">
        </div>
        <table class="table table-hover table-condensed table-bordered" style="word-wrap:break-word;
        word-break:break-all; margin-top: 7px;">
        <tr>
            <td ><strong>用例ID&nbsp;</strong></td>
            <td><strong>用例名字</strong></td>
            <td><strong>key</strong></td>
            <td><strong>请求内容</strong></td>
            <td><strong>url</strong></td>
            <td><strong>请求方式</strong></td>
            <td><strong>预期</strong></td>
            <td><strong>实际返回</strong></td>
            <td><strong>结果</strong></td>
        </tr>
    '''


def test_result_colour(test_result):
    if test_result == 'pass':
        htl = '''<td bgcolor="green">pass</td>'''
    elif test_result == 'fail':
        htl = '''<td bgcolor="fail">fail</td>'''
    elif test_result == 'error':
        htl = '''<td bgcolor="red">error</td>'''
    else:
        htl = '<td bgcolor="crimson">exect</td>'
    return htl


def result_detail(identification, case_id, interface_name, key, request_data, url, request_method, assert_fail_reason,
                  json, test_result):
    detail = '''
        <tr class="case-tr %s">
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            %s
        </tr>
    ''' % (identification, case_id, interface_name, key, request_data, url, request_method, assert_fail_reason, json,
           test_result_colour(test_result))
    return detail


style_cut = '''
</div></div></table><script src="https://code.jquery.com/jquery.js"></script>
<script src="https://cdn.bootcss.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
<script type="text/javascript">
$("#check-fail").click(function(e){
    $(".case-tr").removeClass("hidden-tr");
    $(".pass").addClass("hidden-tr");
    $(".warning").addClass("hidden-tr");
    $(".error").addClass("hidden-tr");
});
$("#check-error").click(function(e){
     $(".case-tr").removeClass("hidden-tr");
    $(".pass").addClass("hidden-tr");
    $(".danger").addClass("hidden-tr");
    $(".error").addClass("hidden-tr");
});
$("#check-pass").click(function(e){
     $(".case-tr").removeClass("hidden-tr");
    $(".warning").addClass("hidden-tr");
    $(".danger").addClass("hidden-tr");
    $(".error").addClass("hidden-tr");
});
$("#check-exception").click(function(e){
     $(".case-tr").removeClass("hidden-tr");
    $(".warning").addClass("hidden-tr");
    $(".danger").addClass("hidden-tr");
    $(".pass").addClass("hidden-tr");
});
$("#check-all").click(function(e){
    $(".case-tr").removeClass("hidden-tr");
});
</script>
</body></html>'''


def result(title_content, start_time, end_time, pass_num, fail_num, case_id, interface_name, key, request_data, url,
           request_method, assert_fail_reason, json, test_result, exception_num, error_num):
    if type(interface_name) == list:
        relus = ' '
        for i in range(len(interface_name)):
            if test_result[i] == "pass":
                clazz = "pass"
            elif test_result[i] == "fail":
                clazz = "fail"
            elif test_result[i] == "exception":
                clazz = "exception"
            else:
                clazz = 'error'
            relus += (result_detail(clazz, case_id[i], interface_name[i], key[i], request_data[i], url[i],
                                    request_method[i], assert_fail_reason[i], json[i], test_result[i]))
        text = title(title_content)+content+test_result_data(start_time, end_time, pass_num, fail_num, exception_num,
                                                             error_num) + case_content + relus + style_cut
    else:
        text = title(title_content)+content+test_result_data(start_time, end_time, pass_num, fail_num, exception_num,
                                                             error_num)+case_content + \
               result_detail(case_id, interface_name, key, request_data, url, request_method, assert_fail_reason,
                             json, result, exception_num) + style_cut
    return text


def generate_html(file_path, title_content, start_time, end_time, pass_num, fail_num, case_id, interface_name, key,
                  request_data, url, request_method, assert_fail_reason, json, test_result, exception_num, error_num):
    texts = result(title_content, start_time, end_time, pass_num, fail_num, case_id, interface_name, key, request_data, url,
                   request_method, assert_fail_reason, json, test_result, exception_num, error_num)
    with open(file_path, 'wb') as f:
        f.write(texts.encode('utf-8'))

