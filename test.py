import bfloat16_alu

if __name__ == "__main__":
    print(bfloat16_alu.bfloat16(7))
    hiA, opA = bfloat16_alu.bfloat16(5.25)
    hiB, opB = bfloat16_alu.bfloat16(3.25)
    signA, expA, manA = bfloat16_alu.process_bin_bfloat16(opA)
    signB, expB, manB = bfloat16_alu.process_bin_bfloat16(opB)
    print(signA, expA, manA)
    print(signB, expB, manB)
    # print(expA - expB)
    sum = bfloat16_alu.add(opA, opB)
    print(sum)
    # mansum = 75

    # if mansum < 128:
    #     normalize = 0
    
    #     while mansum < 128:
    #         mansum = mansum << 1
    #         normalize += 1

    # print(mansum)
    # print(normalize)
