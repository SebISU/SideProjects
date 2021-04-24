#
# Podstawy Sztucznej Inteligencji, IIS 2020
# Autor: Tomasz Jaworski
# Opis: Szablon kodu do stabilizacji odwróconego wahadła (patyka) w pozycji pionowej podczas ruchu wózka.
#

import gym # Instalacja: https://github.com/openai/gym
import time
from helper import HumanControl, Keys, CartForce
import matplotlib.pyplot as plt


import numpy as np
import skfuzzy as fuzz
import math

#
# przygotowanie środowiska
#
control = HumanControl()
env = gym.make('gym_PSI:CartPole-v2')
env.reset()
env.render()


def on_key_press(key: int, mod: int):
    global control
    force = 10
    if key == Keys.LEFT:
        control.UserForce = force * CartForce.UNIT_LEFT # krok w lewo
    if key == Keys.RIGHT:
        control.UserForce = force * CartForce.UNIT_RIGHT # krok w prawo
    if key == Keys.P: # pauza
        control.WantPause = True
    if key == Keys.R: # restart
        control.WantReset = True
    if key == Keys.ESCAPE or key == Keys.Q: # wyjście
        control.WantExit = True

env.unwrapped.viewer.window.on_key_press = on_key_press

#########################################################
# KOD INICJUJĄCY - do wypełnienia
#########################################################

"""

1. Określ dziedzinę dla każdej zmiennej lingwistycznej. Każda zmienna ma własną dziedzinę.
2. Zdefiniuj funkcje przynależności dla wybranych przez siebie zmiennych lingwistycznych.
3. Wyświetl je, w celach diagnostycznych.
"""

angleRange = np.arange(-15, 16, 1)
cartRange = np.arange(-15, 16, 1)
moveRange = np.arange(-10, 11, 1)

angle_left = fuzz.trapmf(angleRange, [-15,-15, -5, 0])
angle_center = fuzz.trimf(angleRange, [-5, 0, 5])
angle_right = fuzz.trapmf(angleRange, [0, 5, 15, 15])

# for keeping stick in vertical position cart variables don't required

cart_left = fuzz.trapmf(cartRange, [-15,-15, -1, 0])
cart_center = fuzz.trimf(cartRange, [-1, 0, 1])
cart_right = fuzz.trapmf(cartRange, [0, 1, 15, 15])

move_left = fuzz.trimf(moveRange, [-10, -10, 0])
move_center = fuzz.trimf(moveRange, [-10, 0, 10])
move_right = fuzz.trimf(moveRange, [0, 10, 10])

"""
Przykład wyświetlania:
"""

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(angleRange, angle_left, 'b', linewidth=1.5, label='Left')
ax0.plot(angleRange, angle_center, 'g', linewidth=1.5, label='Zero')
ax0.plot(angleRange, angle_right, 'r', linewidth=1.5, label='Right')
ax0.set_title('Angle')
ax0.legend()

ax1.plot(cartRange, cart_left, 'b', linewidth=1.5, label='Left')
ax1.plot(cartRange, cart_center, 'g', linewidth=1.5, label='Zero')
ax1.plot(cartRange, cart_right, 'r', linewidth=1.5, label='Right')
ax1.set_title('cartRange')
ax1.legend()

ax2.plot(moveRange, move_left, 'b', linewidth=1.5, label='Left')
ax2.plot(moveRange, move_center, 'g', linewidth=1.5, label='Zero')
ax2.plot(moveRange, move_right, 'r', linewidth=1.5, label='Right')
ax2.set_title('moveRange')
ax2.legend()

plt.tight_layout()
plt.show()


#########################################################
# KONIEC KODU INICJUJĄCEGO
#########################################################


