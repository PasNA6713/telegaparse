from telegraph import Telegraph

telegraph = Telegraph()
telegraph.create_account(short_name='1337')

def create_post(lot_info: dict) -> str:

    try:
        picture = lot["pictures"][0]
    except Exception as e:
        picture = ""

    response = telegraph.create_page(
        f"Цена - {lot['cost']['current']}, {lot['description']['title']}",
        html_content=f'<img src="{picture}" alt="Изображение товара отсутсвует">'+
        f"<p><strong>Место осмотра {lot['region']}</strong></p>"+
        f"<p><strong>{lot['bidding_type']}</strong></p>" +
        f"<p>{lot['description']['full']}</p>" +
        f"<blockquote>Дата проведения торгов: {lot['date']['bidding']}</blockquote>" +
        f"<blockquote>Дата начала представления заявок на участие: {lot['date']['start_bid']}</blockquote>" +
        f"<blockquote>Дата окончания представления заявок на участие: {lot['date']['end_bid']}</blockquote>" +
        f"<blockquote>Начальная цена, руб.: {lot['cost']['current']}</blockquote>" +
        f"<blockquote>Шаг цены: {lot['cost']['step']}</blockquote>" +
        '<p><strong>По всем вопросам </strong><a href="https://t.me/WalletBurnbot" target="_blank"><strong>@WalletBurn</strong></a></p>' +
        '<p><strong>Подписаться на канал </strong><a href="https://t.me/WalletBurnbot" target="_blank"><strong>@WalletBurn</strong></a></p>'
        
    )
    return('https://telegra.ph/{}'.format(response['path']))