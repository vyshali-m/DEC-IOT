# Convert DER certificate to C++ byte array
def der_to_cpp_array(filename):
    with open(filename, 'rb') as f:
        der_data = f.read()
    
    hex_data = der_data.hex().upper()
    cpp_array = ", ".join(f"0x{hex_data[i:i+2]}" for i in range(0, len(hex_data), 2))
    return cpp_array

# Specify the DER certificate file
filename = "bytes_cert.der"
cpp_array = der_to_cpp_array(filename)

# Print the C++ byte array
print("const uint8_t serverCertificate[] = {")
print(cpp_array)
print("};")
