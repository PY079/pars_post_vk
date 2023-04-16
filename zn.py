# -*- coding: utf-8 -*-
import vk_api, os, requests, sqlite3, time, telebot
from telebot.types import InputMediaPhoto
from data_project import vk_token_ra, id_gossip_nf, id_gossip_nf_clone, tg_token_bot, id_tg_group

def send_med_gr(sp_tg,cop,text_tg,id_post):
    media = []

    if len(sp_tg) >1:
        text_tg+= f"<a href='{cop}'>Оригинальный пост</a>\n<a href='https://vk.com/wall{id_gossip_nf_clone}_{id_post}'>Скопированный пост</a>\n\n<a href='https://vk.com/gossipnfclone'>Gossip NF CLONE</a>\n<a href='https://vk.com/gossipnf'>Gossip NF</a>"
        for i in range(len(sp_tg)): 
            if i == 0:
                media.append(InputMediaPhoto(sp_tg[i], text_tg, parse_mode='HTML'))
            else:
                media.append(InputMediaPhoto(sp_tg[i]))
        bot.send_media_group(id_tg_group, media)
    if len(sp_tg) <= 1:
        text_tg+= f"<a href='{cop}'>Оригинальный пост</a>\n<a href='https://vk.com/wall{id_gossip_nf_clone}_{id_post}'>Скопированный пост</a>\n\n<a href='https://vk.com/gossipnfclone'>Gossip NF CLONE</a>\n<a href='https://vk.com/gossipnf'>Gossip NF</a>"
        bot.send_photo(id_tg_group, sp_tg[0], text_tg, parse_mode='HTML')

def con(): # Создаём подключени
    os.system('cls')
    global vk, bot
    session = vk_api.VkApi(token=vk_token_ra)
    vk = session.get_api()
    bot = telebot.TeleBot(tg_token_bot)

def upd_db():
    global asd
    wal = vk.wall.get(owner_id = id_gossip_nf, count = 1,offset = 0, filter = 'all')

    id_lat = wal['count']
    id_ew = id_lat+1

    pk = 'C:/Users/User/Desktop/tg_bot_mus/gho.db'
    s= '/home/gygcywdvevev/pa/gho.db'

    connect = sqlite3.connect(pk)
    cursor = connect.cursor()
    ew = cursor.execute("SELECT `new_id` FROM `name` ").fetchone()
    connect.commit()

    count_post_bd = ew[0]




    if count_post_bd <= id_lat:
        asd = id_lat - ew[0]


        print(f'\n\n{asd}\n\n\n')
        if asd >= 0:
            cursor.execute(f"UPDATE `name` SET `new_id`={ew[0]+1}")
            print(f'В таблице: {ew[0]+1}')
            connect.commit()
            wall_get()
        else:
            cursor.execute(f"UPDATE `name` SET `new_id`={ew[0]+1}")
            connect.commit()

    if count_post_bd > id_ew:
        new_id = count_post_bd-id_ew
        cursor.execute(f"UPDATE `name` SET `new_id`={count_post_bd - new_id}")
        print(f'В БД -- {count_post_bd} поменял на -- {count_post_bd - new_id}')
        connect.commit()

    


