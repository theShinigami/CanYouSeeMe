#!/usr/bin/python3
# author: @masterSal
import r2pipe

BIN_NAME = "canyouseeme"

def solve():
    # open binary
    r = r2pipe.open(BIN_NAME, flags=['-2', '-d'])

    # flag char check break point
    BP1 = 0x08048561

    # break point for flag index
    RANDOM_NUM_BP = 0x08048513

    flag = list('X'*22)

    # to track how many char update in flag array
    flag_update_counter = 0

    # auto analyze
    r.cmd('aaaa')

    # seek to main
    r.cmd('s main')

    # set breakpoint after random function call
    r.cmd(f'db {RANDOM_NUM_BP}')

    # set breakpoint for flag cmp instruction
    r.cmd(f'db {BP1}')

    # ood prep
    ood_arg = 'ood a b {}'.format(''.join(flag))
    r.cmd(ood_arg)

    while True:

        # if all the flag char has been update
        # break out of the loop
        if flag_update_counter >= 22:
            break
      
        # run program
        r.cmd('dc')

        # get the random value from eax register
        flag_index = int(r.cmd('dr eax').strip(), 16)

        # run program
        r.cmd('dc')

        # get flag char from eax register
        flag_char = int(r.cmd('dr eax').strip(), 16)

        # if the the register value for the flag char
        # is different than the index of the passed flag argument
        # update the flag array argument
        if flag[flag_index] != chr(flag_char):

            # update flag char
            flag[flag_index] = chr(flag_char)

            # update flag char counter
            flag_update_counter += 1

            # ood prep
            ood_arg = "ood a b {}".format(''.join(flag))
            r.cmd(ood_arg)

            print(''.join(flag), end='\r')
    print()

def main():
    solve()


if __name__ == "__main__":
    main()


