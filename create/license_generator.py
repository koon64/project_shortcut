from os import path
import pathlib
from datetime import datetime


class LicenseGenerator:
    '''
    A class to create a license

    Attributes
    ----------
        LICENSE_FILE_NAME (str): default license name

    Methods
    -------
    has_license(_type) -> bool:
        Returns if the license exists
    
    get_format(_type) -> str:
        Returns the format of a license
    
    get_default_arguments() -> dict:
        Returns default arguments
    
    create(_type) -> bool:
        Creates a license from a type
    

    '''

    LICENSE_FILE_NAME = 'LICENSE'
    LICENSE_PATH = str(pathlib.Path(__file__).parent.absolute()) + '/licenses/{_type}.license'
    
    @classmethod
    def has_license(
            cls,
            _type: str
        ) -> bool:
        '''Returns if the license exists

        Args:
            _type (str): Type of the license
        
        Returns:
            bool: True if the license exists, False if it doesn't

        '''
        return path.exists(
            cls.LICENSE_PATH.format(
                _type=_type
            )
        )

    @classmethod
    def get_format(
            cls,
            _type: str
        ) -> str:
        '''Returns the license format from a license type

        Args:
            _type (str): Type of the license

        Returns:
            str: String of the license format
        
        '''
        with open(
            cls.LICENSE_PATH.format(
                _type=_type
            )
        ) as file:
            fmt = file.read()
            file.close()
            return fmt

    @classmethod
    def get_license(
            cls,
            _type: str,
            **kwargs
        ) -> str:
        '''Returns a formatted license
        
        Args:
            _type (str): Type of the license
            **kwargs: Arbitrary keyword arguments.
        
        Returns:
            str: Full license
        
        '''
        fmt = cls.get_format(
            _type=_type
        )
        # returns the format with the combined args of given and default
        return fmt.format(
            **kwargs
        )

    @classmethod
    def license_exists(
            cls
        ) -> bool:
        '''Checks if the licese file already exists
        
        Returns:
            bool: True if the file exists, False if not
        
        '''
        return path.exists(cls.LICENSE_FILE_NAME)

    @classmethod
    def create_license_file(
            cls,
            license: str
        ) -> bool:
        '''Writes a license to the file

        Args:
            license (str): String of the formatted license

        Returns:
            bool: True if the file was written, False if it could not be written

        '''
        try:
            # opens the file with write flag
            with open(
                cls.LICENSE_FILE_NAME,
                "w"
            ) as file:
                # write to the file
                file.write(license)
                # close file
                file.close()
                # return ok status
                return True
        except Exception as e:
            print("Could not write file")
            return False

    @classmethod
    def create(
            cls,
            **kwargs
        ) -> bool:
        '''Creates a license

        Args:
            _type (str): Type of the license
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bool: True if the license was created, False if the license was invalid
        
        '''
        # test if the license already exists
        if cls.license_exists():
            print("License already exists, skipping write")
            return True
        # get the license type
        _type = kwargs.get('license')
        # test if the license exists
        if not cls.has_license(_type):
            print(f'{_type} is an unsupported license, please add the license to the \'licenses\' folder')
            return False
        
        license = cls.get_license(
            _type=_type,
            **kwargs
        )
        return cls.create_license_file(license)

        