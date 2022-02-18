# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from odoo.tools import date_utils 

class Relationfinder(http.Controller):
    @http.route('/relationfinder/', auth='public')
    def index(self, **kw):
        request.cr.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME ASC;")
        tableList = list(request.cr.fetchall())
        y = dict()
        errorList = []
        for table in tableList:
            tableName = str(table[0]).replace("_",".")
            try:
                x = dict(request.env[tableName].sudo().fields_get())
                y[table[0]] = x
            except:
                errorList.append(tableName)
        result = {"tables":y,"errorTables":errorList}
        result = json.dumps(result)
        tables = str(result) #skip this later
        return tables
    
    @http.route('/relations/', auth='public')
    def relats(self, **kw):
        mainKey = "relation"
        request.cr.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME ASC;")
        tableList = list(request.cr.fetchall())
        y = dict()
        errorList = []
        for table in tableList:
            tableName = str(table[0]).replace("_",".")
            try:
                x = dict(request.env[tableName].sudo().fields_get())
                relList = dict()
                for vers in x.keys():
                    if "relation" in x[vers].keys():
                        relList[vers] = x[vers]
                y[table[0]] = relList
            except:
                pass
            
        result = {"tables":y}
        result = json.dumps(result)
        tables = str(result) #skip this later
        return tables

    @http.route('/relationtable/', auth='public')
    def relattable(self, **kw):
        # menu_ids = request.env['ir.model.relation'].sudo().search([])
        # data = json.dumps(menu_ids.read(),default=date_utils.json_default)
        # data = dict(request.env['user.notify.rel'].sudo())
        # data = request.env['user.notify.rel'].sudo().search([])
        # data = json.dumps(data,default=date_utils.json_default)
        request.cr.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'user_notify_rel';")
        data = list(request.cr.fetchall())
        # request.cr.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'docket.notifii';")
        # data = list(request.cr.fetchall())
        return str(data)