import sys, bfloat16_alu

if __name__ == "__main__":
    if len(sys.argv) > 1:
        operation = int(sys.argv[1])
        operandA = int(sys.argv[2])
        hex_float_opA, bin_float_opA = bfloat16_alu.bfloat16(operandA)
        operandB = int(sys.argv[3])
        hex_float_opB, bin_float_opB = bfloat16_alu.bfloat16(operandB)
    else:
        operation = 0
        operandA = int(sys.argv[2])
        hex_float_opA, bin_float_opA = bfloat16_alu.bfloat16(operandA)
        operandB = int(sys.argv[3])
        hex_float_opB, bin_float_opB = bfloat16_alu.bfloat16(operandB)

    if operation == 0:
        bfloat16_alu.add(bin_float_opA, bin_float_opB)

    elif operation == 1:
        bfloat16_alu.mult(bin_float_opA, bin_float_opB)