#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import Response
import logging
import datetime
import uuid

import simplepos_dao

#logger
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
app = Flask(__name__)

@app.before_request
def before_request():
    logging.debug(request);


@app.route("/")
def index():
    productResult = simplepos_dao.selectProduct()
    saleResult = simplepos_dao.selectSale()
    saleTotalSum = 0;
    saleTotalEndSum = 0;
    saleTotalNotEndSum = 0;

    for item in saleResult :
        saleTotalSum += item.sale_price
        if item.end_yn == "N" :
            saleTotalNotEndSum += item.sale_price
        else :
            saleTotalEndSum += item.sale_price
    
    return render_template("index.html", productResult=productResult, saleResult=saleResult, saleTotalSum=saleTotalSum, saleTotalEndSum=saleTotalEndSum, saleTotalNotEndSum=saleTotalNotEndSum)


@app.route("/product/insert", methods=['POST'])
def productInsert():
    productName = request.form["productName"]
    productPrice = int(request.form["productPrice"])

    if productName == None or productPrice == None :
        return "Mandatory parameter is missing"

    simplepos_dao.insertProduct(productName, productPrice)
    return redirect(url_for("index"))


@app.route("/sale/insert", methods=['POST'])
def saleInsert():

    #logging.debug(request.form)
    tid = str(uuid.uuid4()).split('-')[0]
    for item in request.form.getlist('id'):
        productCode = request.form.get('code_'+item);
        saleQuantity = request.form.get('qty_'+item);
        salePrice = request.form.get('price_'+item);
        simplepos_dao.insertSale(tid, productCode, saleQuantity, salePrice)        

    return redirect(url_for("index"))

@app.route("/sale")
def saleSelect():
    result = simplepos_dao.selectSaleHisory()
    total = simplepos_dao.selectTotalSale()

    #initialize dictionary
    detailDictionary = {}
    for row in result:
        detail = simplepos_dao.selectSaleHisoryDetail(row['sale_code'])

        detailList = []
        for item in detail:
            #logging.debug(item['product_name'] + " " + str(item['sale_quantity']) + "개 " + str(item['sale_price']) + "원" )
            detailList.append(item['product_name'] + " " + str(item['sale_quantity']) + "개 " + str(locale.format('%.0f', item['sale_price'], 1)) + "원" )
        
        detailDictionary[row['sale_code']] = ', '.join(detailList)

    return render_template("sale.html", saleResult=result, totalResult=total, detailResult=detailDictionary)


@app.route("/approve", methods=['POST'])
def approve():
    simplepos_dao.updateSale()
    return redirect(url_for("index"))


@app.route("/init", methods=['GET'])
def initailDB():
    simplepos_dao.initailDB()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

'''
#Excel Export
@app.route("/excel/sale")
def excelSale():
    logging.debug("======= Excel Report =======")

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    currency_format = workbook.add_format({'num_format': '#,##0'})

    # Set the columns widths.
    worksheet.set_column('A:E', 15)
    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:B', 20)

    # Add a table to the worksheet.
    data = simplepos_dao.selectSaleHisoryForExcel()
    worksheet.add_table('A1:E'+str(len(data)+1), {'data': data,
                               'style': 'Table Style Light 11',
                               'columns': [{'header': 'No.'},
                                           {'header': '판매일자'},
                                           {'header': '상품명'},
                                           {'header': '판매수량'},
                                           {'header': '판매가격', 'format': currency_format},
                                           ]})

    workbook.close()

     # Rewind the buffer.
    output.seek(0)

    response = Response()
    response.status_code = 200
    response.data = output.read()

    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=sale_" + time.strftime("%Y%m%d") + ".xlsx"
    return response


@app.route("/upload/action", methods=['POST'])
def uploadAction():
    file = request.files['excelFile']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        logging.debug("[Upload File Name] : " + filename);
        file.save(os.path.join('C:/Documents and Settings/Administrator/Desktop/', filename))

        #excel read
        workbook = open_workbook('C:/Documents and Settings/Administrator/Desktop/' + filename)
        sheet = workbook.sheet_by_index(0)

        #excel full read
#       for row_index in range(sheet.nrows):
#           for col_index in range(sheet.ncols):
#               logging.debug(cellname(row_index,col_index))
#               logging.debug(sheet.cell(row_index,col_index).value)

        for row_index in range(sheet.nrows):
            if row_index != 0:
                logging.debug("productName : " + str(sheet.cell(row_index,0).value))
                logging.debug("productDesc : " + str(sheet.cell(row_index,1).value))
                logging.debug("productPrice : " + str(sheet.cell(row_index,2).value))
                logging.debug("stock : " + str(sheet.cell(row_index,3).value))
                productName = sheet.cell(row_index,0).value
                productDesc = sheet.cell(row_index,1).value
                productPrice = int(sheet.cell(row_index,2).value)
                stock = int(sheet.cell(row_index,3).value)
                simplepos_dao.insertProduct(productName, productDesc, productPrice, stock)
    else:
        logging.debug("=============NOT ALLOW FILE UPLOAD=============")
    return redirect(url_for("prodctSelect"))


ALLOWED_EXTENSIONS = set(['xlsx', 'xls'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.context_processor
def utility_processor():
    def format_price(amount):
        locale.setlocale(locale.LC_ALL, '')
        return locale.format('%.0f', amount, 1)
    return dict(format_price=format_price)
'''