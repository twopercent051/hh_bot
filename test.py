string = '<p><strong>Обязанности:</strong></p> <ul> <li>сборка товара по накладным (продукты питания)</li> <li>адресное хранение</li> <li>разгрузка, загрузка машин (газель)</li> </ul> <p><strong>Требования:</strong></p> <ul> <li>без опыта</li> </ul> <p><strong>Условия:</strong></p> <ul> <li>работа на складе продуктов питания</li> <li>пятидневка (Суббота, Воскресенье выходной), посменно, одна неделя с 8,00 до 18.00, вторая неделя с 10.00 до 19.00</li> <li>первый месяц оклад 43 000 руб, затем сдельная оплата (от 43 000 руб до 70000 руб)</li> <li>к месту работы и обратно ходит вахта от перекрёстка ул. Тюляева и ул. Сормовская. утром ( <em>1-я в 7,30; 2-я в 8,30; 3-я 9,30</em>)</li> </ul>'


def tag_corrector(string):
    result = string.replace('<strong>', '<b>').replace('</strong>', '</b>')
    result = result.replace('<p>', '\n').replace('</p>', '\n')
    result = result.replace('<ul>', '').replace('</ul>', '')
    result = result.replace('<li>', '—').replace('</li>', '')

    return result

new = tag_corrector(string)
print(new)