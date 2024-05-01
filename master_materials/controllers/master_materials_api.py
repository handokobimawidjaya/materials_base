# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
try:
    import simplejson as json
except ImportError:
    import json

def invalid_response(message):
    return {
        'status': 0,
        'message': message
    }

def valid_response(message, data):
    return {
        'status': 1,
        'message': message,
        'data': data 
    }

class MasterMaterialsApi(http.Controller):
    @http.route('/api/get_master_materials', methods=['GET'], type='http', auth='public')
    def get_master_materials(self, **params):
        type = params.get('type')
        code = params.get('code')
        name = params.get('name')
        
        filter = [('type','in',('fabric','jeans','cotton'))]
        if type:
            filter = [('type','=',type)]
        if code:
            filter.append(('code','=',code))
        if name:
            filter.append(('name','ilike',name))

        material_obj = request.env['master.materials'].sudo().search(filter)
        data = []
        for master in material_obj:
            data.append({
                'name': master.name,
                'code': master.code,
                'type': master.type,
                'price': master.price,
                'supplier_id': master.supplier_id.id,
                'supplier_code': master.supplier_id.default_code,
                'supplier_name': master.supplier_id.name
            })

        result = json.dumps({'status':1,'message':'success','data':data})
        return Response(result,content_type='application/json;charset=utf-8',status=200)
    
    @http.route('/api/create_master_materials', methods=['POST'], type='json', auth='public')
    def create_master_materials(self, **params):
        result = []
        for data in params.get('data'):
            mandatory_fields = ['type','code','name','price','supplier_code']
            fields = []
            for mandatory in mandatory_fields:
                if mandatory not in data.keys():
                    fields.append(mandatory)

            if len(fields) > 0:
                return invalid_response([{'error': 'Mandatory Request in Body %s!' %(fields), 'info': 'ERROR_TYPE_MANDATORY_PARAMS'}])

            type = data.get('type')
            code = data.get('code')
            name = data.get('name')
            price = data.get('price')
            supplier_code = data.get('supplier_code')
            
            supplier_obj = request.env['res.partner'].sudo().search([('default_code','=',supplier_code)])
            if not supplier_obj:
                return invalid_response([{'error': 'Supplier not Found', 'info': 'Pastikan Supplier telah terdaftar di Master Supplier.'}])

            duplicate_material_obj = request.env['master.materials'].sudo().search([('code','=',code)])
            if duplicate_material_obj:
                return invalid_response([{'error': 'Duplicate Transaction.', 'info': 'Transaksi Material dengan Code %s telah terbentuk' % (code)}])
                
            try:
                material_obj = request.env['master.materials'].sudo().create({
                    'name': name,
                    'code': code,
                    'type': type,
                    'price': price,
                    'supplier_id': supplier_obj.id
                })
                result.append({
                    'transaction_id': material_obj.id,
                    'code': material_obj.code,
                    'name': material_obj.name
                })
            except Exception as exc:
                return invalid_response([{
                    'error': 'Error When Create Master Materials',
                    'info': 'Error : %s' % (exc)
                }])

        return valid_response(
            message = 'Success When Create Materials',
            data = result
        )
        
    @http.route('/api/update_master_materials', methods=['POST'], type='json', auth='public')
    def update_master_materials(self, **params):
        transaction_code = params.get('transaction_code')
        if not transaction_code:
            return invalid_response([{
                'error': 'Mandatory Request in Body transaction_code!',
                'info': 'ERROR_TYPE_MANDATORY_PARAMS'
            }])
        
        supplier_obj = False
        supplier_code = params.get('supplier_code')
        if supplier_code:
            supplier_obj = request.env['res.partner'].sudo().search([('default_code','=',supplier_code)])
            if not supplier_obj:
                return invalid_response([{
                    'error': 'Supplier not Found',
                    'info': 'Pastikan Supplier telah terdaftar di Master Supplier.'
                }])

        vals = {}
        material_obj = request.env['master.materials'].sudo().search([('code','=',transaction_code)])
        if not material_obj:
            return invalid_response([{
                'error': 'Transaction Materials with Code %s not Found' % (transaction_code),
                'info': 'Pastikan Transaksi Materials telah dibuat.'
            }])

        if params.get('code'):
            vals.update({'code': params.get('code')})
        if params.get('name'):
            vals.update({'name': params.get('name')})
        if params.get('type'):
            vals.update({'type': params.get('type')})
        if params.get('price'):
            vals.update({'price': params.get('price')})
        if supplier_obj:
            vals.update({'supplier_id': supplier_obj.id})

        try:
            material_obj.sudo().write(vals)
            return valid_response(message='Success Update Transaction', data={'transaction_code': transaction_code})

        except Exception as exc:
            return invalid_response([{
                'error': 'Error When Update Master Materials',
                'info': 'Error : %s' % (exc)
            }])
        
    @http.route('/api/delete_master_materials', methods=['POST'], type='json', auth='public')
    def delete_master_materials(self, **params):
        transaction_code = params.get('transaction_code')
        if not transaction_code:
            return invalid_response([{
                'error': 'Mandatory Request in Body transaction_code!',
                'info': 'ERROR_TYPE_MANDATORY_PARAMS'
            }])
        
        material_obj = request.env['master.materials'].sudo().search([('code','=',transaction_code)])
        if not material_obj:
            return invalid_response([{
                'error': 'Transaction Materials with Code %s not Found' % (transaction_code),
                'info': 'Pastikan Transaksi Materials telah dibuat.'
            }])
        
        try:
            material_obj.sudo().unlink()
            return valid_response(message='Success Delete Transaction', data=[{'transaction_code': transaction_code}])
        except Exception as exc:
            return invalid_response([{
                'error': 'Error When Delete Master Materials',
                'info': 'Error : %s' % (exc)
            }])