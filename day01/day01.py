spelled_to_digits_array = (
    ('one', '1'),
    ('two', '2'),
    ('three', '3'),
    ('four', '4'),
    ('five', '5'),
    ('six', '6'),
    ('seven', '7'),
    ('eight', '8'),
    ('nine', '9'),
)

def spelled_to_digits(calibration_value_string):
    for spelled, digit in spelled_to_digits_array:
        calibration_value_string = calibration_value_string.replace(
            spelled, 
            spelled[:-1] + digit + spelled[-1]
        )
    return calibration_value_string

def get_calibration_value(calibration_value_string):
    digits = [digit for digit in calibration_value_string if digit.isdigit()]
    return int(digits[0] + digits[-1])
    

calibration_values_file = open('calibration_values.txt', 'r')
calibration_values_strings = calibration_values_file.readlines()
calibration_values_file.close()

calibration_values_strings = list(map(spelled_to_digits, calibration_values_strings))
calibration_values = list(map(get_calibration_value, calibration_values_strings))
print(sum(calibration_values))