class CBU:
    def __init__(self, cbu: str) -> None:
        self.cbu = cbu

    def _first_block_is_valid(self, first_block: str) -> bool:
        """
        Checks the validity of the first block of a Clave Bancaria Uniforme (CBU).

        Args:
            first_block (str): The first eight digits of a CBU.

        Returns:
            bool: True if the first block is valid, False otherwise.


        The function verifies the check digit and ensures it matches the calculated differential value.
        The first block is considered valid if the check digit is nonzero and matches the differential, 
        or if the check digit is zero and the differential is equal to 10.
        """    
        bank_digits = first_block[:3]
        subsidiary_digits = first_block[3:7]
        check_digit = int(first_block[7:])

        bank_multipliers = [7, 1, 3]
        subsidiary_multipliers = [9, 7, 1, 3]

        # Calculate the sum of products for the bank digits and bank multipliers
        bank_sum = sum(int(digit) * multiplier for digit, multiplier in zip(bank_digits, bank_multipliers))

        # Calculate the sum of products for the subsidiary digits and subsidiary multipliers
        subsidiary_sum = sum(int(digit) * multiplier for digit, multiplier in zip(subsidiary_digits, subsidiary_multipliers))

        differential = 10 - (bank_sum + subsidiary_sum) % 10

        if (check_digit != 0 and check_digit == differential) or (check_digit == 0 and differential == 10):
            return True
        return False

    def _second_block_is_valid(self, second_block: str) -> bool:
        """
        Checks the validity of the second block of a Clave Bancaria Uniforme (CBU).

        Args:
            second_block (str): The second block of a CBU, consisting of 13 digits.

        Returns:
            bool: True if the second block is valid, False otherwise.

        The function verifies the check digit and ensures it matches the calculated differential value.
        The second block is considered valid if the check digit is nonzero and matches the differential, 
        or if the check digit is zero and the differential is equal to 10.
        """    
        account_digits = second_block[:13]
        check_digit = int(second_block[13:])

        account_multipliers = [3, 9, 7, 1, 3, 9, 7, 1, 3, 9, 7, 1, 3]

        # Calculate the sum of products for the account digits and account multipliers
        account_sum = sum(int(digit) * multiplier for digit, multiplier in zip(account_digits, account_multipliers))

        differential = 10 - account_sum % 10

        if(check_digit != 0 and check_digit == differential) or (check_digit == 0 and differential == 10):
            return True
        return False

    def is_valid(self) -> bool:
        """
        Checks the validity of the CBU.

        Returns:
            bool: True if the CBU is valid, False otherwise.

        Raises:
            TypeError: If the CBU is not provided as a string.
            ValueError: If the CBU contains non-numeric characters (such as spaces, dots, hyphens, etc)
            ValueError: If the CBU length is not 22 digits.
        """
        if not isinstance(self.cbu, str):
            raise TypeError("CBU must be provided in string format")
        
        if not self.cbu.isnumeric():
            raise ValueError("CBU can't contain non-numeric characters (such as spaces, dots, hyphens, etc)")

        if len(self.cbu) != 22:
            raise ValueError("CBU must be exactly 22 digits")

        first_block = self.cbu[:8]
        second_block = self.cbu[8:]

        if self._first_block_is_valid(first_block) and self._second_block_is_valid(second_block):
            return True
        return False
