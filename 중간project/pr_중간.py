import re
import logging
from logging import info as print
from random import *
from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from operator import itemgetter
from copy import *
from tkinter import filedialog

logging.basicConfig(level=logging.DEBUG)

# 식당이름, 학교와의 거리, 평점순, 주문대기수, 배달료, 예상배달시간
restaurant = [["마포갈매기", 385],
              ["버거킹", 620],
              ["니뽕내뽕", 613],
              ["메차쿠차", 683],
              ["인생극장", 1600],
              ["스시오야붕", 1400],
              ["미소야", 1480],
              ["자금성", 1430],
              ["뜨끈이감자탕", 330]]
# 메뉴 데이터
menu = [[["마포갈매기150g", 9500], ["매콤갈매기150g", 9500], ["마포삼겹살150g", 9500], ["돼지껍딱150g", 8500]],
        [["몬스터와퍼세트", 10700], ["스태커4와퍼세트", 15900], ["기네스와퍼세트", 10700], ["콰트로치즈와퍼세트", 10100]],
        [["차뽕", 7500], ["태뽕", 7500], ["일뽕", 7500], ["크뽕", 8900]],
        [["해물야끼 우동", 8500], ["등심카츠 정식", 10800], ["코돈블루 돈까스 정식", 11500], ["메차쿠차 돈까스 정식", 12500]],
        [["양념쪽갈비", 13000], ["매운쪽갈비", 14000], ["최류탄 주먹밥", 5000], ["용궁라면", 5000]],
        [["연어초밥(12p)", 19000], ["참치초밥(12p)", 24000], ["활어초밥(12p)", 24000], ["소고기초밥(12p)", 18000]],
        [["로스카츠", 8500], ["히레카츠", 9500], ["고구마 치즈 돈카츠", 10000], ["매운철판돈카츠", 9500]],
        [["얼큰돼지짬뽕", 8000], ["치즈탕수육", 19000], ["해물수제비짜장", 7000], ["해물수제비짬뽕", 8000]],
        [["뼈해장국", 8000], ["한우맑은곰탕", 8000], ["왕갈비탕", 12000], ["한우사골순대국", 8000]]
        ]

# 콤보박스 데이터 삽입용 리스트
res = []
# 선택된 메뉴 문자열저장, 최종금액 저장, 최종선택 인덱스저장
result_string, result_charge, final_select = '', 0, 0
# 함수연계를 위해 bool 변수 선언
b_choose, b_add = False, False

# 콤보박스에 들어갈 데이터 삽입
for i in range(9):
    res.append(restaurant[i][0])


# 프로그램 종료
def stop(event=None):
    window.quit()


# 거리(50m/min) + 주문대기수(1대기:20분)를 고려한 배달시간
def delivery_time(a, b):
    return 20 + round((a / 50) + (b * 20))


# 평점, 주문대기수, 배달료, 배달시간 순으로 랜덤값 삽입
def rand_num(a):
    for i in range(9):
        a[i].append(randrange(1, 6))
        a[i].append(randrange(0, 4))
        a[i].append(round(randrange(1000, 3000), -2))
        a[i].append(delivery_time(a[i][1], a[i][3]))


# 우선순위를 통한 가게 추천
def priority(event=None):
    text_recommend.delete('1.0', END)
    if found_pri.get() == 'score':
        copy_restaurant.sort(key=itemgetter(2), reverse=True)
        text_recommend.delete('1.0', END)
        for i in range(9):
            if copy_restaurant[i][2] == 5:
                text_recommend.insert(END, str(i + 1) + '. ' + copy_restaurant[i][0] + ', ' + '평점: ' + '★' * copy_restaurant[i][2] + ' 강추!!!' + '\n')
            else:
                text_recommend.insert(END, str(i+1) + '. ' + copy_restaurant[i][0] + ', ' + '평점: ' + '★'*copy_restaurant[i][2] + '\n')
    elif found_pri.get() == 'time':
        copy_restaurant.sort(key=itemgetter(5))
        text_recommend.delete('1.0', END)
        for i in range(9):
            text_recommend.insert(END, str(i+1) + '. ' + copy_restaurant[i][0] + ', ' + '주문대기수: ' + str(copy_restaurant[i][3]) + ', ' + '예상배달시간: ' + str(copy_restaurant[i][5]) + '분' + '\n')
    elif found_pri.get() == 'charge':
        copy_restaurant.sort(key=itemgetter(4))
        text_recommend.delete('1.0', END)
        for i in range(9):
            text_recommend.insert(END, str(i+1) + '. ' + copy_restaurant[i][0] + ', ' + '배달료: ' + str(copy_restaurant[i][4]) + '원' + '\n')


