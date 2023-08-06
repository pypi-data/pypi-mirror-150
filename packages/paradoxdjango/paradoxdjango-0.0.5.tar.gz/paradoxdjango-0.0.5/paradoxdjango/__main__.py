"""
Invokes paradoxdjango-admin when the paradoxdjango module is run as a script.

Example: python -m paradoxdjango check
"""
from paradoxdjango.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
