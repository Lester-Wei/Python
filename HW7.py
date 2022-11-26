#!/bin/python3

import math
import os
import random
import re
import sys
from typing import Dict, Optional, Tuple, Any

Action = str

class State:
    # Implement the State class here
    una = 'unauthorized'
    a = 'authorized'
def login_checker(action_param,atm_password,atm_current_balance):
    print('login',action_param,atm_password,atm_current_balance)
    if action_param == atm_password:
        return (True,atm_current_balance,None)
    else:
        return (False,atm_current_balance,None)
def logout_checker(action_param,atm_password,atm_current_balance):
    print('logout',action_param,atm_password,atm_current_balance)
    return (True,atm_current_balance,None)
def withdraw_checker(action_param,atm_password,atm_current_balance):
    print('withdraw',action_param,atm_password,atm_current_balance)
    if atm_current_balance == None:
        atm_current_balance = 0
    if action_param > atm_current_balance:
        return (False,atm_current_balance,None)
    else:
        return (True,atm_current_balance - action_param,None)
def deposit_checker(action_param,atm_password,atm_current_balance):
    if atm_current_balance == None:
        return (True,action_param, None)
    else:
        return (True,atm_current_balance + action_param, None)
def balance_checker(action_param,atm_password,atm_current_balance):
    print('balance',action_param,atm_password,atm_current_balance)
    if atm_current_balance == None:
        return (True,atm_current_balance,0)
    else:
        return (True,atm_current_balance,atm_current_balance)
def dbl_login_checker(action_param,atm_password,atm_current_balance):
    if atm_current_balance == None:
        atm_current_balance = 0
    print('dbl_login',action_param,atm_password,atm_current_balance)
    return (False,atm_current_balance,None)
# Implement the transition_table here
transition_table = {State.una:[('login',login_checker,State.a)],
                    State.a:[('login',dbl_login_checker,State.a),
                            ('withdraw',withdraw_checker,State.a),
                            ('deposit',deposit_checker,State.a),
                            ('balance',balance_checker,State.a),
                            ('logout',logout_checker,State.una)]}

# Implement the init_state here
init_state = State.una

# Look for the implementation of the ATM class in the below Tail section
if __name__ == "__main__":
    class ATM:
        def __init__(self, init_state: State, init_balance: int, password: str, transition_table: Dict):
            self.state = init_state
            self._balance = init_balance
            self._password = password
            self._transition_table = transition_table

        def next(self, action: Action, param: Optional) -> Tuple[bool, Optional[Any]]:
            try:
                for transition_action, check, next_state in self._transition_table[self.state]:
                    if action == transition_action:
                        passed, new_balance, res = check(param, self._password, self._balance)
                        if passed:
                            self._balance = new_balance
                            self.state = next_state
                            return True, res
            except KeyError:
                pass
            return False, None


    if __name__ == "__main__":
        fptr = open(os.environ['OUTPUT_PATH'], 'w')
        password = input()
        init_balance = int(input())
        atm = ATM(init_state, init_balance, password, transition_table)
        q = int(input())
        for _ in range(q):
            action_input = input().split()
            action_name = action_input[0]
            try:
                action_param = action_input[1]
                if action_name in ["deposit", "withdraw"]:
                    action_param = int(action_param)
            except IndexError:
                action_param = None
            success, res = atm.next(action_name, action_param)
            if res is not None:
                fptr.write(f"Success={success} {atm.state} {res}\n")
            else:
                fptr.write(f"Success={success} {atm.state}\n")

        fptr.close()


