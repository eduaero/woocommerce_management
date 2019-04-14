from functions import signInWooVyD,downloadOneProduct

wcapi=signInWooVyD()
# 6834
# 6965

# OrderedDict([('id', 9), ('sonID', 7887), ('regular_price', '13.50'), ('prodID', '7886'), ('prodName', 'Camiseta bebé Te quiero mamá de la cabeza a los pies'), ('catID1', None), ('att_name0', None), ('att_option0', None), ('att_id0', None), ('regular_price_new', 11.5)])
#Contador: 9 Nombre: Camiseta bebé Te quiero mamá de la cabeza a los pies Producto: 7886   Antiguo Precio: 13.50 Nuevo Precio: 11.50
# {'code': 'woocommerce_rest_product_variation_invalid_id', 'message': 'ID no válido.', 'data': {'status': 400}}
# Id 14396

#Las variaciones están mal bajadas
downloadOneProduct(7887 ,wcapi,1)

downloadOneProduct(7886 ,wcapi,1)

downloadOneProduct(14396 ,wcapi,1)
