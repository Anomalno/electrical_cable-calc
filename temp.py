type_iz='ПВХ'          #Тип изоляции
I_nagr=50              #Ток нагрузки
U_nom=380              #Номинальное напряжение
U_nach=400             #Начальное напряжение
Mat_jil='Медь'         #Материал жилы
Sp_pr='Воздух'         #Способ прокладки
temp=12                #Расчетная температура среды
Cpl=2                  #Кол-во ранее проложенных параллельных ЛЭП
L_cpl=100              #Расстояние между паралл. ЛЭП
cosf=0.83              #Коэф.мощности
l=830                  #Длина линии
x0=0.06                #Реактивное сопр.линии
import time
#Считаем максимальное падение напряжения:
deltaUmax=U_nach-U_nom*0.9
#Задаем индексы для материала жилы и способа прокладки
if Mat_jil=='Медь':
    y=53
else:
    y=31.7            
if Sp_pr=='Воздух':
    Sp_pr=1
if Sp_pr=='Земля':
    Sp_pr=2
if Mat_jil=='Медь':
    Mat_jil=1
if Mat_jil=='Алюминий':
    Mat_jil=2 
#Округляем температуру до большего значения,кратного 5
import math
print(math.ceil(temp/5)*5)
#Задаем списки для расчета коэффициентов
Spr_temp=[[-5,1.29,1.18],[0,1.24,1.14],[5,1.2,1.1],[10,1.15,1.05],[15,1.11,1],[20,1.05,0.95],[25,1,0.89],[30,0.94,0.84],[35,0.88,0.77],[40,0.81,0.71],[45,0.74,0.63],[50,0.67,0.55]]
Spr_kab=[[100,1,0.9,0.85,0.8,0.78,0.75],[200,1,0.92,0.87,0.84,0.82,0.81],[300,1,0.93,0.9,0.87,0.86,0.85]]
#Функция расчета температурного коэффициента:
def temp_k():
    global k1
    for i in range(0,len(Spr_temp)):
        if Spr_temp[i][0]>=(math.ceil(temp/5)*5):
            k1=Spr_temp[i][Sp_pr]
            print('k1=',k1)
            return k1
#Функция расчета коэффициента по параллельным кабелям:
def kab_k(n,a):
    global k2
    for i in range(0,len(Spr_kab)):
        if Spr_kab[i][0]==a:
            k2=Spr_kab[i][Cpl+n]
            print('k2=',k2)
            return k2
#Таблица для выбора сечения [материал][способ прокладки][ток]
Spr_tok=[[0],
             [[0],
              [33.5,42.8,58.6,78.1,104.2,127.4,155.3,196.2,242.7,280.9,321.8,369.2,439.0,504.1,588.7],
              [43.7,54.9,73.5,94.9,123.7,146.9,173.9,214.8,259.5,294.8,332.9,376.7,438.0,495.7,568.2]],
             [[0],
              [27.0,34.4,46.5,62.3,80.9,98.6,117.2,149.7,183.2,213.0,242.7,280.9,333.9,394.3,465.9],
              [34.4,40.9,54.9,71.6,94.9,114.4,133.0,165.5,199.0,226.9,254.8,290.2,337.6,387.8,448.3]]]
#Список сечений
S=[4,6,10,16,25,35,50,70,95,120,150,185,240,300,400]
#Функция нахождения сечения
def Sechenie():
    global Sk,k1,k2,I_nagr,S_index,b
    for i in range(0,len(S)):
        Tok=I_nagr/(k1*k2*b)
        if Tok<=Spr_tok[Mat_jil][Sp_pr][i]:
            Sk=S[i]
            S_index=i
            print('Iрассч одной линии=',Tok)
            print('Площадь сечения 1-й линии=',Sk)
            return Sk
        if Tok>Spr_tok[Mat_jil][Sp_pr][len(S)-1] and (b+Cpl<6):
            b=b+1
            i=0
            print('b1',b)
            
#Функция нахождения падения напряжения       
def U():
    global deltaU
    r0=1000/(y*Sk)
    print('r0=',r0)
    sinf=math.pow(1-math.pow(cosf,2),1/2)
    print('sinf=',sinf)
    deltaU=math.pow(3,1/2)*(I_nagr/b)*(r0*cosf+x0*sinf)*l/1000
    print('deltaU одной линии=',deltaU)
    print('deltaUmax=',deltaUmax)
    return deltaU
    
#НАЧАЛО ПРОГРАММЫ
temp_k()
for a in range(L_cpl,301,100):
    for b in range(1,7-Cpl):
        print('Расстояние между линиями=',a,' Кол-во линий,не считая ранее проложенных=',b)
        kab_k(b,a)
        Sechenie()
        for c in range(1,3):      
            U()
            print('Площадь сечения 1-й линии=',Sk)
            if deltaU<deltaUmax:
                break
            else:
                print('Не получилось.Увеличиваю сечение..')
                print('______________________________')
                Sk=S[S_index+c]
            time.sleep(2)
        if deltaU<deltaUmax:
            break
        else:
            print('Не сошлось по напряжению.Начинаю пересчет...')
            
        print('__________________________________________________')
        time.sleep(2)  
    if deltaU<deltaUmax:
            print('______________________________')
            print('Расчет завершен')
            print('______________________________')
            break
print('S одной линии=',Sk,'мм^2')
print('Кол-во линий всего',b+Cpl)
print('Кол-во наших линий ',b)
print('Расстояние между линиями',a)
print('k1=',k1)
print('k2=',k2)
