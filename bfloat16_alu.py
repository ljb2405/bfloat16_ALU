import sys

"""Bfloat16 ALU simulator"""
############# Pre-processor Functions (int to bin bfloat16) #################
# Function for converting decimal to binary
def float_bin(my_number, places):
    if places == 0:
        my_whole = str(my_number)
        my_dec = 0
        places = 30
    else:
        my_whole, my_dec = str(my_number).split(".")
    my_whole = int(my_whole)
    res = (str(bin(my_whole))+".").replace('0b','')
 
    for x in range(places):
        my_dec = str('0.')+str(my_dec)
        temp = '%1.20f' %(float(my_dec)*2)
        my_whole, my_dec = temp.split(".")
        res += my_whole
    return res
 
# Converts int to hex/bin floating number
def bfloat16(n) :
    # identifying whether the number
    # is positive or negative
    sign = 0
    if n < 0 :
        sign = 1
        n = n * (-1)
    
    if isinstance(n, int) is True:
        p = 0
    else:
        p = 30
    # convert float to binary
    dec = float_bin (n, places = p)
 
    dotPlace = dec.find('.')
    onePlace = dec.find('1')
    # finding the mantissa
    if onePlace > dotPlace:
        dec = dec.replace(".","")
        onePlace -= 1
        dotPlace -= 1
    elif onePlace < dotPlace:
        dec = dec.replace(".","")
        dotPlace -= 1
    mantissa = dec[onePlace+1:]
 
    # calculating the exponent(E)
    exponent = dotPlace - onePlace
    exponent_bits = exponent + 127
 
    # converting the exponent from
    # decimal to binary
    exponent_bits = bin(exponent_bits).replace("0b",'')
 
    mantissa = mantissa[0:7]
 
    # the bfloat16 notation in binary    
    final = str(sign) + exponent_bits.zfill(8) + mantissa
 
    # convert the binary to hexadecimal
    hstr = '0x%0*X' %((len(final) + 3) // 4, int(final, 2))
    return (hstr, final)

# Parses binary floating number to sign, exponent, and mantissa
def process_bin_bfloat16(bfloat16 : str):
    sign = int(bfloat16[0])
    # TODO: Figure out how to NOT represent in neg number
    exp = int(bfloat16[1:9], 2)
    mantissa = int(bfloat16[9:16], 2)
    return sign, exp, mantissa
#############################################################################
############################### ALU Operations ##############################
def cmp(operandA, operandB):
    signA, expA, manA = process_bin_bfloat16(operandA)
    signB, expB, manB = process_bin_bfloat16(operandB)

    if signA == signB and expA == expB and manA == manB:
        return 0

    # Think about in schematic way

# Add op for the ALU
# TODO: Truncation error, diff sign not covered, overflow/underflow not dealt,
# same sign ops work (for positive)
def add(operandA, operandB):
    signA, expA, manA = process_bin_bfloat16(operandA)
    signB, expB, manB = process_bin_bfloat16(operandB)

    # Sign Comparator
    sign = signA ^ signB

    # Difference Module
    # In: expA and expB Out: expA - expB
    diffexp = expA - expB

    # Absolute Value Difference Module
    absdiff = abs(diffexp)

    # Mux Signal Generator
    # if A is smaller, manshiftsel = 0
    # if B is smaller, manshiftsel = 1
    if diffexp < 0:
        manshiftsel = 0
    else:
        manshiftsel = 1
    
    # Mantissa Addition
    # Man 1 Mux - Mux without shifter
    if manshiftsel == 0:
        man1 = manB + 128
    elif manshiftsel == 1:
        man1 = manA + 128
    
    # Man 2 Mux - Mux with shifter
    if manshiftsel == 0:
        man2 = manA + 128
    elif manshiftsel == 1:
        man2 = manB + 128

    # Man 2 Shifter
    man2 = man2 >> absdiff
    # Mantissa Adder
    mansum = man1 + man2
    print(mansum)
    # Normalize Mantissa Shifter
    carryout = 0
    # Truncates mantissa to 8 bits with the hidden bit
    if mansum > 255:
        mansum = mansum >> 1
    # Computes carryout
    if mansum > 127:
        carryout = 1
    # See if the mantissa needs to be normalized
    if mansum < 64:
        normalize = 0

        while mansum < 64:
            mansum = mansum * 2 ** 1
            normalize += 1
    # Mask 
    # mansum = mansum - 256

    # Exponent Computation
    if manshiftsel == 0:
        expsum = expB
    elif manshiftsel == 1:
        expsum = expA

    if carryout == 1:
        expsum += 1
    
    # Sign module
    if sign:
        if manshiftsel == 0:
            signsum = signB
        elif manshiftsel == 1:
            signsum = signA
        
    elif sign == 0:
        signsum = signA

    # Mantissa Truncator for Python emulation
    while mansum > 127:
        mansum = mansum // 2
    
    while expsum > 511:
        expsum = expsum // 2

    binman = bin(mansum)

    while len(binman) < 11:
        binman = binman + '0'

    return '0b' + '{0:01b}'.format(signsum) + ' {0:08b}'.format(expsum) + ' ' + binman[3:10]# ' {0:07b}'.format(mansum)

    # # Sign Comparator
    # # if 0, positive & if 1, negative
    # if signA > signB:
    #     comp = -1
    # elif signA == signB:
    #     comp = 0
    # else:
    #     comp = 1
    
    # signcomp = signA ^ signB
    # # Exponent Comparison
    # if expA > expB:
    #     expcomp = 1
    # elif expA == expB:
    #     expcomp = 0
    # else:
    #     expcomp = -1
    
    # # Mantissa Comparison
    # if manA > manB:
    #     mancomp = 1
    # elif manA == manB:
    #     mancomp = 0
    # else:
    #     mancomp = -1

    # # Control Logic
    # # Diffuse = 1 if A > B
    # # Diffuse = 0 if A < B
    # if comp:
    #     diffuse = 1
    # elif comp == -1:
    #     diffuse = 0
    # else:
    #     if expcomp:
    #         diffuse = 1
    #     elif expcomp == -1:
    #         diffuse = 0
    #     else:
    #         if mancomp:
    #             diffuse = 1
    #         elif mancomp == -1:
    #             diffuse = 0
    #         else:
    #             return bfloat16(0)

    # # Exponent Calculation
    # # Exponent Difference Computation
    # # Find a better way to represent this in modular sense
    # if diffuse:
    #     diff = expA - expB
    # else:
    #     diff = expB - expA
    
    # # write more in a schematic way
    # if diffuse and diff <= 8:
    #     manB >> diff
    # elif diffuse == 0 and diff <= 8:
    #     manA >> diff
    
    # # Add Computation based on control signal
    # if signcomp == 0 and diffuse:
    #     resman = manA + manB
    #     resexp = expA

    #     while resman >= 128:
    #         resman >>= 1
    #         resexp += 1
    #         print(bin(resman))
            
    #     return '0b' + '{0:01b}'.format(signA) + '{0:08b}'.format(resexp) + '{0:07b}'.format(resman)

    # elif signcomp == 0 and diffuse == 0:
    #     resman = manA + manB
    #     resexp = expB

    #     while resman >= 128:
    #         resman = resman >> 1
    #         resexp += 1
    #         print(bin(resman))
            
    #     return '0b' + '{0:01b}'.format(signA) + '{0:08b}'.format(resexp) + '{0:07b}'.format(resman)
    
    # elif signcomp == 1 and diffuse:
    #     resman = manA - manB
    #     resexp = expA
    #     while resman < 128:
    #         resexp -= 1
    #         resman <<= 1
    #     return '0b' + '{0:01b}'.format(signA) + '{0:08b}'.format(resexp) + '{0:07b}'.format(resman)

    # elif signcomp == 1 and diffuse == 0:
    #     resman = manB - manA
    #     resexp = expB
    #     while resman < 128:
    #         resexp -= 1 
    #         resman <<= 1
    #     return '0b' + '{0:01b}'.format(signB) + '{0:08b}'.format(resexp) + '{0:07b}'.format(resman)

# Mult op for the ALU
def mult(operandA, operandB):
    signA, expA, manA = process_bin_bfloat16(operandA)
    signB, expB, manB = process_bin_bfloat16(operandB)


    return 0