def countWaysToCreateWave(arr, m):
    if len(arr) == 0:
        return 0
    print(arr, m)
    modulo = 10e9 + 7
    n = len(arr)
    dp_up = [[0 for x in range(m)] for x in range(n + 1)]
    k = 0
    # Beginning
    # If the first number is -1 then the probable ways of all numbers to form the wave is 1
    if arr[0] == -1:
        dp_up[0] = [1 for x in range(m)]
    # If the first number is t then the probable ways of number t to form the wave is 1
    else:
        dp_up[0][arr[0] - 1] = 1
    # Define s0,s1,s2,...,st,...sn-1 as numbers in the array, define Upwave as wave where s2 > s1 and Downwave as wave where s2 < s1
    # Calculate Upwave:

    for t in range(1, n):  # denote st = arr[t]
        # peak_sign siginifies the tth number should be a peak of the wave or not, 0=small, 1=large
        peak_sign = int((t + 1) % 2)
        # if tth and t+1th numbers are both -1, calculate the probable ways
        if arr[t - 1] == -1 and arr[t] == -1:
            if peak_sign == 1:
                dp_up[t] = [sum(dp_up[t - 1][0:k:]) for k in range(m)]
            else:
                dp_up[t] = [sum(dp_up[t - 1][k:-1:]) for k in range(m)]
        # if tth is -1 and t+1th number isn't -1 , calculate the probable ways
        elif arr[t - 1] == -1 and arr[t] != -1:
            if peak_sign == 1:
                # small parts are remained and larger or equal numbers become zero
                alist = dp_up[t - 1][0:arr[t]:]
                zerolist = [0 for x in range(arr[t], m)]
                alist.extend(zerolist)
                dp_up[t] = alist
            else:
                zerolist = [0 for x in range(0, arr[t])]
                alist = dp_up[t - 1][arr[t]:m:]
                zerolist.extend(alist)
                dp_up[t] = zerolist

        elif arr[t - 1] != -1 and arr[t] == -1:
            if peak_sign == 1:
                # small parts are remained and larger or equal numbers become zero
                zerolist = [0 for x in range(arr[t - 1])]
                alist = [dp_up[t - 1][arr[t - 1] - 1] for x in range(arr[t - 1], m)]
                zerolist.extend(alist)
                dp_up[t] = zerolist
            else:
                zerolist = [0 for x in range(arr[t - 1], m)]
                alist = [dp_up[t - 1][arr[t - 1] - 1] for x in range(arr[t - 1])]
                alist.extend(zerolist)
                dp_up[t] = alist

        elif arr[t - 1] != -1 and arr[t] != -1:
            if peak_sign == 1:
                if arr[t] <= arr[t - 1]:
                    dp_up[t] = [0 for x in range(m)]
                else:
                    dp_up[t] = [0 for x in range(m)]
                    dp_up[t][arr[t] - 1] = dp_up[t - 1][arr[t - 1] - 1]
    # Ending
    peak_sign = int((n + 1) % 2)
    if arr[-2] == -1 and arr[-1] == -1:
        upres = int(sum(dp_up[-2]) % modulo)
    elif arr[-2] != -1 and arr[-1] == -1:
        if peak_sign == 1:
            upres = int((sum(dp_up[-2]) * (m - arr[-2])) % modulo)
        else:
            upres = int((sum(dp_up[-2]) * (arr[-2] - 1)) % modulo)
    elif arr[-2] == -1 and arr[-1] != -1:
        if peak_sign == 1:
            upres = int(sum(dp_up[-2][0:k:]) % modulo)
        else:
            upres = int(sum(dp_up[-2][k:-1:]) % modulo)
    else:
        if peak_sign == 1:
            if arr[-2] >= arr[-1]:
                upres = 0
            else:
                upres = int(sum(dp_up[-2]) % modulo)
        else:
            if arr[-2] <= arr[-1]:
                upres = 0
            else:
                upres = int(sum(dp_up[-2]) % modulo)

    return upres