# 메뉴 랜덤 추천기
def rand_recommend(event=None):
    text_recommend.delete('1.0', END)
    res_num = randrange(0, 9)
    menu_num = randrange(0, 4)
    text_recommend.insert(END, '가게명: ' + restaurant[res_num][0] + '\n' + '메뉴: ' + menu[res_num][menu_num][0] +
                          '(' + str(menu[res_num][menu_num][1]) + '원)' + '\n' + '배달료: ' + str(restaurant[res_num][4]) + '원')


# 사진 변경 및 가게 메뉴 출력
def out_menu(event=None):
    global image_map, image_info, res, final_select, b_choose, b_add
    b_choose = True
    text_charge.delete('1.0', END)
    if b_add == False:
        res = []
        for i in range(9):
            if restaurant[i][0] == pattern_var.get():
                final_select = i
                image_map = PhotoImage(file='식당위치/'+str(i+1) + ".png")
                image_info = PhotoImage(file='식당위치/'+str(i+1)*2 + ".png")
                label_map.configure(image=image_map)
                label_info.configure(image=image_info)
                for name, charge in menu[i]:
                    res.append(name)
                    text_charge.insert(END, '메뉴: ' + name + ', 가격: ' + str(charge) + '\n')
        combobox.configure(value=res)
        b_add = True
    else:
        text_charge.insert(END, 'ERROR: 메뉴선택중 가게변경은 불가합니다')


# 메뉴 추가
def add(event=None):
    global res, result_string, result_charge, final_select, b_choose
    text_charge.delete('1.0', END)
    if b_choose == True:
        result_string += pattern_var.get() + ', '
        for i in range(4):
            if pattern_var.get() == menu[final_select][i][0]:
                result_charge += menu[final_select][i][1]
        text_charge.insert(END, '-' + restaurant[final_select][0] + '-' +
                           '\n' + '선택중...' + '(' + result_string + ')')
    else:
        text_charge.insert(END, 'ERROR: 식당을 먼저 선택해 주세요!')


# 최종 메뉴 선택 및 금액 출력
def result(event=None):
    global res, result_string, result_charge, final_select, b_choose, b_add
    text_charge.delete('1.0', END)
    if b_choose == True:
        if b_add == True:
            text_charge.insert(END, '가게명: ' + restaurant[final_select][0] + '\n' + '주문내역: ' + result_string +
                               '\n' + '가격: ' + str(result_charge+restaurant[final_select][4]) +
                        '(배달료 포함), ' + '예상 배달시간: ' + str(restaurant[final_select][5]) + '분')
            res = []
            for i in range(9):
                res.append(restaurant[i][0])
            combobox.configure(value=res)
            result_string, result_charge, final_select = '', 0, 0
            b_choose, b_add = False, False
        else:
            text_charge.insert(END, 'ERROR: 메뉴를 먼저 선택해 주세요!')
    else:
        text_charge.insert(END, 'ERROR: 식당을 먼저 선택해 주세요!')


# 식당, 메뉴 초기화
def clear(event=None):
    global res, result_string, result_charge, final_select, b_choose, b_add
    text_charge.delete('1.0', END)
    text_charge.insert(END, '선택이 초기화 되었습니다. 가게를 다시 선택하세요')
    res = []
    for i in range(9):
        res.append(restaurant[i][0])
    combobox.configure(value=res)
    result_string, result_charge, final_select = '', 0, 0
    b_choose, b_add = False, False


