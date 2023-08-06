import pandas as pd
import xlwings as xw
import json
import pygsheets
import tempfile

class formatData:

    def _google_creds_as_file():
        temp = tempfile.NamedTemporaryFile()
        temp.write(json.dumps({
            "type": "service_account",
            "project_id": "acoustic-mix-349604",
            "private_key_id": "dbf48593a3fbd764da425d82c88d30b8e995c38c",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxPQemL4fttjLY\nMF8F2sD3vdTlxoOS15MpqGPm09HHPkl10HoxRN2+bwiUFgELiZ2J7T4wVhtE/0X/\nAkpH5OOxP5FrvyJlKY7+YX29qV9BVUskFDL33qsmCheg3spghsRfPmv05d8uiLbP\nAPXyY/0c6mJIsv8qZiLleLhqnglpHe6qrRhPKBSt+ms4Mf6eDWMt+CgfLoa4AH1Z\nI9wIrGFj4Mc1WjiOAl4GZin+QT61pwMAVLn9Z9pG0owrpzGgFIM+X/GbwGBs0Lpa\nXetS5vJx9xfUyGtLSxcTAudnSTXRfJlNDWpOmnc3njNct4kg6pVjTgLjr2DHLaJ4\nBCsCrtcNAgMBAAECggEAHOUqxJS2L/KG2okUTNOLpzgrJ+TT2ZJMuztpQh4hcr68\nYjlBWpv0HNJkTyRBOlzOsshbXa0EGB0YD8mTS6JM3r5S2oKYPG7okZ9aTRv6XB/o\nNrMWViPWukZl8MOxscf25uI53nzFhIQkbZ4l+sUDZH3v1RNdl098e/XQ9wzZ0umZ\nDesvEYUVSsDQn3bh/jjv+NKIOHFxga83L4W6qLIYBf/oUPp2YWljT/E0a0fVKPHT\nWK5F5lg568Wng/9ERxT86OA5zFq0UOkPg1xSLKHgFfMsCQhqlEMCt8Ortk8uYgOI\nMIxsCa8Qlq/0+p1t7HTXwj+iQKRlIk6ux4aNnoGRHwKBgQDrOlpMR/hgFa2OpFPQ\nmhiB5os2azN8366SFfCL3CtAWVGhsBjteUGCNxJdBSaIpuVGIcEXpDOf/T6Np9wj\nfn2yYafDKxNTr7PPNBNB4uzlMEYsum8t90B/v/WGDWuGnLXTG7t3W6FGHu1fgmmE\nnASqWWUgs/7d2sg5+FZmkDd2PwKBgQDA476nKSt+NbPYLJzFJvnGcAmd/+TOCbVF\nojpE6hr4eY4lCDaibhfymY+Sc4WJuaChULshVVTa0a5Fd/NA3rj4kSum9Ow9clAf\nbptSedXIfuofgqjLve4gj3U8Nq7vFzZBQs7l5n/yrLz1kxwn9WhZ08lpgWOtYCan\nsCdcUNiXswKBgAEghHI9HgmH0Q8P5n7nXhqxOhWGqfZ9M97rT/27jlF+nA+EQnpQ\nzGmNTf84GRkqg4q0erJcTQsFMZmIJlvdLUj/gshCmpMaEmh5vWXhanUmqA9qzUGR\nH7P8/XYo9kzsz0o1pc5KmBk36Lc+brb98F/Ikd14P05cz/zHHdLb+ggNAoGBALTP\nh7L4U63ON1SHlTj17SNHeKxj6B3/Wa35gTeCX1/VyhoKlfQy0T33Fm9I3L+agulU\nXOXFMHKiJQM3io2febJ/mnS5mA2Nb2/XZb+tN2nnFh4Ng57g3iwlbdbQx7CViKUq\nM/mr1PotVD+686S9VWEGtwGwaThnLjT4Wh0eJ7ojAoGBAMQZ3dwiI4GBGe/D8Gde\nKlK5LXkNP8/APTSAc72mzzVRsmR1WEtUyof7V4F/fT14eNGueKBfq+lVqg4NIhHk\n4h4n/0/7V7r8EOSQ4l1MxPu0RYHxki0YIvAioXkqtcgHX1eugwSEtMCxoynM2JbP\njOu8KAS4vmoOm7MAjDDRDOBo\n-----END PRIVATE KEY-----\n",
            "client_email": "read-data@acoustic-mix-349604.iam.gserviceaccount.com",
            "client_id": "109453699538625719972",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/read-data%40acoustic-mix-349604.iam.gserviceaccount.com"
            }).encode('utf-8'))
        temp.flush()
        return temp


    def _refactordata(filepath,sheet):
        creds_file = formatData._google_creds_as_file()
        gc = pygsheets.authorize(service_account_file=creds_file.name)
        backtest_filepath=filepath

        wbk = xw.Book(backtest_filepath)
        ws = wbk.sheets[sheet]
        lst = []

        for i in range(0, 2):
            format_val=[]
            for j in range(0, 200):
                format_val.append(ws.cells(i,j).formula)
            
            lst.append(format_val)
            

        datadf = pd.DataFrame(lst)

        sh = gc.open('OHLC Data')
        wks = sh[0]
        wks.set_dataframe(datadf,(1,1))