####################### Modified
def countWaysToCreateWave(arr, m):
    if len(arr) == 0:
        return 0
    print(arr, m)
    modulo = 10e9 + 7
    n = len(arr)
    dp_up = [[0 for x in range(m)] for x in range(n + 1)]
    k = 0
    # Beginning
    # If the first number is -1 then the probable ways of all numbers to form the wave is 1
    if arr[0] == -1:
        dp_up[0] = [1 for x in range(m)]
    # If the first number is t then the probable ways of number t to form the wave is 1
    else:
        dp_up[0][arr[0] - 1] = 1
    # Define s0,s1,s2,...,st,...sn-1 as numbers in the array, define Upwave as wave where s2 > s1 and Downwave as wave where s2 < s1
    # Calculate Upwave:

    for t in range(1, n):  # denote st = arr[t]
        # peak_sign siginifies the tth number should be a peak of the wave or not, 0=small, 1=large
        peak_sign = int((t + 1) % 2)
        # if tth and t+1th numbers are both -1, calculate the probable ways
        if arr[t - 1] == -1 and arr[t] == -1:
            if peak_sign == 1:
                dp_up[t] = [sum(dp_up[t - 1][0:k:]) for k in range(m)]
            else:
                dp_up[t] = [sum(dp_up[t - 1][k:-1:]) for k in range(m)]
        # if tth is -1 and t+1th number isn't -1 , calculate the probable ways
        elif arr[t - 1] == -1 and arr[t] != -1:
            if peak_sign == 1:
                # small parts are remained and larger or equal numbers become zero
                alist = dp_up[t - 1][0:arr[t]:]
                zerolist = [0 for x in range(arr[t], m)]
                alist.extend(zerolist)
                dp_up[t] = alist
            else:
                zerolist = [0 for x in range(0, arr[t])]
                alist = dp_up[t - 1][arr[t]:m:]
                zerolist.extend(alist)
                dp_up[t] = zerolist

        elif arr[t - 1] != -1 and arr[t] == -1:
            if peak_sign == 1:
                # small parts are remained and larger or equal numbers become zero
                zerolist = [0 for x in range(arr[t - 1])]
                alist = [dp_up[t - 1][arr[t - 1] - 1] for x in range(arr[t - 1], m)]
                zerolist.extend(alist)
                dp_up[t] = zerolist
            else:
                zerolist = [0 for x in range(arr[t - 1], m)]
                alist = [dp_up[t - 1][arr[t - 1] - 1] for x in range(arr[t - 1])]
                alist.extend(zerolist)
                dp_up[t] = alist

        elif arr[t - 1] != -1 and arr[t] != -1:
            if peak_sign == 1:
                if arr[t] <= arr[t - 1]:
                    dp_up[t] = [0 for x in range(m)]
                else:
                    dp_up[t] = [0 for x in range(m)]
                    dp_up[t][arr[t] - 1] = dp_up[t - 1][arr[t - 1] - 1]
    # Ending
    peak_sign = int((n + 1) % 2)
    if arr[-2] == -1 and arr[-1] == -1:
        upres = int(sum(dp_up[-2]) % modulo)
    elif arr[-2] != -1 and arr[-1] == -1:
        if peak_sign == 1:
            upres = int((sum(dp_up[-2]) * (m - arr[-2])) % modulo)
        else:
            upres = int((sum(dp_up[-2]) * (arr[-2] - 1)) % modulo)
    elif arr[-2] == -1 and arr[-1] != -1:
        if peak_sign == 1:
            upres = int(sum(dp_up[-2][0:k:]) % modulo)
        else:
            upres = int(sum(dp_up[-2][k:-1:]) % modulo)
    else:
        if peak_sign == 1:
            if arr[-2] >= arr[-1]:
                upres = 0
            else:
                upres = int(sum(dp_up[-2]) % modulo)
        else:
            if arr[-2] <= arr[-1]:
                upres = 0
            else:
                upres = int(sum(dp_up[-2]) % modulo)







    print(upres)

    dp_up = [[0 for x in range(m)] for x in range(n + 1)]
    k = 0
    # Beginning
    # If the first number is -1 then the probable ways of all numbers to form the wave is 1
    if arr[0] == -1:
        dp_up[0] = [1 for x in range(m)]
    # If the first number is t then the probable ways of number t to form the wave is 1
    else:
        dp_up[0][arr[0] - 1] = 1
    # Define s0,s1,s2,...,st,...sn-1 as numbers in the array, define Upwave as wave where s2 > s1 and Downwave as wave where s2 < s1
    # Calculate Upwave:

    for t in range(1, n):  # denote st = arr[t]
        # peak_sign siginifies the tth number should be a peak of the wave or not, 0=small, 1=large
        peak_sign = int((t) % 2)
        # if tth and t+1th numbers are both -1, calculate the probable ways
        if arr[t - 1] == -1 and arr[t] == -1:
            if peak_sign == 1:
                dp_up[t] = [sum(dp_up[t - 1][0:k:]) for k in range(m)]
            else:
                dp_up[t] = [sum(dp_up[t - 1][k:-1:]) for k in range(m)]
        # if tth is -1 and t+1th number isn't -1 , calculate the probable ways
        elif arr[t - 1] == -1 and arr[t] != -1:
            if peak_sign == 1:
                # small parts are remained and larger or equal numbers become zero
                alist = dp_up[t - 1][0:arr[t]:]
                zerolist = [0 for x in range(arr[t], m)]
                alist.extend(zerolist)
                dp_up[t] = alist
            else:
                zerolist = [0 for x in range(0, arr[t])]
                alist = dp_up[t - 1][arr[t]:m:]
                zerolist.extend(alist)
                dp_up[t] = zerolist

        elif arr[t - 1] != -1 and arr[t] == -1:
            if peak_sign == 1:
                # small parts are remained and larger or equal numbers become zero
                zerolist = [0 for x in range(arr[t - 1])]
                alist = [dp_up[t - 1][arr[t - 1] - 1] for x in range(arr[t - 1], m)]
                zerolist.extend(alist)
                dp_up[t] = zerolist
            else:
                zerolist = [0 for x in range(arr[t - 1], m)]
                alist = [dp_up[t - 1][arr[t - 1] - 1] for x in range(arr[t - 1])]
                alist.extend(zerolist)
                dp_up[t] = alist

        elif arr[t - 1] != -1 and arr[t] != -1:
            if peak_sign == 1:
                if arr[t] <= arr[t - 1]:
                    dp_up[t] = [0 for x in range(m)]
                else:
                    dp_up[t] = [0 for x in range(m)]
                    dp_up[t][arr[t] - 1] = dp_up[t - 1][arr[t - 1] - 1]
    # Ending
    peak_sign = int((n) % 2)
    if arr[-2] == -1 and arr[-1] == -1:
        downres = int(sum(dp_up[-2]) % modulo)
    elif arr[-2] != -1 and arr[-1] == -1:
        if peak_sign == 1:
            downres = int((sum(dp_up[-2]) * (m - arr[-2])) % modulo)
        else:
            downres = int((sum(dp_up[-2]) * (arr[-2] - 1)) % modulo)
    elif arr[-2] == -1 and arr[-1] != -1:
        if peak_sign == 1:
            downres = int(sum(dp_up[-2][0:k:]) % modulo)
        else:
            downres = int(sum(dp_up[-2][k:-1:]) % modulo)
    else:
        if peak_sign == 1:
            if arr[-2] >= arr[-1]:
                downres = 0
            else:
                downres = int(sum(dp_up[-2]) % modulo)
        else:
            if arr[-2] <= arr[-1]:
                downres = 0
            else:
                downres = int(sum(dp_up[-2]) % modulo)
    print(downres)
    return upres + downres