window = Tk()
window.title("2017180037 전성희")
window.geometry("1280x720+200+100")
window.resizable(False, False)

# 레이블 이미지 선정
image_map = PhotoImage(file='식당위치/'+str(1)+".png")
image_info = PhotoImage(file='식당위치/'+str(1)*2+".png")
# 레스토랑 정보 입력
rand_num(restaurant)
copy_restaurant = deepcopy(restaurant)
# 프로그램 이름
label = Label(text='한국산업기술대 배달 맛집', font = ("HY견고딕", 15))
label.place(x=350, y=0)
# 프레임(추천 메뉴, 추천 결과, 메뉴 입력, 총 결제 금액, 지도, 가게사진)
frame_menu = LabelFrame(window, text='Priority', relief="solid")
frame_menu.place(x=0, y=30, width=440)

frame_recommend = LabelFrame(window, text='Lists', relief="solid")
frame_recommend.place(x=0, y=75, width=440)

frame_input = LabelFrame(window, text='Input', relief="solid")
frame_input.place(x=440, y=30, width=440)

frame_result = LabelFrame(window, text='Output', relief="solid")
frame_result.place(x=440, y=75, width=440)

frame_map = LabelFrame(window, text='MAP', relief="solid")
frame_map.place(x=0, y=220, width=880, height=500)

frame_info = LabelFrame(window, text='Info', relief="solid")
frame_info.place(x=880, y=0, width=400, height=720)
# 지도이미지
label_map = Label(frame_map, image=image_map)
label_map.pack()
# 식당사진
label_info = Label(frame_info, image=image_info)
label_info.pack()
# 우선순위버튼
found_pri = StringVar(value='score')
Radiobutton(frame_menu, text='평점순', value='score', variable=found_pri).pack(side=LEFT)
Radiobutton(frame_menu, text='배달시간순', value='time', variable=found_pri).pack(side=LEFT)
Radiobutton(frame_menu, text='배달료순', value='charge', variable=found_pri).pack(side=LEFT)
# 랜덤 추천
button_random = Button(frame_menu, width=14, text='랜덤추천', command=rand_recommend, takefocus=False)
button_random.pack(side=RIGHT)
# 우선순위결과
button_find = Button(frame_menu, width=14, text='Find', command=priority, takefocus=False)
button_find.pack(side=RIGHT)
# 입력창
pattern_var = StringVar(value='마포갈매기')
combobox = Combobox(frame_input, width=20, textvariable=pattern_var, height=4, values=res)
combobox.pack(side=LEFT, fill=X)
# 가게선택
button_choose = Button(frame_input, text='가게선택', command=out_menu, takefocus=False)
button_choose.pack(side=LEFT)
# 메뉴선택
button_add = Button(frame_input, text='메뉴선택', command=add, takefocus=False)
button_add.pack(side=LEFT)
# 결제금액
button_result = Button(frame_input, text='결제금액', command=result, takefocus=False)
button_result.pack(side=LEFT)
# 초기화
button_clear = Button(window, text='초기화', command=clear, takefocus=False)
button_clear.place(x=776, y=190)
# 계산결과창
text_charge = ScrolledText(frame_result, height=7, font=("Malgun Gothic", 10))
text_charge.pack(side=LEFT, fill=X)
# 메뉴추천창
text_recommend = ScrolledText(frame_recommend, height=7, font=("Malgun Gothic", 10))
text_recommend.pack(side=LEFT, fill=X)

menu_root = Menu()

menu_file = Menu(menu_root, tearoff=0)
menu_file.add_command(label='quit', command=stop)
menu_root.add_cascade(label='File', menu=menu_file)

window.config(menu=menu_root)
window.bind("<Escape>", stop)
window.mainloop()