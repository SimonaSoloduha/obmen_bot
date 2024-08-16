from datetime import datetime
from math import floor
from PIL import Image, ImageDraw, ImageFont


def get_text(rub_buy, rub_sell, uah_buy, uah_sell, usd_bay=41300, usd_sell=40800):
    """
    Просчет курса
    :param paragraph: курсы
    :return: str, текст
    """
    day = datetime.today().day
    rub_uah = floor(1000 / rub_buy * uah_sell * 0.935)
    rub_pln = floor(10000 / rub_buy * 3.8 * 0.935) / 10
    rub_eur = floor(10000 / rub_buy * 0.89 * 0.94) / 10
    rub_usd = floor(rub_uah * 10000 / usd_bay) / 10

    uah_rub = floor(100 / uah_buy * rub_sell * 0.945) * 10
    pln_rub = floor(2.12 * rub_sell * 0.94) * 100
    eur_rub = floor(10.30 * rub_sell * 0.94) * 100
    usd_rub = floor(usd_sell * uah_rub/100000) * 100

    text = (f"Выгодный курс на {day} авгута \n\nОТДАЕТЕ / ПОЛУЧАЕТЕ\n1000 руб = {rub_uah} грн\n1000 руб = {rub_pln} pln\n"
            f"1000 руб = {rub_eur} eur\n1000 руб = {rub_usd} usd\n\nОТДАЕТЕ / ПОЛУЧАЕТЕ\n1000 грн = "
            f"{'{0:,}'.format(uah_rub).replace(',', ' ')} руб\n"
            f"1000 pln = {'{0:,}'.format(pln_rub).replace(',', ' ')} "
            f"руб\n1000 eur = {'{0:,}'.format(eur_rub).replace(',', ' ')} "
            f"руб\n1000 usd = {'{0:,}'.format(usd_rub).replace(',', ' ')} руб\n")
    get_images(rub_uah, rub_pln, rub_eur, rub_usd, uah_rub, pln_rub, eur_rub, usd_rub)
    return text


def get_text_real(rub_buy, rub_sell, uah_buy, uah_sell):
    """
    Просчет курса
    :param paragraph: курсы
    :return: str, текст
    """
    day = datetime.today().day
    rub_uah = floor(1000 / rub_buy * uah_sell)
    uah_rub = floor(1000 / uah_buy * rub_sell)

    text = (f"Курс на {day} авгута \n\nОТДАЕТЕ  / ПОЛУЧАЕТЕ\n1000 руб = {rub_uah} грн\n\nОТДАЕТЕ / ПОЛУЧАЕТЕ\n1000 грн = "
            f"{'{0:,}'.format(uah_rub).replace(',', ' ')} руб\n"
            f"{rub_buy}"
            f"{rub_sell}"
            f"{uah_buy}"
            f"{uah_sell}")

    return text

def get_images(rub_uah, rub_pln, rub_eur, rub_usd, uah_rub, pln_rub, eur_rub, usd_rub):
    day = datetime.today().day
    img = Image.open('img/from_rub.PNG')
    image_1 = ImageDraw.Draw(img)

    font = ImageFont.truetype('img/font/Founder-Bold-BF64d30a7d4bf9b.otf', size=58)
    image_1.text(
        (410, 585),
        '{0:,}'.format(rub_uah).replace(',', ' '),
        font=font,
        fill='#1C0606')
    image_1.text(
        (390, 663),
        '{0:,}'.format(rub_pln).replace(',', ' '),
        font=font,
        fill='#1C0606')
    image_1.text(
        (420, 738),
        '{0:,}'.format(rub_eur).replace(',', ' '),
        font=font,
        fill='#1C0606')
    image_1.text(
        (400, 810),
        '{0:,}'.format(rub_usd).replace(',', ' '),
        font=font,
        fill='#1C0606')
    img.save(f"img/result/{day}_1.png")
    img = Image.open('img/to_rub.PNG')
    image_2 = ImageDraw.Draw(img)
    font = ImageFont.truetype('img/font/Founder-Bold-BF64d30a7d4bf9b.otf', size=48)

    image_2.text(
        (105, 585),
        '{0:,}'.format(usd_rub).replace(',', ' '),
        font=font,
        fill='#1C0606')
    image_2.text(
        (399, 585),
        '{0:,}'.format(eur_rub).replace(',', ' '),
        font=font,
        fill='#1C0606')
    image_2.text(
        (687, 585),
        '{0:,}'.format(pln_rub).replace(',', ' '),
        font=font,
        fill='#1C0606')
    image_2.text(
        (433, 775),
        '{0:,}'.format(uah_rub).replace(',', ' '),
        font=font,
        fill='#1C0606')
    img.save(f'img/result/{day}_2.png')


def get_images_path():
    day = datetime.today().day
    return [f'img/result/{day}_2.png', f'img/result/{day}_1.png']
