email_template = """
</html>
    <head>
        <meta charset="utf-8">
        <title>Bharti-axa Alert</title>
        <style>
            .datapop tr td {
                padding: 8px 12px;
                border-right: 1px solid #efefef;
                color: #595959;
            }

            .datapop tr:nth-child(odd) {
                background: #f7f7f7;
            }

            .datapop tr:nth-child(even) {
                background: #EDEDED;
            }

            .datapop tr:hover {
                background: #fff;
            }
        </style>
    </head>

    <body>
        <table width="100%" border="0" cellspacing="0" cellpadding="0"
            style="background: #efefef; font-family: Helvetica, Arial, 'sans-serif'">
            <tbody>
                <tr>
                    <td align="center">
                        <table width="700" border="0" cellspacing="0" cellpadding="0"
                            style="margin:20px auto; background: #fff; border-radius: 6px;">
                            <tbody>
                                <tr>
                                    <td>
                                        <table width="100%" border="0" cellspacing="0" cellpadding="0"
                                            style="padding: 20px;">
                                            <tbody>
                                                <tr>
                                                    <td><img src="https://www.bhartiaxa.com/sites/default/files/2022-08/bharti-axa-logo.svg?w=256&q=75"
                                                        width="100" height="40" alt="" /></td>
                                                    <td align="right"><img
                                                            src="https://lumiq.ai/static/lumiq-f31913638eef8c454d268b6f70719ae8.webp"
                                                            width="100" height="50" alt="" /></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <table width="90%" border="0" cellspacing="0" cellpadding="0">
                                            <tr>
                                                <td height="1" style="background: #efefef;"></td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td align="center" style="font-size: 26px; color: red;"><img
                                            src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/150px-Amazon_Web_Services_Logo.svg.png">
                                    </td>
                                </tr>
                                <tr>
                                    <td>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <table width="90%" border="0" cellspacing="0" cellpadding="0">
                                            <tbody>
                                                <tr>
                                                    <td align="center" valign="middle" style="font-size: 22px;">
                                                        reportTitle</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td align="center" valign="middle">
                                        <h3>reportMessageHeader</h3>
                                    </td>
                                </tr>
                                <tr>
                                    <td>&nbsp;</td>
                                </tr>
                                TABLEBODY
                                <tr>
                                    <td height="40">&nbsp;</td>
                                </tr>
                                <tr>
                                    <td align="center" valign="top">&nbsp;</td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td align="center">&nbsp;</td>
                </tr>
                <tr>
                    <td align="center" style="font-size: 12px;">
                        This is an auto generated e-mail. Please do not reply.
                    </td>
                </tr>
            </tbody>
        </table>
    </body>

    </html>
"""


email_body = """<tr>
    <td align="center" valign="middle" style="padding-top: 15px;">
            <h3>Report_header_name</h3>
        </td>
    </tr>
    <tr>
        <td align="center">
            <table width="90%" border="1" cellspacing="0" cellpadding="0" class="datapop">
                <tbody>
                    <tr>
                        TABLEBODY
                    </tr>
                </tbody>
            </table>
        </td>
    </tr>
"""


col_name ="""
    <td width="30%" align="left" valign="middle" bgcolor="#464646" style="color: #fff; padding: 6px;">col_name</td>
"""
row_data = """
    <td width="30%" align="left" valign="middle" bgcolor="#fff" style="color: #464646; padding: 6px;">value_name</td>
"""