def wall_get():
    audio=False
    poll = False
    album=False
    doc=False
    youla=False
    sp_vk = []
    sp_tg = []
    text_tg = '#real_post\n\n'
    wal = vk.wall.get(owner_id = id_gossip_nf, count = 1, filter = 'all')


    if 'is_pinned' in wal['items'][0]:
        ots=1+asd
        #ots = 1
        wa = requests.post('https://api.vk.com/method/wall.get',data={'access_token':vk_token_ra,'owner_id':id_gossip_nf, 'offset':ots,'count':'1','filter':'all','v':'5.131'}).json()
        # wa = requests.post('https://api.vk.com/method/wall.get',data={'access_token':vk_token_ra,'owner_id':-87249056, 'offset':1,'count':'1','filter':'all','v':'5.131'}).json()
        print('Пост в закрепе')
        if wa['response']['items'][0]['comments']['can_post'] == 0:
            attachments = False ;text_in_post =  False; block_comments = True
            print('Без коментариев - не отправляется')
        else: block_comments = False
    else:
        print('Пост не в закрепе')
        ots=0+asd
        # wa = requests.post('https://api.vk.com/method/wall.get',data={'access_token':vk_token_ra,'owner_id':-103364707, 'offset':2, 'count':'1','filter':'all','v':'5.131'}).json()
        wa = requests.post('https://api.vk.com/method/wall.get',data={'access_token':vk_token_ra,'owner_id':id_gossip_nf, 'offset':ots,'count':'1','filter':'all','v':'5.131'}).json()
        if wa['response']['items'][0]['comments']['can_post'] == 0:
            block_comments = True
            print('Без коментариев - не отправляется')
        else:  block_comments = False



    if wa['response']['items'][0]['marked_as_ads'] == 1:
        marked_as_ads = True
        print('Реклама в сообществе - не отправляется')
    else: marked_as_ads = False

    if 'copy_history' in wa['response']['items'][0]:
        copy_history = True
        print('Репост - не отправляется')
    else: copy_history = False

    # слова, по которым код определяет: рекламный пост или нет, можно добовлять слова
    if 'text' in wa['response']['items'][0]:
        mes_text2 = wa['response']['items'][0]['text'] # Текст сообщения
        lower_text = mes_text2.lower()
        block_list=['тогда тебе','записывайтесь','ждём вас','ждем вас','перейдите по ссылке','наш адрес', 'требуются','записывайся','записывайся по номеру','переходите по ссылке','предложение ограниченно','цены вырастут','заходите в сообщество','многое другое в паблике','самые низкие цены','низкие цены','переходи по ссылки в комментариях','все подробности в паблике','подробная информация в группе','качественно','недорого','качественно и не дорого','пишите и звоните',' подписывайся на канал',' подписывайся']
        post_ads = any(ad in lower_text for ad in block_list)
    
    cop = f"https://vk.com/wall{wa['response']['items'][0]['owner_id']}_{wa['response']['items'][0]['id']}"
    
    if 'text' in wa['response']['items'][0] and not 'В посте найдено голосование' in text_tg:
        mes_text = wa['response']['items'][0]['text'] # Текст сообщения
        
        if len(mes_text)>3966:
            text_tg+= 'Bad Request: message is too long. Max 4096\n\n-------------\n'
        else:
            text_tg+= f'{mes_text}\n'
        text_in_post = True
    
    elif 'text' in wa['response']['items'][0] and 'В посте найдено голосование' in text_tg:
        answ =[]
        mes_text = wa['response']['items'][0]['text'] # Текст сообщения
        
        if len(mes_text)>3966:
            text_tg+= 'Bad Request: message is too long. Max 4096\n\n-------------\n'
        else:
        
            for i2 in wa['response']['items'][0]['attachments'][0]['poll']['answers']:
                answ.append(i2['text'])
            text_tg+= f"Тема: {wa['response']['items'][0]['attachments'][0]['poll']['question']}\nВарианты:  {', '.join(answ)}\n\n-------------\n"

        text_in_post = True
    else: text_in_post = False
    

    if copy_history == False and marked_as_ads == False and block_comments == False and post_ads == False:
        if 'attachments' in wa['response']['items'][0]:
            for i in wa['response']['items'][0]['attachments']:
                _type = i['type']
                
                if _type == 'photo' or _type =='video':
                    sp_vk.append(f"{_type}{i[_type]['owner_id']}_{i[_type]['id']}_{i[_type]['access_key']}")
                    if _type == 'photo':
                        sp_tg.append(f"https://vk.com/{_type}{i[_type]['owner_id']}_{i[_type]['id']}")
                    if _type == 'video':
                        sp_tg.append('https://vk.com/photo-214698143_457239023')

                elif _type == 'poll':   
                    poll = True  
                    sp_vk.append(f"poll{i['poll']['owner_id']}_{i['poll']['embed_hash']}")
                    text_tg+= f"В посте найдено голосование\n"


                elif _type == 'audio':
                    audio=True
                    tg_url1=f"https://vk.com/audio{i['audio']['owner_id']}_{i['audio']['id']}";art1 = f"{i['audio']['artist']}";titl1 = f"{i['audio']['title']}"
                    sp_vk.append(f"audio{i['audio']['owner_id']}_{i['audio']['id']}_{i[_type]['track_code']}")
                    text_tg+= f"<a href='{tg_url1}'>{art1} - {titl1}</a>\n"

                elif _type == 'album':
                    album = True
                    print(12)
                    sp_vk.append(f"{_type}{i[_type]['owner_id']}_{i[_type]['id']}")
                    text_tg+= f"\nАльбом -->  <a href='https://vk.com/{_type}{i[_type]['owner_id']}_{i[_type]['id']}'>{i[_type]['title']}</a>\n"            
                    print(sp_vk)

                elif _type == 'doc':
                    doc=True
                    sp_vk.append(i[_type]['url'].replace('https://vk.com/','').replace('?hash=','_').split('&')[0])
                    text_tg+=f"\nДокумент -->  <a href ='{i[_type]['url'].split('?')[0]}'>{i[_type]['title']}</a>\n"
                
                elif _type == 'link' and wa['response']['items'][0]['attachments'][0][_type]['caption'] == 'youla.ru':
                    youla=True
                    sp_vk.append(wa['response']['items'][0]['attachments'][0][_type]['url'])
                    text_tg+= f"Объявление --> <a href ='{i[_type]['url']}'>{i[_type]['title']}</a>\n"
                
                elif _type == 'link' and wa['response']['items'][0]['attachments'][0][_type]['description'] == 'Плейлист':
                    audio = True
                    url0 = wa['response']['items'][0]['attachments'][0][_type]['url'].replace('access_hash=','').replace('https://m.vk.com/audio?act=','').split('&')
                    t = wa['response']['items'][0]['attachments'][0][_type]['url']
                    
                    sp_vk.append(f'{url0[0]}_{url0[1]}')
                    text_tg+= f"Плейлист --> <a href='{t}'>{wa['response']['items'][0]['attachments'][0][_type]['title']}</a>\n"


                

        text_tg+='-------------\n'
        if 'geo' in wa['response']['items'][0]['attachments']:
            hyt=wa['response']['items'][0]['geo']['coordinates'].split(' ')
            la=hyt[0]; lo=hyt[1]; geo=True
        else: geo=False

        

        if 'signer_id' in wa['response']['items'][0]:
            p = wa['response']['items'][0]['signer_id'] # Подпись
            ##########################
            ar = vk.users.get(user_ids = p, name_case = 'gen')
            a1 = ar[0]
            if 'first_name' in a1:first_name = a1['first_name']
            else: first_name = None

            if 'last_name' in a1:last_name = a1['last_name']
            else: last_name = None

            text_tg+= f"\nОт <a href ='https://vk.com/id{p}'>{first_name} {last_name}</a>\n"
            print(f'{first_name} {last_name}')
            ##########################

            signer_id = True

        else: signer_id = False
        



        if len(sp_vk)>0 and text_in_post == True and signer_id == True:
            if geo == False:
                id = vk.wall.post(owner_id = id_gossip_nf_clone, message=(f'{mes_text}\n\n--------------------\nОт: [id{p}|{first_name} {last_name}]'),attachments=sp_vk,  signed=0, copyright=cop)
                if audio == False and poll == False and album == False and doc == False and youla == False:
                    send_med_gr(sp_tg,cop,text_tg,id['post_id'])  
                else:
                    text_tg+= f"<a href='{cop}'>Оригинальный пост</a>\n<a href='https://vk.com/wall{id_gossip_nf_clone}_{id['post_id']}'>Скопированный пост</a>\n\n<a href='https://vk.com/gossipnfclone'>Gossip NF CLONE</a>\n<a href='https://vk.com/gossipnf'>Gossip NF</a>"
                    bot.send_message(id_tg_group,text_tg, parse_mode='HTML',disable_web_page_preview = True)
                print('пост 1')
            
            if geo == True:
                vk.wall.post(owner_id = id_gossip_nf_clone, message=(f'{mes_text}\n\n--------------------\nОт: [id{p}|{first_name} {last_name}]'),attachments=sp_vk,  signed=0, copyright=cop, lat=la, long=lo)
                print('пост 1')


        if len(sp_vk)<1 and text_in_post == True and signer_id == True:
            if geo == False:
                id = vk.wall.post(owner_id = id_gossip_nf_clone, message=(f'{mes_text}\n\n--------------------\nОт: [id{p}|{first_name} {last_name}]'),  signed=0, copyright=cop)
                text_tg+= f"<a href='{cop}'>Оригинальный пост</a>\n<a href='https://vk.com/wall{id_gossip_nf_clone}_{id['post_id']}'>Скопированный пост</a>\n\n<a href='https://vk.com/gossipnfclone'>Gossip NF CLONE</a>\n<a href='https://vk.com/gossipnf'>Gossip NF</a>"
                bot.send_message(id_tg_group,text_tg, parse_mode='HTML',disable_web_page_preview = True)
                print('пост 2')
            
            if geo == True:
                vk.wall.post(owner_id = id_gossip_nf_clone, message=(f'{mes_text}\n\n--------------------\nОт: [id{p}|{first_name} {last_name}]'),  signed=0, copyright=cop, lat=la, long=lo)
                print('пост 2')
        

        if len(sp_vk)>0 and text_in_post == True and signer_id == False:
            if geo == False:
                id = vk.wall.post(owner_id = id_gossip_nf_clone, message=mes_text,attachments=sp_vk,  signed=0, copyright=cop)
                
                if audio == False and poll == False and album == False and doc == False: send_med_gr(sp_tg,cop,text_tg,id['post_id'])    
                
                else: 
                    text_tg+= f"<a href='{cop}'>Оригинальный пост</a>\n<a href='https://vk.com/wall{id_gossip_nf_clone}_{id['post_id']}'>Скопированный пост</a>\n\n<a href='https://vk.com/gossipnfclone'>Gossip NF CLONE</a>\n<a href='https://vk.com/gossipnf'>Gossip NF</a>"
                    bot.send_message(id_tg_group,text_tg, parse_mode='HTML',disable_web_page_preview = True)
                
                print('пост 3')
            
            if geo == True:
                vk.wall.post(owner_id = id_gossip_nf_clone, message=mes_text,attachments=sp_vk,  signed=0, copyright=cop, lat=la, long=lo)
                print('пост 3')

        if len(sp_vk)>0 and text_in_post == False and signer_id == False:
            if geo == False:
                id = vk.wall.post(owner_id = id_gossip_nf_clone, attachments=sp_vk,  signed=0, copyright=cop)
                send_med_gr(sp_tg,cop,text_tg,id['post_id'])  
                print('пост 4')
            
            if geo == True:
                vk.wall.post(owner_id = id_gossip_nf_clone, attachments=sp_vk,  signed=0, copyright=cop, lat=la, long=lo)
                print('пост 4')

        if len(sp_vk)<1 and text_in_post == True and signer_id == False:
            if geo == False:

                id = vk.wall.post(owner_id = id_gossip_nf_clone, message=mes_text,  signed=0, copyright=cop)

                text_tg+= f"<a href='{cop}'>Оригинальный пост</a>\n<a href='https://vk.com/wall-219505503_{id['post_id']}'>Скопированный пост</a>\n\n<a href='https://vk.com/gossipnfclone'>Gossip NF CLONE</a>\n<a href='https://vk.com/gossipnf'>Gossip NF</a>"
                bot.send_message(id_tg_group,text_tg, parse_mode='HTML',disable_web_page_preview = True)
                print('пост 5')
                
                
            if geo == True:
                vk.wall.post(owner_id = id_gossip_nf_clone, message=mes_text,  signed=0, copyright=cop, lat=la, long=lo)
                print('пост 5')



def tg():
    con()
    while True:
        upd_db()
        time.sleep(60)

tg()
# con()
# print(upd_db())
#wall_get()