def build_text_file(context, output_path):
    str_list = []

    str_0 = '<p>Products:</p>\n'
    str_list.append(str_0)
    str_1 = '<p>Products quantity: '
    str_list.append(str_1)
    str_2 = context['products']['quantity']
    str_list.append(str_2)
    str_3 = '</p>\n'
    str_list.append(str_3)
    str_4 = '<p>Maximum price: '
    str_list.append(str_4)
    str_5 = context['maximum_price']
    str_list.append(str_5)
    str_6 = '</p>\n'
    str_list.append(str_6)
    str_7 = '<ul>\n'
    str_list.append(str_7)
    for product in context['product_list']:
        str_8 = ' <li>'
        str_list.append(str_8)
        str_9 = product['name']
        str_list.append(str_9)
        str_10 = ': '
        str_list.append(str_10)
        str_11 = product['price']
        str_list.append(str_11)
        if product['price'] > context['maximum_price']:
            str_12 = ' <b> - ABOVE MAXIMUM PRICE</b>'
            str_list.append(str_12)
        str_13 = '</li>\n'
        str_list.append(str_13)
    str_14 = '\n'
    str_list.append(str_14)
    str_15 = '</ul>'
    str_list.append(str_15)

    output_file = open(output_path, 'w')
    for string in str_list:
        output_file.write(str(string))
