from random import *
ошибки = 0
for i in range(10):
    a = randint(2,10)
    b = randint(2,10)
    r = int(input(str(a)+' x '+str(b)+' = '))
    if r!=a*b:
          print('Неверно. Ответ = ',a*b)
          ошибки+=1
print('Число ошибок: ',ошибки)
if ошибки==0: print('отлично')
elif 1<=ошибки<=2: print('хорошо')
elif 3<=ошибки<=4: print('удовлетворительно')
else: print('плохо')