#
# Główna pętla symulacji
#
while not control.WantExit:

    #
    # Wstrzymywanie symulacji:
    # Pierwsze wciśnięcie klawisza 'p' wstrzymuje; drugie wciśnięcie 'p' wznawia symulację.
    #
    if control.WantPause:
        control.WantPause = False
        while not control.WantPause:
            time.sleep(0.1)
            env.render()
        control.WantPause = False

    #
    # Czy użytkownik chce zresetować symulację?
    if control.WantReset:
        control.WantReset = False
        env.reset()


    ###################################################
    # ALGORYTM REGULACJI - do wypełnienia
    ##################################################

    """
    Opis wektora stanu (env.state)
        cart_position   -   Położenie wózka w osi X. Zakres: -2.5 do 2.5. Ppowyżej tych granic wózka znika z pola widzenia. 
        cart_velocity   -   Prędkość wózka. Zakres +- Inf, jednak wartości powyżej +-2.0 generują zbyt szybki ruch.
        pole_angle      -   Pozycja kątowa patyka, a<0 to odchylenie w lewo, a>0 odchylenie w prawo. Pozycja kątowa ma
                            charakter bezwzględny - do pozycji wliczane są obroty patyka.
                            Ze względów intuicyjnych zaleca się konwersję na stopnie (+-180). 
        tip_velocity    -   Prędkość wierzchołka patyka. Zakres +- Inf. a<0 to ruch przeciwny do wskazówek zegara,
                            podczas gdy a>0 to ruch zgodny z ruchem wskazówek zegara.
                            
    Opis zadajnika akcji (fuzzy_response):
        Jest to wartość siły przykładana w każdej chwili czasowej symulacji, wyrażona w Newtonach.
        Zakładany krok czasowy symulacji to env.tau (20 ms).
        Przyłożenie i utrzymanie stałej siły do wózka spowoduje, że ten będzie przyspieszał do nieskończoności,
        ruchem jednostajnym.



    1. Przeprowadź etap rozmywania, w którym dla wartości zmierzonych wyznaczone zostaną ich przynależności do poszczególnych
       zmiennych lingwistycznych. Jedno fizyczne wejście (źródło wartości zmierzonych, np. położenie wózka) posiada własną
       zmienną lingwistyczną.
       
       Sprawdź funkcję fuzz.interp_membership
       
    2. Wyznacza wartości aktywacji reguł rozmytych, wyznaczając stopień ich prawdziwości.
       Przykład reguły:
       JEŻELI kąt patyka jest zerowy ORAZ prędkość wózka jest zerowa TO moc chwilowa jest zerowa
       JEŻELI kąt patyka jest lekko ujemny ORAZ prędkość wózka jest zerowa TO moc chwilowa jest lekko ujemna
       JEŻELI kąt patyka jest średnio ujemny ORAZ prędkość wózka jest lekko ujemna TO moc chwilowa jest średnio ujemna
       JEŻELI kąt patyka jest szybko rosnący w kierunku ujemnym TO moc chwilowa jest mocno ujemna
       .....

       Przyjmując, że spójnik LUB (suma rozmyta) to max() a ORAZ/I (iloczyn rozmyty) to min() sprawdź funkcje fmax i fmin.
    
    3. Przeprowadź agregację reguł o tej samej konkluzji.
       Jeżeli masz kilka reguł, posiadających tę samą konkluzję (ale różne przesłanki) to poziom aktywacji tych reguł
       należy agregować tak, aby jedna konkluzja miała jeden poziom aktywacji. Skorzystaj z sumy rozmytej.
    
    4. Dla każdej reguły przeprowadź operację wnioskowania Mamdaniego.
       Operatorem wnioskowania jest min().
       Przykład: Jeżeli lingwistyczna zmienna wyjściowa ForceToApply ma 5 wartości (strong left, light left, idle, light right, strong right)
       to liczba wyrażeń wnioskujących wyniesie 5 - po jednym wywołaniu operatora Mamdaniego dla konkluzji.
       
       W ten sposób wyznaczasz aktywacje poszczególnych wartości lingwistycznej zmiennej wyjściowej.
       Uważaj - aktywacja wartości zmiennej lingwistycznej w konkluzji to nie liczba a zbiór rozmyty.
       Ponieważ stosujesz operator min(), to wynikiem będzie "przycięty od góry" zbiór rozmyty.
       
    5. Agreguj wszystkie aktywacje dla danej zmiennej wyjściowej.
    
    6. Dokonaj defuzyfikacji (np. całkowanie ważone - centroid).  => diffuze  fuzz.centroid()
    
    7. Czym będzie wyjściowa wartość skalarna?
    """

    cart_position, cart_velocity, pole_angle, tip_velocity = env.state # Wartości zmierzone

    fuzzy_response = CartForce.IDLE_FORCE # do zmiennej fuzzy_response zapisz wartość siły, jaką chcesz przyłożyć do wózka.

    pole_angle = np.degrees(pole_angle)

    #################
    # expected cart position in range -2.5-2.5 
    expected = 0
    #################

    cart_diff = -1* (cart_position - expected) # *-1?

    angle_level_left = fuzz.interp_membership(angleRange, angle_left, pole_angle)
    angle_level_center = fuzz.interp_membership(angleRange, angle_center, pole_angle)
    angle_level_right = fuzz.interp_membership(angleRange, angle_right, pole_angle)

    cart_level_left = fuzz.interp_membership(cartRange, cart_left, cart_diff)
    cart_level_center = fuzz.interp_membership(cartRange, cart_center, cart_diff)
    cart_level_right = fuzz.interp_membership(cartRange, cart_right, cart_diff)

    angle_cart_left = np.fmax(angle_level_left, cart_level_left)
    angle_cart_center = np.fmax(angle_level_center, cart_level_center)
    angle_cart_right = np.fmax(angle_level_right, cart_level_right)

    # if you just want to keep stick in vertical position use angle variables instead of angle_cart. Cart variables don't required

    move_activation_left = np.fmin(angle_cart_left, move_left)
    move_activation_center = np.fmin(angle_cart_center, move_center)
    move_activation_right = np.fmin(angle_cart_right, move_right)
    
    # # Visualize this
    # tip0 = np.zeros_like(moveRange)
    # fig, ax0 = plt.subplots(figsize=(8, 3))

    # ax0.fill_between(moveRange, tip0, move_activation_left, facecolor='b', alpha=0.7)
    # ax0.plot(moveRange, move_left, 'b', linewidth=0.5, linestyle='--', )
    # ax0.fill_between(moveRange, tip0, move_activation_center, facecolor='g', alpha=0.7)
    # ax0.plot(moveRange, move_center, 'g', linewidth=0.5, linestyle='--')
    # ax0.fill_between(moveRange, tip0, move_activation_right, facecolor='r', alpha=0.7)
    # ax0.plot(moveRange, move_right, 'r', linewidth=0.5, linestyle='--')
    # ax0.set_title('Output membership activity')

    # # Turn off top/right axes
    # for ax in (ax0,):
    #     ax.spines['top'].set_visible(False)
    #     ax.spines['right'].set_visible(False)
    #     ax.get_xaxis().tick_bottom()
    #     ax.get_yaxis().tick_left()

    # plt.tight_layout()
    # plt.show()


    aggregated = np.fmax(move_activation_left, np.fmax(move_activation_center, move_activation_right))
    fuzzy_response = fuzz.defuzz(moveRange, aggregated, 'centroid')


    #
    # KONIEC algorytmu regulacji
    #########################

    # Jeżeli użytkownik chce przesunąć wózek, to jego polecenie ma wyższy priorytet
    if control.UserForce is not None:
        applied_force = control.UserForce
        control.UserForce = None
    else:
        applied_force = fuzzy_response

    #
    # Wyświetl stan środowiska oraz wartość odpowiedzi regulatora na ten stan.
    print(
        f"cpos={cart_position:8.4f}, cvel={cart_velocity:8.4f}, pang={pole_angle:8.4f}, tvel={tip_velocity:8.4f}, force={applied_force:8.4f}")

    #
    # Wykonaj krok symulacji
    env.step(applied_force)

    #
    # Pokaż kotku co masz w środku
    env.render()
    #time.sleep(0.1)

#
# Zostaw ten patyk!
env.close()


# range of angle value => -15-15 degrees
# if you want to set an expected state you should set a 5th input variable
# cart movement velocity is a sum value of all forces, but decreases if there is no new move
# tip velocity about 13 is possible
# using just the angle is enough