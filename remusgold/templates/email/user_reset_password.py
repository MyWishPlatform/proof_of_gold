html_style='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Ducatus Second Mail</title>
    <style type="text/css">
      body {
        margin: 0;
        padding: 0;
        min-width: 100% !important;
        font-family: sans-serif;
      }
      img {
        height: auto;
      }
      .content {
        width: 100%;
        max-width: 1000px;
      }
      .content--footer {
        width: 100%;
      }
      .header {
        text-align: center;
        padding: 20px;
      }
      .footer {
        text-align: right;
      }
      .text--center {
        text-align: center;
      }
      .text {
        font-size: 20px;
        color: #404040;
        font-weight: 300;
      }
      .code {
        color: #1737a0;
        padding-top: 5px;
      }
      .padding {
        padding-left: 30px;
        padding-right: 30px;
      }
      .text-cont {
        padding-top: 20px;
      }
      .accent {
        padding: 10px 0 0px 0;
        font-size: 25px;
        font-weight: 400;
        color: #404040;
        text-transform: uppercase;
        text-align: center;
      }
      .dear {
        font-weight: 400;
        font-size: 20px;
        color: #404040;
      }
      .body-text {
        padding: 0px 15px 15px 15px;
        font-size: 15px;
        font-weight: 300;
        text-align: center;
        line-height: 18px;
      }
      table {
        border-collapse: separate;
      }
    </style>
  </head>'''
reset_body = """<body ducatus bgcolor="#ffffff">
      <tr>
        <td>
            <tr>
              <td style="padding-bottom: 50px">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="accent">
                      You registered, please follow link {reset_password_url}
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
        </td>
      </tr>
  </body>
</html>
"""
