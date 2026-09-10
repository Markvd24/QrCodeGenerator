exponent_to_integer = [
    1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38, 76, 152, 45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 192, 157, 39, 78, 156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35, 70, 140, 5, 10, 20, 40, 80, 160, 93, 186, 105, 210, 185, 111, 222, 161, 95, 190, 97, 194, 153, 47, 94, 188, 101, 202, 137, 15, 30, 60, 120, 240, 253, 231, 211, 187, 107, 214, 177, 127, 254, 225, 223, 163, 91, 182, 113, 226, 217, 175, 67, 134, 17, 34, 68, 136, 13, 26, 52, 104, 208, 189, 103, 206, 129, 31, 62, 124, 248, 237, 199, 147, 59, 118, 236, 197, 151, 51, 102, 204, 133, 23, 46, 92, 184, 109, 218, 169, 79, 158, 33, 66, 132, 21, 42, 84, 168, 77, 154, 41, 82, 164, 85, 170, 73, 146, 57, 114, 228, 213, 183, 115, 230, 209, 191, 99, 198, 145, 63, 126, 252, 229, 215, 179, 123, 246, 241, 255, 227, 219, 171, 75, 150, 49, 98, 196, 149, 55, 110, 220, 165, 87, 174, 65, 130, 25, 50, 100, 200, 141, 7, 14, 28, 56, 112, 224, 221, 167, 83, 166, 81, 162, 89, 178, 121, 242, 249, 239, 195, 155, 43, 86, 172, 69, 138, 9, 18, 36, 72, 144, 61, 122, 244, 245, 247, 243, 251, 235, 203, 139, 11, 22, 44, 88, 176, 125, 250, 233, 207, 131, 27, 54, 108, 216, 173, 71, 142, 1]
integer_to_exponent = [
    0, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75, 4, 100, 224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113, 5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69, 29, 181, 194, 125, 106, 39, 249, 185, 201, 154, 9, 120, 77, 228, 114, 166, 6, 191, 139, 98, 102, 221, 48, 253, 226, 152, 37, 179, 16, 145, 34, 136, 54, 208, 148, 206, 143, 150, 219, 189, 241, 210, 19, 92, 131, 56, 70, 64, 30, 66, 182, 163, 195, 72, 126, 110, 107, 58, 40, 84, 250, 133, 186, 61, 202, 94, 155, 159, 10, 21, 121, 43, 78, 212, 229, 172, 115, 243, 167, 87, 7, 112, 192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 49, 197, 254, 24, 227, 165, 153, 119, 38, 184, 180, 124, 17, 68, 146, 217, 35, 32, 137, 46, 55, 63, 209, 91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190, 97, 242, 86, 211, 171, 20, 42, 93, 158, 132, 60, 57, 83, 71, 109, 65, 162, 31, 45, 67, 216, 183, 123, 164, 118, 196, 23, 73, 236, 127, 12, 111, 246, 108, 161, 59, 82,41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90, 203, 89, 95, 176, 156, 169, 160, 81, 11, 245, 22, 235, 122, 117,44, 215, 79, 174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168, 80, 88, 175]
exp_add = lambda a, b: integer_to_exponent[exponent_to_integer[a % 255] ^ exponent_to_integer[b % 255]]
exp_to_int = lambda A: [exponent_to_integer[a] for a in A]
int_to_exp = lambda A: [integer_to_exponent[a] for a in A]

def generate_generator_polynomial(type):
    # index: [a for x^type, a for x^(type-1), a for x^(type-2), ..., a for x^0]
    # So building the formula, it would be:
    # poly[0] * x^n + poly[1] * x^(n-1) + poly[2] * x^(n-2) + ... poly[n] * x^0
    
    if type <= 1:
        return [0, 0]

    previous_polynomial = generate_generator_polynomial(type-1)

    new_polynomial = [previous_polynomial[0]]

    for i in range(type-1):
        from_x = previous_polynomial[i+1]
        from_a = previous_polynomial[i] + type - 1
        new_polynomial.append(exp_add(from_x, from_a))

    new_polynomial.append(previous_polynomial[-1] + type - 1)
    return new_polynomial

message_polynomial = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
for num in [10]:
    generator_polynomial = generate_generator_polynomial(num)
    print(generator_polynomial)
    print()
    print()
quit()

def polynomial_long_devision(message_polynomial_in: list[int], generator_polynomial_in):
    # Step 1: Set variables
    message = int_to_exp(message_polynomial_in)
    generator = generator_polynomial_in

    number_of_codewords = len(message)
    
    # Step 2: Multiply the Message Polynomial by x^n where n is the number of codewords
    message = message
    print(message)
    print()
    for step in range(1):
        # Multiply the Generator Polynomial by the Lead Term of the Message Polynomial
        # XOR the result with the message polynomial

        lead_term = message[0]

        for alpha in range(len(generator) - 1):
            generator_alpha = generator[alpha + 1] + lead_term
            print(exponent_to_integer[generator_alpha])
            message[alpha] = exp_add(message[alpha + 1], generator_alpha)

        message[-1] = (generator[-1] + lead_term) % 255
            
        print(exp_to_int(message))
        print()

    return message








print(polynomial_long_devision(message_polynomial, generator_polynomial))

